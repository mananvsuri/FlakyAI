"""Dataset API endpoints."""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from sqlalchemy.orm import Session
from typing import List
import csv
import io
from datetime import datetime

from app.core.database import get_db
from app.models.dataset import Dataset
from app.models.test_execution import TestExecution
from app.schemas.dataset import DatasetResponse, DatasetUploadResponse

router = APIRouter()


@router.post("/upload", response_model=DatasetUploadResponse)
async def upload_dataset(
    file: UploadFile = File(...),
    name: str = Form("uploaded_dataset"),
    db: Session = Depends(get_db)
):
    """Upload a dataset (CSV format)."""
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported currently")
    
    # Read file content
    content = await file.read()
    text_content = content.decode('utf-8')
    
    # Parse CSV
    csv_reader = csv.DictReader(io.StringIO(text_content))
    
    # Make name unique by checking if it exists
    base_name = name
    counter = 1
    while db.query(Dataset).filter(Dataset.name == name).first():
        name = f"{base_name}_{counter}"
        counter += 1
    
    # Create dataset record
    dataset = Dataset(
        name=name,
        source="upload",
        is_synthetic=False,
        created_at=datetime.utcnow()
    )
    db.add(dataset)
    db.flush()  # Get dataset ID
    
    # Parse and store executions
    executions = []
    test_ids = set()
    warnings = []
    errors = []
    
    for idx, row in enumerate(csv_reader):
        try:
            # Parse required fields
            test_id = row.get('test_id')
            execution_id = row.get('execution_id')
            timestamp_str = row.get('timestamp')
            outcome = row.get('outcome')
            
            if not all([test_id, execution_id, timestamp_str, outcome]):
                warnings.append(f"Row {idx+2}: Missing required fields")
                continue
            
            # Parse timestamp
            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            except:
                warnings.append(f"Row {idx+2}: Invalid timestamp format")
                continue
            
            # Validate outcome
            if outcome not in ['PASSED', 'FAILED', 'SKIPPED', 'ERROR']:
                warnings.append(f"Row {idx+2}: Invalid outcome '{outcome}'")
                continue
            
            # Parse optional fields
            duration = float(row.get('duration', 0)) if row.get('duration') else None
            retry_count = int(row.get('retry_count', 0)) if row.get('retry_count') else 0
            
            # Create execution record
            execution = TestExecution(
                dataset_id=dataset.id,
                project_id=row.get('project_id'),
                test_id=test_id,
                execution_id=execution_id,
                timestamp=timestamp,
                outcome=outcome,
                duration=duration,
                retry_count=retry_count,
                error_message=row.get('error_message'),
                stack_trace=row.get('stack_trace'),
                environment=row.get('environment'),
                commit_hash=row.get('commit_hash'),
                branch=row.get('branch'),
                changed_files=int(row.get('changed_files', 0)) if row.get('changed_files') else None,
                runner_id=row.get('runner_id'),
                is_flaky_label=row.get('is_flaky_label'),
                label_source=row.get('label_source')
            )
            
            executions.append(execution)
            test_ids.add(test_id)
            
        except Exception as e:
            errors.append(f"Row {idx+2}: {str(e)}")
    
    if not executions:
        db.rollback()
        raise HTTPException(status_code=400, detail="No valid executions found in file")
    
    # Bulk insert executions
    db.bulk_save_objects(executions)
    
    # Update dataset stats
    dataset.num_tests = len(test_ids)
    dataset.num_executions = len(executions)
    
    # Check if synthetic
    if any(exec.label_source == 'synthetic' for exec in executions):
        dataset.is_synthetic = True
    
    db.commit()
    db.refresh(dataset)
    
    return DatasetUploadResponse(
        dataset_id=dataset.id,
        dataset_name=dataset.name,
        num_records=len(executions),
        num_tests=dataset.num_tests,
        num_executions=dataset.num_executions,
        is_synthetic=dataset.is_synthetic,
        warnings=warnings[:10],  # Limit warnings
        errors=errors[:10]  # Limit errors
    )


@router.get("/", response_model=List[DatasetResponse])
def list_datasets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all datasets."""
    datasets = db.query(Dataset).offset(skip).limit(limit).all()
    return datasets


@router.get("/{dataset_id}", response_model=DatasetResponse)
def get_dataset(dataset_id: int, db: Session = Depends(get_db)):
    """Get dataset by ID."""
    dataset = db.query(Dataset).filter(Dataset.id == dataset_id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset
