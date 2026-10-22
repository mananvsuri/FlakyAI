"""Prediction model."""

from sqlalchemy import Column, Integer, String, DateTime, Float, JSON, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


class Prediction(Base):
    """ML model prediction for a test."""
    
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Model reference
    model_id = Column(Integer, ForeignKey("model_info.id"), nullable=False)
    
    # Test reference
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    test_id = Column(String, index=True, nullable=False)
    project_id = Column(String, index=True)
    
    # Prediction
    predicted_label = Column(String, nullable=False)  # FLAKY, NOT_FLAKY, INSUFFICIENT_DATA
    confidence = Column(Float)  # 0-1
    flakiness_score = Column(Float)  # 0-1, probability of being flaky
    
    # Explanation
    feature_importance = Column(JSON)  # SHAP values or feature contributions
    explanation_method = Column(String)  # e.g., "shap", "feature_importance"
    
    # Evidence
    num_executions = Column(Integer)
    failure_rate = Column(Float)
    transition_rate = Column(Float)
    
    # Recommendation
    recommendation = Column(String)
    recommendation_evidence = Column(JSON)
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    inference_time_ms = Column(Float)
