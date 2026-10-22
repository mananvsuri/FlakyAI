# FlakeGuard AI API Documentation

**Base URL:** `http://localhost:8000/api/v1`

**Interactive Documentation:** `http://localhost:8000/docs` (Swagger UI)

---

## Authentication

Currently, no authentication is required. For production deployment, implement appropriate authentication and authorization.

---

## Endpoints

### Health Check

#### GET /health

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

---

## Datasets

### Upload Dataset

#### POST /api/v1/datasets/upload

Upload a dataset file (CSV, JSON, or JUnit XML).

**Request:**
- Content-Type: `multipart/form-data`
- Body:
  - `file`: Dataset file
  - `name`: Dataset name
  - `description`: (Optional) Dataset description
  - `source`: (Optional) Data source
  - `is_synthetic`: (Optional) Boolean indicating synthetic data

**Response:**
```json
{
  "dataset_id": 1,
  "dataset_name": "my_tests",
  "num_records": 1500,
  "num_tests": 150,
  "num_executions": 1500,
  "is_synthetic": false,
  "warnings": [],
  "errors": []
}
```

**Errors:**
- 400: Invalid file format or schema errors
- 413: File too large
- 422: Validation error

---

### List Datasets

#### GET /api/v1/datasets

Get all datasets.

**Query Parameters:**
- `skip`: Offset (default: 0)
- `limit`: Max results (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "name": "my_tests",
    "description": "Test execution history",
    "source": "upload",
    "is_synthetic": false,
    "num_tests": 150,
    "num_executions": 1500,
    "num_projects": 5,
    "created_at": "2024-01-01T12:00:00Z"
  }
]
```

---

### Get Dataset

#### GET /api/v1/datasets/{dataset_id}

Get dataset details.

**Response:**
```json
{
  "id": 1,
  "name": "my_tests",
  "description": "Test execution history",
  "source": "upload",
  "is_synthetic": false,
  "num_tests": 150,
  "num_executions": 1500,
  "num_projects": 5,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:00:00Z"
}
```

---

### Get Test Executions

#### GET /api/v1/datasets/{dataset_id}/executions

Get test execution records.

**Query Parameters:**
- `test_id`: Filter by test ID
- `project_id`: Filter by project ID
- `outcome`: Filter by outcome (PASSED, FAILED, SKIPPED, ERROR)
- `skip`: Offset (default: 0)
- `limit`: Max results (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "dataset_id": 1,
    "project_id": "project_a",
    "test_id": "test_login_001",
    "execution_id": "exec_12345",
    "timestamp": "2024-01-01T12:00:00Z",
    "outcome": "FAILED",
    "duration": 2.5,
    "retry_count": 1,
    "error_message": "Timeout waiting for element",
    "environment": "staging"
  }
]
```

---

## Models

### Train Model

#### POST /api/v1/models/train

Train a new model.

**Request:**
```json
{
  "model_name": "rf_model_v1",
  "model_type": "random_forest",
  "dataset_id": 1,
  "config": {
    "n_estimators": 100,
    "max_depth": 10
  },
  "test_size": 0.2,
  "validation_size": 0.2,
  "use_chronological_split": true
}
```

**Model Types:**
- `baseline`: Rule-based baseline
- `logistic`: Logistic Regression
- `random_forest`: Random Forest
- `gradient_boosting`: Gradient Boosting

**Response:**
```json
{
  "model_id": 1,
  "model_name": "rf_model_v1",
  "model_type": "random_forest",
  "train_metrics": {
    "precision": 0.85,
    "recall": 0.80,
    "f1": 0.82,
    "pr_auc": 0.87
  },
  "val_metrics": {
    "precision": 0.82,
    "recall": 0.78,
    "f1": 0.80,
    "pr_auc": 0.85
  },
  "test_metrics": {
    "precision": 0.83,
    "recall": 0.79,
    "f1": 0.81,
    "pr_auc": 0.86
  },
  "training_duration_seconds": 45.3,
  "num_features": 25,
  "feature_names": ["failure_rate", "transition_rate", ...],
  "train_size": 600,
  "val_size": 200,
  "test_size": 200,
  "class_distribution": {
    "FLAKY": 150,
    "NOT_FLAKY": 850
  }
}
```

