"""Prediction API endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
import numpy as np

from app.core.database import get_db
from app.models.test_execution import TestExecution
from app.models.dataset import Dataset
from app.ml.features.feature_extractor import FeatureExtractor
from app.ml.models.flaky_detector import create_detector

router = APIRouter()


@router.post("/analyze/{dataset_id}")
async def analyze_dataset(
    dataset_id: int,
    model_type: str = "random_forest",
    db: Session = Depends(get_db)
):
    """Analyze a dataset and detect flaky tests."""
    
    # Get dataset
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    # Get executions
    executions = db.query(TestExecution).filter(
        TestExecution.dataset_id == dataset_id
    ).all()
    
    if not executions:
        raise HTTPException(status_code=400, detail="No executions found")
    
    # Convert to DataFrame
    exec_data = []
    for exec in executions:
        exec_data.append({
            'test_id': exec.test_id,
            'timestamp': exec.timestamp,
            'outcome': exec.outcome,
            'duration': exec.duration,
            'retry_count': exec.retry_count,
            'error_message': exec.error_message,
            'environment': exec.environment,
            'is_flaky_label': exec.is_flaky_label
        })
    
    df = pd.DataFrame(exec_data)
    
    # Extract features
    extractor = FeatureExtractor()
    features_df = extractor.extract_features(df)
    
    # Separate features and labels
    feature_cols = [col for col in features_df.columns if col not in ['test_id', 'label']]
    X = features_df[feature_cols]
    
    # Create and train detector
    detector = create_detector(model_type)
    
    # If we have labels, train on them
    if 'label' in features_df.columns and features_df['label'].nunique() > 1:
        labels = features_df['label']
        # Only train on labeled data
        labeled_mask = labels.isin(['FLAKY', 'NOT_FLAKY'])
        if labeled_mask.sum() > 10:  # Need at least 10 samples
            X_train = X[labeled_mask]
            y_train = labels[labeled_mask]
            detector.fit(X_train, y_train)
    
    # Make predictions
    predictions = detector.predict(X)
    probabilities = detector.predict_proba(X)
    
    # Get feature importance
    if hasattr(detector, 'get_feature_importance'):
        feature_importance = detector.get_feature_importance()
    else:
        feature_importance = {}
    
    # Build results
    results = []
    for idx, (_, row) in enumerate(features_df.iterrows()):
        test_id = row['test_id']
        
        # Get probability of being flaky
        if probabilities.shape[1] == 2:
            flaky_prob = probabilities[idx][1]
        else:
            flaky_prob = 0.5
        
        # Determine classification
        pred_label = predictions[idx]
        
        # Get top features for this test
        test_features = {}
        for feat in feature_cols[:5]:  # Top 5 features
            test_features[feat] = float(row[feat]) if pd.notna(row[feat]) else 0
        
        # Generate recommendations
        recommendations = _generate_recommendations(row, pred_label)
        
        result = {
            'test_id': test_id,
            'prediction': pred_label,
            'flakiness_score': float(flaky_prob),
            'confidence': float(max(probabilities[idx])),
            'execution_count': int(row['execution_count']),
            'failure_rate': float(row['failure_rate']),
            'transition_rate': float(row['transition_rate']),
            'features': test_features,
            'recommendations': recommendations
        }
        results.append(result)
    
    # Sort by flakiness score
    results.sort(key=lambda x: x['flakiness_score'], reverse=True)
    
    # Summary statistics
    summary = {
        'total_tests': len(results),
        'flaky_tests': sum(1 for r in results if r['prediction'] == 'FLAKY'),
        'stable_tests': sum(1 for r in results if r['prediction'] == 'NOT_FLAKY'),
        'insufficient_data': sum(1 for r in results if r['prediction'] == 'INSUFFICIENT_DATA'),
        'model_type': model_type,
        'feature_importance': dict(sorted(
            feature_importance.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:10]) if feature_importance else {}
    }
    
    return {
        'summary': summary,
        'predictions': results
    }


def _generate_recommendations(row: pd.Series, prediction: str) -> List[dict]:
    """Generate investigation recommendations."""
    recommendations = []
    
    if prediction == 'INSUFFICIENT_DATA':
        recommendations.append({
            'priority': 'MEDIUM',
            'message': 'Insufficient execution history. Need more test runs.',
            'action': 'Run the test more times to gather data'
        })
    elif prediction == 'FLAKY':
        failure_rate = row.get('failure_rate', 0)
        transition_rate = row.get('transition_rate', 0)
        
        if transition_rate > 0.3:
            recommendations.append({
                'priority': 'HIGH',
                'message': f'High outcome variability (transition rate: {transition_rate:.2%})',
                'action': 'Check for non-deterministic behavior, race conditions, or timing dependencies'
            })
        
        if row.get('duration_variability', 0) > 0.5:
            recommendations.append({
                'priority': 'MEDIUM',
                'message': 'High execution time variability',
                'action': 'Investigate timeouts, resource contention, or external dependencies'
            })
        
        if row.get('environment_count', 1) > 1 and failure_rate > 0.1:
            recommendations.append({
                'priority': 'MEDIUM',
                'message': 'Test runs in multiple environments',
                'action': 'Check for environment-specific failures'
            })
        
        if row.get('error_diversity', 0) > 2:
            recommendations.append({
                'priority': 'LOW',
                'message': 'Multiple different error messages',
                'action': 'Review error patterns for common root causes'
            })
    
    return recommendations


@router.get("/test/{test_id}")
async def get_test_analysis(
    test_id: str,
    dataset_id: int,
    db: Session = Depends(get_db)
):
    """Get detailed analysis for a specific test."""
    
    # Get test executions
    executions = db.query(TestExecution).filter(
        TestExecution.dataset_id == dataset_id,
        TestExecution.test_id == test_id
    ).order_by(TestExecution.timestamp).all()
    
    if not executions:
        raise HTTPException(status_code=404, detail="Test not found")
    
    # Build execution timeline
    timeline = []
    for exec in executions:
        timeline.append({
            'timestamp': exec.timestamp.isoformat(),
            'outcome': exec.outcome,
            'duration': exec.duration,
            'retry_count': exec.retry_count,
            'error_message': exec.error_message,
            'environment': exec.environment
        })
    
    # Calculate statistics
    total = len(executions)
    failures = sum(1 for e in executions if e.outcome == 'FAILED')
    passes = sum(1 for e in executions if e.outcome == 'PASSED')
    
    # Detect transitions
    transitions = 0
    for i in range(1, len(executions)):
        if executions[i].outcome != executions[i-1].outcome:
            transitions += 1
    
    return {
        'test_id': test_id,
        'total_executions': total,
        'pass_count': passes,
        'fail_count': failures,
        'failure_rate': failures / total if total > 0 else 0,
        'transition_rate': transitions / (total - 1) if total > 1 else 0,
        'timeline': timeline
    }
