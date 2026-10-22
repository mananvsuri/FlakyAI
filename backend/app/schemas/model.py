"""Model schemas."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class ModelTrainRequest(BaseModel):
    """Model training request."""
    
    model_type: str = Field(..., pattern="^(baseline|logistic|random_forest|gradient_boosting)$")
    model_name: str = Field(..., min_length=1)
    dataset_id: int = Field(..., gt=0)
    
    # Training configuration
    config: Dict[str, Any] = {}
    
    # Data split
    test_size: float = Field(0.2, ge=0.1, le=0.5)
    validation_size: float = Field(0.2, ge=0.1, le=0.5)
    use_chronological_split: bool = True


class ModelTrainResponse(BaseModel):
    """Model training response."""
    
    model_id: int
    model_name: str
    model_type: str
    
    # Training metrics
    train_metrics: Dict[str, float]
    val_metrics: Dict[str, float]
    test_metrics: Dict[str, float]
    
    # Training info
    training_duration_seconds: float
    num_features: int
    feature_names: list[str]
    
    # Dataset info
    train_size: int
    val_size: int
    test_size: int
    class_distribution: Dict[str, int]


class ModelInfo(BaseModel):
    """Model information."""
    
    id: int
    name: str
    model_type: str
    version: Optional[str]
    is_active: bool
    trained_at: datetime
    training_duration_seconds: Optional[float]
    metrics: Optional[Dict[str, Any]]
    
    model_config = {"from_attributes": True}