**Errors:**
- 400: Invalid configuration
- 404: Dataset not found
- 422: Validation error

---

### List Models

#### GET /api/v1/models

Get all trained models.

**Response:**
```json
[
  {
    "id": 1,
    "name": "rf_model_v1",
    "model_type": "random_forest",
    "version": "1.0",
    "is_active": true,
    "trained_at": "2024-01-01T12:00:00Z",
    "training_duration_seconds": 45.3,
    "metrics": {
      "test_precision": 0.83,
      "test_recall": 0.79,
      "test_f1": 0.81,
      "test_pr_auc": 0.86
    }
  }
]
```

---

### Get Model

#### GET /api/v1/models/{model_id}

Get model details.

**Response:**
```json
{
  "id": 1,
  "name": "rf_model_v1",
  "model_type": "random_forest",
  "version": "1.0",
  "is_active": true,
  "trained_at": "2024-01-01T12:00:00Z",
  "training_duration_seconds": 45.3,
  "metrics": {...},
  "training_config": {...},
  "feature_names": [...]
}
```

---

## Predictions

### Predict Tests

#### POST /api/v1/predictions/predict

Get predictions for tests.

**Request:**
```json
{
  "test_ids": ["test_login_001", "test_checkout_002"],
  "model_name": "rf_model_v1",
  "dataset_id": 1
}
```

**Response:**
```json
[
  {
    "test_id": "test_login_001",
    "project_id": "project_a",
    "predicted_label": "FLAKY",
    "confidence": 0.85,
    "flakiness_score": 0.72,
    "num_executions": 50,
    "failure_rate": 0.24,
    "transition_rate": 0.18,
    "explanation_method": "shap",
    "feature_contributions": [
      {
        "feature_name": "transition_rate",
        "value": 0.18,
        "contribution": 0.15,
        "description": "Rate of outcome changes between consecutive executions"
      },
      {
        "feature_name": "failure_rate",
        "value": 0.24,
        "contribution": 0.12,
        "description": "Proportion of failed executions"
      }
    ],
    "recommendations": [
      {
        "message": "Test shows intermittent failures. Investigate for race conditions or timing dependencies.",
        "priority": "HIGH",
        "evidence": {
          "failure_rate": 0.24,
          "transition_rate": 0.18,
          "consecutive_failures": 3
        },
        "action": "Review test code for async operations without proper waits"
      }
    ],
    "model_name": "rf_model_v1",
    "inference_time_ms": 12.5,
    "created_at": "2024-01-01T12:00:00Z",
    "warnings": []
  }
]
```

---

### Get Explanation

#### GET /api/v1/predictions/{test_id}/explain

Get detailed explanation for a test prediction.

**Query Parameters:**
- `model_name`: (Optional) Model to use
- `dataset_id`: (Optional) Dataset ID

**Response:**
```json
{
  "test_id": "test_login_001",
  "predicted_label": "FLAKY",
  "flakiness_score": 0.72,
  "feature_contributions": [...],
  "explanation_method": "shap",
  "observation_window": {
    "start": "2024-01-01T00:00:00Z",
    "end": "2024-01-31T23:59:59Z",
    "num_executions": 50
  },
  "data_sufficiency": "SUFFICIENT",
  "num_executions": 50,
  "historical_outcomes": ["PASSED", "FAILED", "PASSED", ...],
  "recent_failure_rate": 0.30
}
```

---

## Analysis

### Get Recommendations

#### GET /api/v1/analysis/recommendations/{test_id}

Get investigation recommendations for a test.

**Query Parameters:**
- `dataset_id`: Dataset ID

**Response:**
```json
{
  "test_id": "test_login_001",
  "recommendations": [
    {
      "message": "Test shows intermittent failures across multiple environments",
      "priority": "HIGH",
      "evidence": {
        "failure_rate": 0.24,
        "environment_count": 3,
        "failure_correlation": 0.15
      },
      "action": "Check for environment-independent issues like race conditions"
    }
  ]
}
```

---

### Get Failure Patterns

#### GET /api/v1/analysis/patterns/{test_id}

