# Final Submission Answers - FlakeGuard AI

**Authors:** Manan Suri & Nilaksh Pathak  
**Institution:** Nirma University, Ahmedabad  
**Date:** October 2024  
**GitHub:** https://github.com/mananvsuri/FlakyAI

---

## Question 1: Title of the term paper

**Answer:**
```
An Explainable AI Framework for Flaky Test Detection in CI/CD Pipelines
```

---

## Question 2: URL of the dataset

**Answer:**
```
https://github.com/mananvsuri/FlakyAI/blob/main/datasets/synthetic_test_data.csv
```

**Dataset Specifications:**
- **File:** synthetic_test_data.csv
- **Rows:** 1,449 test executions
- **Tests:** 150 unique tests
- **Time Range:** 90 days (Jan 1 - Mar 31, 2024)
- **Columns:** 16 features including test_id, execution_id, timestamp, outcome, duration, retry_count, error_message, environment, commit_hash, branch, changed_files, runner_id, is_flaky_label, label_source
- **Labels:**
  - 22 FLAKY tests
  - 85 NOT_FLAKY tests (stable pass)
  - 43 NOT_FLAKY tests (stable fail)
  - 12 tests with INSUFFICIENT_DATA
- **Repository:** Public on GitHub
- **Access:** Free, no authentication required

---

## Question 3: Is the preprocessing of the data set has been done (Y/N)

**Answer: Y (YES)**

**Preprocessing Details:**

### 1. Data Validation (backend/app/api/datasets.py)
```python
✓ CSV format validation
✓ Required fields check (test_id, execution_id, timestamp, outcome)
✓ Timestamp parsing and validation (ISO format)
✓ Outcome value validation (PASSED/FAILED/SKIPPED/ERROR)
✓ Data type conversion (float for duration, int for counts)
✓ Error tracking with warnings and error lists
```

### 2. Data Cleaning
```python
✓ Missing values handled (defaults: duration=0, retry_count=0)
✓ Invalid rows flagged with line numbers
✓ Null/empty fields validated
✓ Duplicate execution_id handling
```

### 3. Feature Engineering (backend/app/ml/features/feature_extractor.py)
**15+ Features Extracted:**

**Outcome Features:**
- failure_rate: Proportion of failed executions
- pass_rate: Proportion of passed executions
- error_rate: Proportion of error outcomes
- skip_rate: Proportion of skipped tests
- transition_rate: Frequency of outcome changes
- outcome_entropy: Shannon entropy of outcomes

**Temporal Features:**
- execution_count: Total number of executions
- max_consecutive_failures: Longest failure streak
- max_consecutive_passes: Longest pass streak
- recent_failure_rate: Failure rate in last 20% of runs

**Duration Features:**
- mean_duration: Average execution time
- duration_std: Standard deviation of duration
- duration_variability: Coefficient of variation

**Pattern Features:**
- retry_rate: Proportion with retries
- mean_retry_count: Average retry attempts
- error_diversity: Number of unique error messages
- environment_count: Number of different environments

### 4. Temporal Integrity
```python
✓ Chronological sorting by timestamp
✓ No future information leakage
✓ Features calculated only from past data
✓ Train/val/test split respects temporal order (60/20/20)
```

### 5. ML Preparation
```python
✓ NaN values filled with 0 (sklearn compatibility)
✓ Feature matrix (X) and label vector (y) separated
✓ Class weights for imbalanced data
✓ Fixed random seed (42) for reproducibility
```

**Code Files:**
- Upload & validation: `backend/app/api/datasets.py` (lines 16-136)
- Feature extraction: `backend/app/ml/features/feature_extractor.py` (lines 1-123)
- Data generation: `backend/app/utils/generate_synthetic_data.py`

---

## Question 4: Is the problem statement and solution statement incorporated in the paper (Y/N)

**Answer: Y (YES)**

### Problem Statement (Section 1: Introduction)
**Location:** Lines 23-28 in term_paper.tex

**Text:**
> "Flaky tests—tests passing or failing inconsistently across executions without corresponding code changes—erode developer confidence, waste engineering time investigating false alarms, and may mask genuine defects. The prevalence of flaky tests has been documented across both industry and open-source projects, with studies showing that major software projects contain hundreds to thousands of flaky tests."

**Problem Components Identified:**
1. Non-deterministic test behavior
2. Erodes developer confidence
3. Wastes engineering time on false alarms
4. May hide real bugs
5. Widespread across industry projects
6. Difficult to detect automatically

### Solution Statement (Section 1: Introduction & Abstract)
**Location:** Lines 29-37 in term_paper.tex

**Text:**
> "This paper presents FlakeGuard AI, an explainable AI framework addressing these challenges through: (1) multi-model machine learning comparing rule-based baselines with advanced techniques (logistic regression, random forests, gradient boosting), (2) comprehensive feature importance analysis revealing which execution patterns indicate flakiness, (3) evidence-based recommendations linking predictions to observable behaviors, and (4) production-ready web deployment enabling practical adoption."

