"""Test execution schemas."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TestExecutionCreate(BaseModel):
    """Test execution creation request."""
    
    project_id: Optional[str] = None
    test_id: str = Field(..., min_length=1)
    execution_id: str = Field(..., min_length=1)
    timestamp: datetime
    outcome: str = Field(..., pattern="^(PASSED|FAILED|SKIPPED|ERROR)$")
    duration: Optional[float] = Field(None, ge=0)
    retry_count: Optional[int] = Field(0, ge=0)
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None
    environment: Optional[str] = None
    commit_hash: Optional[str] = None
    branch: Optional[str] = None
    changed_files: Optional[int] = Field(None, ge=0)
    runner_id: Optional[str] = None
    is_flaky_label: Optional[str] = Field(None, pattern="^(FLAKY|NOT_FLAKY|UNKNOWN)$")
    label_source: Optional[str] = None


class TestExecutionResponse(BaseModel):
    """Test execution response."""
    
    id: int
    dataset_id: int
    project_id: Optional[str]
    test_id: str
    execution_id: str
    timestamp: datetime
    outcome: str
    duration: Optional[float]
    retry_count: int
    error_message: Optional[str]
    stack_trace: Optional[str]
    environment: Optional[str]
    commit_hash: Optional[str]
    branch: Optional[str]
    changed_files: Optional[int]
    runner_id: Optional[str]
    is_flaky_label: Optional[str]
    label_source: Optional[str]
    
    model_config = {"from_attributes": True}