Analyze failure patterns for a test.

**Response:**
```json
{
  "test_id": "test_login_001",
  "patterns": {
    "temporal": {
      "time_of_day_correlation": 0.25,
      "day_of_week_correlation": 0.10
    },
    "environmental": {
      "environment_specific": false,
      "failure_by_environment": {
        "staging": 0.30,
        "production": 0.20
      }
    },
    "error_patterns": {
      "most_common_error": "Timeout",
      "error_frequency": 0.60,
      "error_diversity": 3
    }
  }
}
```

---

## Experiments

### Run Experiment

#### POST /api/v1/experiments/run

Run an experimental evaluation.

**Request:**
```json
{
  "name": "baseline_comparison_exp1",
  "experiment_type": "baseline_comparison",
  "description": "Compare all models",
  "config": {
    "models": ["baseline", "logistic", "random_forest", "gradient_boosting"],
    "dataset_id": 1
  },
  "dataset_id": 1
}
```

**Experiment Types:**
- `baseline_comparison`
- `feature_ablation`
- `data_sufficiency`
- `generalization`
- `explainability_eval`
- `runtime_analysis`

**Response:**
```json
{
  "id": 1,
  "name": "baseline_comparison_exp1",
  "experiment_type": "baseline_comparison",
  "status": "running",
  "started_at": "2024-01-01T12:00:00Z"
}
```

---

### List Experiments

#### GET /api/v1/experiments

Get all experiments.

**Response:**
```json
[
  {
    "id": 1,
    "name": "baseline_comparison_exp1",
    "experiment_type": "baseline_comparison",
    "status": "completed",
    "started_at": "2024-01-01T12:00:00Z",
    "completed_at": "2024-01-01T12:15:00Z",
    "duration_seconds": 900,
    "results": {...},
    "metrics": {...}
  }
]
```

---

### Get Experiment

#### GET /api/v1/experiments/{experiment_id}

Get experiment details and results.

**Response:**
```json
{
  "id": 1,
  "name": "baseline_comparison_exp1",
  "experiment_type": "baseline_comparison",
  "description": "Compare all models",
  "config": {...},
  "status": "completed",
  "started_at": "2024-01-01T12:00:00Z",
  "completed_at": "2024-01-01T12:15:00Z",
  "duration_seconds": 900,
  "results": {
    "models": {
      "baseline": {
        "precision": 0.75,
        "recall": 0.70,
        "f1": 0.72,
        "pr_auc": 0.76
      },
      "logistic": {
        "precision": 0.80,
        "recall": 0.75,
        "f1": 0.77,
        "pr_auc": 0.82
      },
      "random_forest": {
        "precision": 0.83,
        "recall": 0.79,
        "f1": 0.81,
        "pr_auc": 0.86
      }
    }
  },
  "output_dir": "experiments/baseline_comparison_exp1"
}
```

---

## Export

### Export Metrics

#### GET /api/v1/export/metrics

Export metrics as CSV or JSON.

**Query Parameters:**
- `format`: `csv` or `json` (default: json)
- `experiment_id`: (Optional) Specific experiment

**Response:**
- Content-Type: `application/json` or `text/csv`
- Downloads file

---

### Export Predictions

#### GET /api/v1/export/predictions

Export predictions as CSV or JSON.

**Query Parameters:**
- `format`: `csv` or `json` (default: json)
- `dataset_id`: Dataset ID
- `model_name`: (Optional) Specific model

**Response:**
- Downloads file with predictions

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

**HTTP Status Codes:**
- 200: Success
- 201: Created
- 400: Bad Request
- 404: Not Found
- 413: Payload Too Large
- 422: Validation Error
- 500: Internal Server Error

---

## Rate Limiting

Currently, no rate limiting is implemented. For production, implement appropriate rate limiting based on usage patterns.

---

## Pagination

List endpoints support pagination:
- `skip`: Number of records to skip
- `limit`: Maximum records to return (max: 1000)

---

## Timestamps

All timestamps are in ISO 8601 format with UTC timezone:
```
2024-01-01T12:00:00Z
```

---

**Last Updated:** 2024  
**API Version:** 1.0.0
