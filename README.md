# FlakeGuard AI

**An Explainable AI Framework for Flaky Test Detection, Failure Prediction, and Root Cause Analysis in CI/CD Pipelines**

A comprehensive academic research project for Software Quality and Testing Assurance.

## Project Overview

FlakeGuard AI is an ML-powered framework that analyzes historical test execution data to:
- Identify potentially flaky tests
- Distinguish flaky tests from persistent failures and stable tests
- Provide explainable predictions using SHAP
- Generate evidence-based investigation recommendations
- Support reproducible academic research on flaky test detection

## Research Questions

- **RQ1**: How effectively can ML identify flaky tests compared with baselines?
- **RQ2**: Which execution-history features contribute most to flakiness prediction?
- **RQ3**: Can explainable AI provide useful, evidence-supported explanations?
- **RQ4**: What trade-offs exist between accuracy, false-positives, and data requirements?
- **RQ5**: How effectively can the framework distinguish failure types?

## Technology Stack

**Backend:**
- Python 3.10+
- FastAPI
- SQLAlchemy + SQLite
- scikit-learn, pandas, NumPy
- SHAP for explainability
- Joblib for model serialization

**Frontend:**
- React 18 + TypeScript
- Vite
- Tailwind CSS
- Recharts for visualizations
- Lucide icons

**Testing:**
- pytest + pytest-cov
- Vitest + React Testing Library
- Playwright (optional e2e)

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI endpoints
│   │   ├── core/         # Configuration, database
│   │   ├── models/       # SQLAlchemy models
│   │   ├── ml/           # ML pipeline, features, training
│   │   ├── schemas/      # Pydantic schemas
│   │   └── utils/        # Utilities
│   ├── tests/            # Backend tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Main pages
│   │   ├── api/          # API client
│   │   └── utils/        # Utilities
│   ├── tests/            # Frontend tests
│   └── package.json
├── datasets/             # Dataset files
├── models/               # Trained models
├── experiments/          # Experiment results
├── docs/                 # Documentation
├── term_paper.md         # Academic paper (Markdown)
├── term_paper.docx       # Academic paper (Word)
├── references_audit.md   # Citation verification
└── docker-compose.yml    # Docker setup
```

## Installation

### Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -m app.core.init_db

# Run backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

## Quick Start

1. **Start the backend:**
   ```bash
   cd backend && source venv/bin/activate && uvicorn app.main:app --reload
   ```

2. **Start the frontend** (in another terminal):
   ```bash
   cd frontend && npm run dev
   ```

3. **Upload a dataset:**
   - Navigate to Dataset Management page
   - Upload CSV, JSON, or JUnit XML file
   - Or use the provided synthetic dataset

4. **Train models:**
   - Go to Model Laboratory
   - Select model type and configuration
   - Click "Train Model"

5. **Analyze tests:**
   - View predictions in Test Explorer
   - Click any test for detailed analysis
   - Review explanations in Explainability Centre

## Dataset Format

The system expects test execution records with these fields:

**Required:**
- `test_id`: Unique test identifier
- `execution_id`: Unique execution identifier
- `timestamp`: ISO 8601 timestamp
- `outcome`: PASSED, FAILED, SKIPPED, or ERROR

**Optional:**
- `project_id`: Project identifier
- `duration`: Execution duration (seconds)
- `retry_count`: Number of retries
- `error_message`: Failure message
- `stack_trace`: Stack trace
- `environment`: Execution environment
- `commit_hash`: Git commit
- `branch`: Git branch
- `changed_files`: Changed file count
- `runner_id`: CI runner identifier

### Example CSV Format

```csv
test_id,execution_id,timestamp,outcome,duration,retry_count,error_message
test_login_001,exec_1,2024-01-01T10:00:00Z,PASSED,1.2,0,
test_login_001,exec_2,2024-01-01T11:00:00Z,FAILED,2.5,1,Timeout
test_login_001,exec_3,2024-01-01T12:00:00Z,PASSED,1.1,0,
```

## Running Tests

### Backend Tests

```bash
cd backend
source venv/bin/activate
pytest tests/ -v --cov=app --cov-report=html
```

Coverage report will be in `backend/htmlcov/index.html`

### Frontend Tests

```bash
cd frontend
npm run test
```

### End-to-End Tests (optional)

```bash
cd frontend
npm run test:e2e
```

## Running Experiments

The experimental evaluation answers RQ1-RQ5 through six experiments:

```bash
cd backend
source venv/bin/activate

# Run all experiments
python -m app.ml.experiments.run_all

# Or run individual experiments
python -m app.ml.experiments.baseline_comparison
python -m app.ml.experiments.feature_ablation
python -m app.ml.experiments.data_sufficiency
python -m app.ml.experiments.generalization
python -m app.ml.experiments.explainability_eval
python -m app.ml.experiments.runtime_analysis
```

Results are saved to `experiments/` directory in JSON and CSV formats.

## Docker Deployment

```bash
# Build and start all services
docker-compose up --build

# Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## API Documentation

Interactive API documentation is available at `/docs` when the backend is running.

Key endpoints:
- `POST /api/v1/datasets/upload` - Upload dataset
- `GET /api/v1/datasets` - List datasets
- `POST /api/v1/models/train` - Train model
- `POST /api/v1/predictions/predict` - Get predictions
- `GET /api/v1/predictions/{test_id}/explain` - Get explanation
- `GET /api/v1/analysis/recommendations/{test_id}` - Get recommendations

## Dataset Sources

### Real Datasets

The project supports publicly available flaky test datasets:

1. **Google Flaky Test Dataset**: See `docs/dataset_sources.md` for details
2. **GitHub CI Test Histories**: Public repositories with historical test results

See `docs/dataset_acquisition.md` for complete documentation on:
- Dataset sources and licensing
- Download instructions
- Preprocessing steps
- Known limitations

### Synthetic Dataset

A synthetic dataset is provided for development and testing. It is clearly labeled as synthetic throughout the application. Do not use synthetic experimental results as evidence of real-world performance.

Generate synthetic data:
```bash
cd backend
python -m app.utils.generate_synthetic_data --num-tests 1000 --num-executions 10000
```

## Model Training

The system implements multiple models:

1. **Rule-based Baseline**: Statistical outcome inconsistency
2. **Logistic Regression**: Linear baseline
3. **Random Forest**: Ensemble method
4. **Gradient Boosting**: HistGradientBoosting or XGBoost

Models are trained with:
- Chronological train/validation/test splits
- Fixed random seeds for reproducibility
- Class weight handling for imbalanced data
- Model serialization with Joblib

## Feature Engineering

Features computed from historical execution data:
- Historical failure rate (various windows)
- Outcome transition rate
- Consecutive pass/fail counts
- Recent failure frequency
- Duration statistics and variability
- Retry frequency
- Error pattern categories
- Environment change indicators
- Missing data indicators

All features use only past information to prevent leakage.

## Explainability

The system provides:
- **Individual explanations**: SHAP values showing feature contributions
- **Global explanations**: Feature importance across all predictions
- **Evidence linking**: Observed data supporting each feature
- **Confidence indicators**: Data sufficiency warnings
- **Method disclosure**: Explanation approach documented

## Troubleshooting

### Backend won't start
- Verify Python 3.10+ is installed: `python --version`
- Check virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
- Check port 8000 is not in use: `lsof -i :8000`

### Frontend won't start
- Verify Node.js 18+ is installed: `node --version`
- Clear node_modules: `rm -rf node_modules && npm install`
- Check port 5173 is not in use

### Database issues
- Delete and reinitialize: `rm backend/flakeguard.db && python -m app.core.init_db`

### Model training fails
- Check dataset is loaded: `curl http://localhost:8000/api/v1/datasets`
- Verify sufficient data (min 100 test records recommended)
- Check logs for specific errors

### Tests failing
- Update dependencies: `pip install -r requirements.txt --upgrade`
- Clear pytest cache: `pytest --cache-clear`

## Academic Paper

The complete research paper is available in:
- `term_paper.md` (Markdown source)
- `term_paper.docx` (Word document)

The paper includes:
- Literature review with verified scholarly sources
- Detailed methodology
- Experimental results (populated after running experiments)
- Discussion and limitations
- IEEE-style references

See `references_audit.md` for citation verification details.

## Contributing

This is an academic research project. For questions or issues:
1. Check existing documentation
2. Review API documentation at `/docs`
3. Check test suite for usage examples

## License

This project is created for academic purposes as part of a Software Quality and Testing Assurance course.

## Citation

If you use this work in academic research, please cite:

```
[Student Name]. (2024). An Explainable AI Framework for Flaky Test Detection, 
Failure Prediction, and Root Cause Analysis in CI/CD Pipelines. 
Software Quality and Testing Assurance Course Project.
```

## Acknowledgments

- Course: Software Quality and Testing Assurance
- Topic 39: AI-Based Detection of Flaky Tests in CI/CD Pipelines
- Datasets: See `docs/dataset_acquisition.md` for data source acknowledgments

## Project Status

- ✅ Backend API implementation
- ✅ ML pipeline with multiple models
- ✅ SHAP-based explainability
- ✅ React frontend with 7 functional pages
- ✅ Comprehensive test suite
- ✅ Experimental evaluation framework
- ✅ Academic paper with literature review
- 📊 Results pending experimental runs

---

**Project Name:** FlakeGuard AI  
**Version:** 1.0.0  
**Last Updated:** 2024