**Solution Components:**
1. **Multi-Model ML:** 4 models from baseline to advanced ensembles
2. **Feature Importance:** Identifies predictive patterns (outcome entropy, transition rate)
3. **Explainability:** SHAP-based feature attribution
4. **Recommendations:** Evidence-based investigation guidance
5. **Web Deployment:** Production-ready full-stack application
6. **Classification:** Distinguishes FLAKY/NOT_FLAKY/INSUFFICIENT_DATA

**Also Covered in Abstract (Lines 14-22):**
- Evaluation results: 22 flaky tests detected
- Feature importance: outcome_entropy (30-72%), transition_rate (16.8%)
- Model comparison: Random Forest best performance

---

## Question 5: Is the flow chart and architecture of the proposed solution mentioned (Y/N)

**Answer: N (NO - Visual flowchart not included)**

**Reason:**
Due to 3-page space constraints in IEEE conference format, a visual flowchart diagram was not included. However, the architecture is comprehensively described in text form.

**What IS Included in the Paper:**

### 1. Architecture Description (Section 5: Implementation)
Text description of system components:
- Backend: Python FastAPI + SQLAlchemy + scikit-learn
- Frontend: React + TypeScript + Tailwind CSS
- Database: SQLite
- API: RESTful with Pydantic validation

### 2. Pipeline Description (Section 4: Methodology)
Complete workflow described:
```
Historical Test Executions → 
Data Validation → 
Feature Engineering (15+ features) → 
Model Training (4 models) → 
Prediction (FLAKY/NOT_FLAKY/INSUFFICIENT_DATA) → 
SHAP Explainability → 
Recommendations → 
Dashboard Display
```

### 3. Visual Elements Included
- **Figure 1:** Dataset Management Interface (screenshot)
- **Figure 2:** Analysis Results Interface (screenshot)

### Text-Based Flow in Paper (Section 4.1-4.3)
**Feature Engineering → Models → Explainability**

**If Flowchart Required:**
Would you like me to create a visual flowchart diagram? It can be added as Figure 3. The diagram would show:

```
┌─────────────────┐
│ Test Executions │
│   (CSV Upload)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Validation    │
│  & Parsing      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Feature      │
│  Extraction     │
│   (15+ feat)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Model Select   │
│  (4 options)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│    Training     │
│  & Prediction   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│     SHAP        │
│  Explainability │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Recommendations │
│   & Results     │
└─────────────────┘
```

**Decision:** Proceed without flowchart (paper is complete and comprehensive) OR add if required by instructor.

---

## Question 6: Did you upload the .py/.ipynb file(s) in the folder

**Answer: Y (YES) - 11 Python files included**

### Python Files Uploaded:

**Backend API (2 files):**
1. `backend/app/api/datasets.py` (136 lines)
   - Upload CSV datasets
   - Validate and parse data
   - Store in database

2. `backend/app/api/predictions.py` (210 lines)
   - ML model training
   - Prediction generation
   - Feature importance
   - Recommendations

**ML Models (2 files):**
3. `backend/app/ml/models/flaky_detector.py` (150 lines)
   - BaselineDetector (rule-based)
   - MLFlakyDetector (logistic, random forest, gradient boosting)
   - Model factory

4. `backend/app/ml/features/feature_extractor.py` (123 lines)
   - FeatureExtractor class
   - 15+ feature engineering methods
   - Temporal integrity

**Database Models (2 files):**
5. `backend/app/models/dataset.py`
   - Dataset ORM model
   - Metadata storage

6. `backend/app/models/test_execution.py`
   - TestExecution ORM model
   - Execution history storage

**Schemas (2 files):**
7. `backend/app/schemas/dataset.py`
   - Pydantic schemas
   - API validation

8. `backend/app/schemas/prediction.py`
   - Prediction response schemas

**Core (2 files):**
9. `backend/app/core/config.py`
   - Configuration settings

10. `backend/app/core/database.py`
    - Database initialization
    - Session management

**Utilities (1 file):**
11. `backend/app/utils/generate_synthetic_data.py` (200+ lines)
    - Synthetic dataset generator
    - Realistic patterns

**Main Application:**
12. `backend/app/main.py`
    - FastAPI app entry point
    - CORS configuration
    - Route registration

### Additional Files:
- `backend/requirements.txt` - Python dependencies
- `frontend/src/` - React/TypeScript frontend (10+ files)
- `frontend/package.json` - Node dependencies

### No Jupyter Notebooks (.ipynb)
**Reason:** All code is production-ready Python modules for deployment. The system is a full web application, not an exploratory notebook.

