"""Dataset model."""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func

from app.core.database import Base


class Dataset(Base):
    """Dataset metadata."""
    
    __tablename__ = "datasets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    
    # Provenance
    source = Column(String)  # e.g., "upload", "synthetic", "github"
    source_url = Column(String)
    license_info = Column(String)
    
    # Dataset characteristics
    is_synthetic = Column(Boolean, default=False)
    num_tests = Column(Integer)
    num_executions = Column(Integer)
    num_projects = Column(Integer)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # File reference
    file_path = Column(String)
