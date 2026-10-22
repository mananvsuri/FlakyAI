"""Flaky test detection models."""

import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from typing import Dict, Tuple
import joblib


class BaselineDetector:
    """Rule-based baseline for flaky test detection."""
    
    def __init__(self, failure_threshold: float = 0.1, transition_threshold: float = 0.2):
        self.failure_threshold = failure_threshold
        self.transition_threshold = transition_threshold
    
    def fit(self, X, y):
        """No training needed for baseline."""
        return self
    
    def predict(self, X):
        """Predict based on simple rules."""
        predictions = []
        
        for idx, row in X.iterrows():
            failure_rate = row.get('failure_rate', 0)
            transition_rate = row.get('transition_rate', 0)
            execution_count = row.get('execution_count', 0)
            
            # Insufficient data
            if execution_count < 5:
                predictions.append('INSUFFICIENT_DATA')
            # Flaky: some failures but not all, with transitions
            elif (failure_rate > self.failure_threshold and 
                  failure_rate < 0.9 and 
                  transition_rate > self.transition_threshold):
                predictions.append('FLAKY')
            # Persistent failure
            elif failure_rate >= 0.9:
                predictions.append('NOT_FLAKY')
            # Stable
            else:
                predictions.append('NOT_FLAKY')
        
        return np.array(predictions)
    
    def predict_proba(self, X):
        """Return dummy probabilities."""
        predictions = self.predict(X)
        probs = []
        for pred in predictions:
            if pred == 'FLAKY':
                probs.append([0.2, 0.8])  # [NOT_FLAKY, FLAKY]
            elif pred == 'INSUFFICIENT_DATA':
                probs.append([0.5, 0.5])
            else:
                probs.append([0.8, 0.2])
        return np.array(probs)


class MLFlakyDetector:
    """Machine learning-based flaky test detector."""
    
    def __init__(self, model_type: str = 'random_forest', **kwargs):
        self.model_type = model_type
        self.model = self._create_model(**kwargs)
        self.feature_names = None
    
    def _create_model(self, **kwargs):
        """Create the specified model."""
        if self.model_type == 'logistic':
            return LogisticRegression(
                random_state=42,
                max_iter=1000,
                class_weight='balanced',
                **kwargs
            )
        elif self.model_type == 'random_forest':
            return RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=10,
                class_weight='balanced',
                **kwargs
            )
        elif self.model_type == 'gradient_boosting':
            return GradientBoostingClassifier(
                n_estimators=100,
                random_state=42,
                max_depth=5,
                learning_rate=0.1,
                **kwargs
            )
        else:
            raise ValueError(f"Unknown model type: {self.model_type}")
    
    def fit(self, X, y):
        """Train the model."""
        # Store feature names
        if hasattr(X, 'columns'):
            self.feature_names = list(X.columns)
        
        # Convert labels to binary (FLAKY vs NOT_FLAKY)
        y_binary = (y == 'FLAKY').astype(int)
        
        self.model.fit(X, y_binary)
        return self
    
    def predict(self, X):
        """Predict flakiness."""
        # Handle insufficient data
        if hasattr(X, 'execution_count'):
            insufficient_mask = X['execution_count'] < 5
        else:
            insufficient_mask = X.iloc[:, 0] < 5  # Assume first column
        
        # Get predictions
        y_pred = self.model.predict(X)
        
        # Convert to labels
        labels = ['NOT_FLAKY' if p == 0 else 'FLAKY' for p in y_pred]
        
        # Mark insufficient data
        if hasattr(X, '__iter__'):
            for i, is_insufficient in enumerate(insufficient_mask):
                if is_insufficient:
                    labels[i] = 'INSUFFICIENT_DATA'
        
        return np.array(labels)
    
    def predict_proba(self, X):
        """Predict probabilities."""
        return self.model.predict_proba(X)
    
    def get_feature_importance(self) -> Dict[str, float]:
        """Get feature importances."""
        if hasattr(self.model, 'feature_importances_'):
            importances = self.model.feature_importances_
        elif hasattr(self.model, 'coef_'):
            importances = np.abs(self.model.coef_[0])
        else:
            return {}
        
        if self.feature_names:
            return dict(zip(self.feature_names, importances))
        return {}
    
    def save(self, path: str):
        """Save model to disk."""
        joblib.dump(self, path)
    
    @staticmethod
    def load(path: str):
        """Load model from disk."""
        return joblib.load(path)


def create_detector(model_type: str = 'random_forest', **kwargs):
    """Factory function to create a detector."""
    if model_type == 'baseline':
        return BaselineDetector(**kwargs)
    else:
        return MLFlakyDetector(model_type=model_type, **kwargs)
