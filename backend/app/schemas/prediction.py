"""Prediction schemas."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Prediction request."""
    
    test_ids: list[str] = Field(..., min_length=1)
    model_name: Optional[str] = None
    dataset_id: Optional[int] = None


class FeatureContribution(BaseModel):
    """Feature contribution to prediction."""
    
    feature_name: str
    value: float
    contribution: float
    description: str


class Recommendation(BaseModel):
    """Investigation recommendation."""
    
    message: str
    priority: str  # HIGH, MEDIUM, LOW
    evidence: Dict[str, Any]
    action: str


class PredictionResponse(BaseModel):
    """Prediction response."""
    
    test_id: str
    project_id: Optional[str]
    predicted_label: str
    confidence: float = Field(..., ge=0, le=1)
    flakiness_score: float = Field(..., ge=0, le=1)
    
    # Evidence
    num_executions: int
    failure_rate: Optional[float]
    transition_rate: Optional[float]
    
    # Explanation
    explanation_method: str
    feature_contributions: list[FeatureContribution]
    
    # Recommendation
    recommendations: list[Recommendation]
    
    # Metadata
    model_name: str
    inference_time_ms: float
    created_at: datetime
    
    # Warnings
    warnings: list[str] = []


class ExplanationResponse(BaseModel):
    """Detailed explanation for a prediction."""
    
    test_id: str
    predicted_label: str
    flakiness_score: float
    
    # Feature importance
    feature_contributions: list[FeatureContribution]
    explanation_method: str
    
    # Observed data
    observation_window: Dict[str, Any]
    data_sufficiency: str  # SUFFICIENT, PARTIAL, INSUFFICIENT
    
    # Context
    num_executions: int
    historical_outcomes: list[str]
    recent_failure_rate: Optional[float]
