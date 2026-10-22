"""Dataset schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class DatasetCreate(BaseModel):
    """Dataset creation request."""
    
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    source: str = Field(default="upload")
    source_url: Optional[str] = None
    license_info: Optional[str] = None
    is_synthetic: bool = False


class DatasetResponse(BaseModel):
    """Dataset response."""
    
    id: int
    name: str
    description: Optional[str]
    source: str
    source_url: Optional[str]
    license_info: Optional[str]
    is_synthetic: bool
    num_tests: Optional[int]
    num_executions: Optional[int]
    num_projects: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime]
    
    model_config = {"from_attributes": True}


class DatasetUploadResponse(BaseModel):
    """Dataset upload response."""
    
    dataset_id: int
    dataset_name: str
    num_records: int
    num_tests: int
    num_executions: int
    is_synthetic: bool
    warnings: list[str] = []
    errors: list[str] = []
