# FlakeGuard AI - Quick Start Guide

Get FlakeGuard AI running in minutes.

## Prerequisites

- Python 3.10 or higher
- Node.js 18 or higher
- Git

## Installation

### 1. Clone and Navigate

```bash
cd /Users/manan/Desktop/SQTA/Innovative
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from app.core.database import init_db; init_db()"
```

### 3. Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install
```

## Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000  
API docs at: http://localhost:8000/docs

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend will be available at: http://localhost:5173

## First Steps

### 1. Check Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "version": "1.0.0"}
```

### 2. Generate Synthetic Data (Optional)

```bash
cd backend
python -m app.utils.generate_synthetic_data --num-tests 150 --num-executions 1500
```

### 3. Upload Dataset

Visit http://localhost:5173 and:
1. Navigate to "Dataset Management"
2. Upload the generated `synthetic_test_data.csv`
3. Or upload your own dataset (CSV, JSON, or JUnit XML)

### 4. Train a Model

1. Navigate to "Model Laboratory"
2. Select model type (e.g., "Random Forest")
3. Select the uploaded dataset
4. Click "Train Model"
5. Wait for training to complete

### 5. View Predictions

1. Navigate to "Test Explorer"
2. Browse tests and their predictions
3. Click any test to see detailed analysis
4. View explanations in "Explainability Centre"

## Quick Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm run test
```

## Docker Quick Start (Alternative)

If you prefer Docker:

```bash
# Build and start all services
docker-compose up --build

# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Troubleshooting

### Backend won't start

**Error: "No module named 'app'"**
```bash
# Make sure you're in the backend directory
cd backend
# And virtual environment is activated
source venv/bin/activate
```

**Error: "Port 8000 already in use"**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
# Or use different port
uvicorn app.main:app --reload --port 8001
```

### Frontend won't start

**Error: "Cannot find module"**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Error: "Port 5173 already in use"**
```bash
# Vite will automatically try next available port
# Or kill process:
lsof -ti:5173 | xargs kill -9
```

### Database issues

**Error: "Table doesn't exist"**
```bash
cd backend
python -c "from app.core.database import init_db; init_db()"
```

**Error: "Database is locked"**
```bash
# Stop all running instances and try again
rm flakeguard.db  # This will delete all data
python -c "from app.core.database import init_db; init_db()"
```

## Next Steps

1. **Explore the Dashboard** - See system overview and metrics
2. **Analyze Tests** - Browse test execution histories
3. **Run Experiments** - Execute the six experimental evaluations
4. **Read Documentation** - Check `docs/` for detailed information
5. **Review Code** - Explore the implementation

## Common Tasks

### Generate More Synthetic Data

```bash
cd backend
python -m app.utils.generate_synthetic_data \
  --num-tests 500 \
  --num-executions 5000 \
  --flaky-ratio 0.20 \
  --output ../datasets/large_synthetic.csv
```

### Train Multiple Models

```bash
# Via API
for model in baseline logistic random_forest gradient_boosting; do
  curl -X POST "http://localhost:8000/api/v1/models/train" \
    -H "Content-Type: application/json" \
    -d "{
      \"model_name\": \"${model}_v1\",
      \"model_type\": \"${model}\",
      \"dataset_id\": 1
    }"
done
```

### Run All Experiments

```bash
cd backend
python -m app.ml.experiments.run_all
```

Results will be saved to `experiments/` directory.

### Export Results

```bash
# Export metrics as CSV
curl "http://localhost:8000/api/v1/export/metrics?format=csv" -o metrics.csv

# Export predictions
curl "http://localhost:8000/api/v1/export/predictions?dataset_id=1&format=csv" -o predictions.csv
```

## Development Mode

### Backend with Auto-Reload

```bash
cd backend
uvicorn app.main:app --reload
```

Changes to Python files will automatically reload the server.

### Frontend with Hot Module Replacement

```bash
cd frontend
npm run dev
```

Changes to React files will automatically update in the browser.

### Run Tests in Watch Mode

```bash
# Backend
cd backend
pytest-watch tests/

# Frontend
cd frontend
npm run test -- --watch
```

## Production Build

### Frontend Production Build

```bash
cd frontend
npm run build
```

Built files will be in `frontend/dist/`

### Backend Production

```bash
cd backend
pip install gunicorn
gunicorn app.main:app --workers 4 --bind 0.0.0.0:8000
```

## Additional Resources

- **Full README:** `README.md`
- **API Documentation:** `docs/api_documentation.md` or http://localhost:8000/docs
- **Dataset Guide:** `datasets/README.md`
- **Experiment Guide:** `experiments/README.md`
- **Project Status:** `PROJECT_STATUS.md`

## Support

For issues:
1. Check troubleshooting section above
2. Review relevant documentation in `docs/`
3. Check backend logs for error messages
4. Verify all prerequisites are installed

## Project Structure

```
.
├── backend/           # Python FastAPI backend
├── frontend/          # React TypeScript frontend
├── datasets/          # Test execution datasets
├── models/            # Trained ML models
├── experiments/       # Experiment results
├── docs/              # Documentation
└── term_paper.md      # Academic paper
```

---

**Ready to explore!** 🚀

Visit http://localhost:5173 to start using FlakeGuard AI.