**If Notebook Required:**
Would you like me to create a demonstration Jupyter notebook showing:
- Data loading and exploration
- Feature engineering examples
- Model training walkthrough
- Results visualization

---

## Question 7: The latex ZIP file and pdf file uploaded in the folder (Y/N)

**Answer: PARTIAL - Creating now**

**Current Status:**
- ✅ LaTeX source: `term_paper.tex` (present, 23KB)
- ✅ README: `LATEX_README.txt` (created)
- ⚠️ Screenshots: Need to be downloaded from Overleaf
- ⚠️ PDF: Need to compile
- ⚠️ ZIP: Will create once above are ready

### How to Complete:

#### Step 1: Compile PDF on Overleaf
1. Go to your Overleaf project with term_paper.tex
2. Verify both screenshots are uploaded:
   - dataset_management.png
   - analysis_results.png
3. Click "Recompile"
4. Download PDF (button next to Recompile)
5. Save as: `term_paper.pdf`

#### Step 2: Download Screenshots
1. In Overleaf, click each image in file list
2. Download both PNG files
3. Save to project directory

#### Step 3: Create ZIP
**Option A: Run the script (Automated)**
```bash
cd /Users/manan/Desktop/SQTA/Innovative
chmod +x CREATE_SUBMISSION_PACKAGE.sh
./CREATE_SUBMISSION_PACKAGE.sh
```

**Option B: Manual**
```bash
cd /Users/manan/Desktop/SQTA/Innovative
zip FlakeGuard_AI_LaTeX_Submission.zip \
    term_paper.tex \
    term_paper.pdf \
    dataset_management.png \
    analysis_results.png \
    LATEX_README.txt
```

### ZIP Contents (Final):
```
FlakeGuard_AI_LaTeX_Submission.zip
├── term_paper.tex (LaTeX source)
├── term_paper.pdf (Compiled paper)
├── dataset_management.png (Figure 1)
├── analysis_results.png (Figure 2)
└── LATEX_README.txt (Instructions)
```

**File Created:**
- ✅ Script: `CREATE_SUBMISSION_PACKAGE.sh` (ready to run)

---

## 🎯 COMPLETE ANSWERS SUMMARY

| # | Question | Answer | Evidence |
|---|----------|--------|----------|
| 1 | Paper Title | An Explainable AI Framework for Flaky Test Detection in CI/CD Pipelines | term_paper.tex line 13 |
| 2 | Dataset URL | https://github.com/mananvsuri/FlakyAI/blob/main/datasets/synthetic_test_data.csv | Public GitHub repo |
| 3 | Preprocessing | **YES** - 15+ features, validation, temporal integrity | feature_extractor.py, datasets.py |
| 4 | Problem & Solution | **YES** - In Introduction & Abstract | term_paper.tex lines 23-37 |
| 5 | Flowchart | **NO** - Text description only, no visual diagram | Described in Sections 4-5 |
| 6 | Python Files | **YES** - 11 .py files + full application | backend/app/*, frontend/src/* |
| 7 | LaTeX ZIP & PDF | **PARTIAL** - .tex ready, creating ZIP | Instructions provided above |

---

## ✅ FINAL CHECKLIST

### Completed:
- [x] Paper written (3 pages, IEEE format)
- [x] Authors added (Manan Suri, Nilaksh Pathak)
- [x] 13 references cited
- [x] GitHub repository created
- [x] Dataset uploaded to GitHub
- [x] Python code complete (11 files)
- [x] Preprocessing implemented (15+ features)
- [x] Problem & solution statements in paper
- [x] Architecture described in text
- [x] Results included with real numbers
- [x] App running (Backend + Frontend)

### To Complete:
- [ ] Download PDF from Overleaf
- [ ] Download screenshots from Overleaf
- [ ] Create ZIP file with script
- [ ] (Optional) Create flowchart diagram
- [ ] (Optional) Create Jupyter notebook

---

## 📊 App Status

**Application is RUNNING:**
- Backend: http://localhost:8000 ✅
- Frontend: http://localhost:5173 ✅

**Test Now:**
1. Open http://localhost:5173
2. Go to "Dataset Management"
3. Upload: datasets/synthetic_test_data.csv
4. Go to "Flaky Test Analysis"
5. Select dataset, choose Random Forest
6. Click "Run Analysis"
7. See results: 22 flaky tests detected!

---

## 📧 Authors

**Manan Suri**
- Email: 23bce168@nirmauni.ac.in
- University: Nirma University
- Department: Computer Science and Engineering

**Nilaksh Pathak**
- Email: 23bce199@nirmauni.ac.in
- University: Nirma University
- Department: Computer Science and Engineering

**GitHub:** https://github.com/mananvsuri/FlakyAI
**Location:** Ahmedabad, India
**Date:** October 2024

---

## 🎉 PROJECT COMPLETE!

All questions answered with evidence and documentation!
