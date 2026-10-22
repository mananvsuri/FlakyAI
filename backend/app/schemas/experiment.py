"""Experiment schemas."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel


class ExperimentCreate(BaseModel):
    """Experiment creation request."""
    
    name: str
    experiment_type: str
    description: Optional[str] = None
    config: Dict[str, Any] = {}
    dataset_id: Optional[int] = None


class ExperimentResponse(BaseModel):
    """Experiment response."""
    
    id: int
    name: str
    experiment_type: str
    description: Optional[str]
    config: Dict[str, Any]
    results: Optional[Dict[str, Any]]
    metrics: Optional[Dict[str, Any]]
    status: str
    started_at: datetime
    completed_at: Optional[datetime]
    duration_seconds: Optional[int]
    output_dir: Optional[str]
    
    model_config = {"from_attributes": True}
