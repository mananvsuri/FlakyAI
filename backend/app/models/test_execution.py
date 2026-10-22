"""Test execution model."""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class TestExecution(Base):
    """Individual test execution record."""
    
    __tablename__ = "test_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    dataset_id = Column(Integer, ForeignKey("datasets.id"), nullable=False)
    
    # Identifiers
    project_id = Column(String, index=True)
    test_id = Column(String, index=True, nullable=False)
    execution_id = Column(String, index=True, nullable=False)
    
    # Execution details
    timestamp = Column(DateTime(timezone=True), nullable=False)
    outcome = Column(String, nullable=False)  # PASSED, FAILED, SKIPPED, ERROR
    duration = Column(Float)  # seconds
    retry_count = Column(Integer, default=0)
    
    # Error information
    error_message = Column(Text)
    stack_trace = Column(Text)
    
    # Context
    environment = Column(String)
    commit_hash = Column(String)
    branch = Column(String)
    changed_files = Column(Integer)
    runner_id = Column(String)
    
    # Ground truth label (if available)
    is_flaky_label = Column(String)  # FLAKY, NOT_FLAKY, UNKNOWN
    label_source = Column(String)  # e.g., "manual", "inferred", "dataset"
    
    # Relationships
    dataset = relationship("Dataset")
