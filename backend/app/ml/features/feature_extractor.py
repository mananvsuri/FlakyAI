"""Feature extraction from test execution history."""

import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime


class FeatureExtractor:
    """Extract features from test execution history for flakiness prediction."""
    
    def extract_features(self, executions: pd.DataFrame) -> pd.DataFrame:
        """Extract features for each test from execution history.
        
        Args:
            executions: DataFrame with columns: test_id, timestamp, outcome, duration, etc.
        
        Returns:
            DataFrame with one row per test and feature columns
        """
        # Sort by timestamp to ensure chronological order
        executions = executions.sort_values('timestamp')
        
        features_list = []
        
        for test_id, test_data in executions.groupby('test_id'):
            features = self._extract_test_features(test_id, test_data)
            features_list.append(features)
        
        df = pd.DataFrame(features_list)
        
        # Fill NaN values with 0 (sklearn models don't accept NaN)
        df = df.fillna(0)
        
        return df
    
    def _extract_test_features(self, test_id: str, test_data: pd.DataFrame) -> Dict:
        """Extract features for a single test."""
        
        features = {'test_id': test_id}
        
        # Basic counts
        features['execution_count'] = len(test_data)
        
        # Outcome features
        outcomes = test_data['outcome'].value_counts()
        total = len(test_data)
        
        features['failure_rate'] = outcomes.get('FAILED', 0) / total
        features['pass_rate'] = outcomes.get('PASSED', 0) / total
        features['error_rate'] = outcomes.get('ERROR', 0) / total
        features['skip_rate'] = outcomes.get('SKIPPED', 0) / total
        
        # Transition rate (outcome changes)
        transitions = (test_data['outcome'] != test_data['outcome'].shift()).sum() - 1
        features['transition_rate'] = transitions / max(total - 1, 1)
        
        # Consecutive sequences
        features['max_consecutive_failures'] = self._max_consecutive(test_data['outcome'], 'FAILED')
        features['max_consecutive_passes'] = self._max_consecutive(test_data['outcome'], 'PASSED')
        
        # Recent failure rate (last 20% of executions)
        recent_count = max(int(total * 0.2), 1)
        recent = test_data.tail(recent_count)
        features['recent_failure_rate'] = (recent['outcome'] == 'FAILED').sum() / recent_count
        
        # Duration features
        if 'duration' in test_data.columns and test_data['duration'].notna().any():
            durations = test_data['duration'].dropna()
            features['mean_duration'] = durations.mean()
            features['duration_std'] = durations.std() if len(durations) > 1 else 0
            features['duration_variability'] = durations.std() / durations.mean() if durations.mean() > 0 else 0
        else:
            features['mean_duration'] = 0
            features['duration_std'] = 0
            features['duration_variability'] = 0
        
        # Retry features
        if 'retry_count' in test_data.columns:
            features['retry_rate'] = (test_data['retry_count'] > 0).sum() / total
            features['mean_retry_count'] = test_data['retry_count'].mean()
        else:
            features['retry_rate'] = 0
            features['mean_retry_count'] = 0
        
        # Environment diversity
        if 'environment' in test_data.columns and test_data['environment'].notna().any():
            features['environment_count'] = test_data['environment'].nunique()
        else:
            features['environment_count'] = 1
        
        # Error diversity
        if 'error_message' in test_data.columns:
            error_messages = test_data[test_data['error_message'].notna()]['error_message']
            features['error_diversity'] = error_messages.nunique() if len(error_messages) > 0 else 0
        else:
            features['error_diversity'] = 0
        
        # Outcome entropy (measure of randomness)
        features['outcome_entropy'] = self._entropy(outcomes.values / total)
        
        # Ground truth label if available
        if 'is_flaky_label' in test_data.columns:
            # Use most common label
            label = test_data['is_flaky_label'].mode()
            features['label'] = label[0] if len(label) > 0 else 'UNKNOWN'
        else:
            features['label'] = 'UNKNOWN'
        
        return features
    
    def _max_consecutive(self, series: pd.Series, value: str) -> int:
        """Calculate maximum consecutive occurrences of a value."""
        max_count = 0
        current_count = 0
        
        for item in series:
            if item == value:
                current_count += 1
                max_count = max(max_count, current_count)
            else:
                current_count = 0
        
        return max_count
    
    def _entropy(self, probabilities: np.ndarray) -> float:
        """Calculate Shannon entropy."""
        probabilities = probabilities[probabilities > 0]
        return -np.sum(probabilities * np.log2(probabilities))
