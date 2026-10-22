"""ML model information model."""

from sqlalchemy import Column, Integer, String, DateTime, JSON, Float
from sqlalchemy.sql import func

from app.core.database import Base


class ModelInfo(Base):
    """Trained model metadata."""
    
    __tablename__ = "model_info"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Model identification
    name = Column(String, unique=True, nullable=False)
    model_type = Column(String, nullable=False)  # baseline, logistic, random_forest, gradient_boosting
    version = Column(String)
    
    # Training metadata
    dataset_id = Column(Integer)
    training_config = Column(JSON)
    
    # Performance metrics
    metrics = Column(JSON)  # precision, recall, f1, pr_auc, etc.
    
    # Model file
    model_path = Column(String)
    feature_names = Column(JSON)
    
    # Timestamps
    trained_at = Column(DateTime(timezone=True), server_default=func.now())
    training_duration_seconds = Column(Float)
    
    # Status
    is_active = Column(Integer, default=0)  # Boolean: 1 for active model
