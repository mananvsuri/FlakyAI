"""Experiment tracking model."""

from sqlalchemy import Column, Integer, String, DateTime, JSON, Text
from sqlalchemy.sql import func

from app.core.database import Base


class Experiment(Base):
    """Experimental evaluation record."""
    
    __tablename__ = "experiments"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Experiment identification
    name = Column(String, nullable=False)
    experiment_type = Column(String, nullable=False)  # baseline_comparison, feature_ablation, etc.
    description = Column(Text)
    
    # Configuration
    config = Column(JSON)
    
    # Results
    results = Column(JSON)
    metrics = Column(JSON)
    
    # Dataset reference
    dataset_id = Column(Integer)
    
    # Timestamps
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Integer)
    
    # Status
    status = Column(String, default="pending")  # pending, running, completed, failed
    
    # Output files
    output_dir = Column(String)
