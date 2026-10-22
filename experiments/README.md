# Experiments Directory

This directory contains results from all experimental evaluations conducted for the FlakeGuard AI research project.

## Experiment Structure

Each experiment has its own subdirectory with standardized outputs:

```
experiments/
├── baseline_comparison/
│   ├── config.json           # Experiment configuration
│   ├── metrics.json          # All metrics in JSON format
│   ├── metrics.csv           # Metrics in CSV format
│   ├── confusion_matrices/   # Confusion matrix data
│   ├── plots/                # Generated charts
│   └── README.md             # Experiment description
├── feature_ablation/
├── data_sufficiency/
├── generalization/
├── explainability_eval/
└── runtime_analysis/
```

## Experiment Types

### 1. Baseline Comparison (RQ1)

**Goal:** Compare ML models with rule-based baseline

**Outputs:**
- `metrics.json`: Precision, recall, F1, PR-AUC, ROC-AUC for all models
- `confusion_matrices/`: Confusion matrix for each model
- `training_times.csv`: Training and inference time comparison
- `model_comparison.png`: Bar chart comparing all metrics

**Key Files:**
- Configuration: `baseline_comparison/config.json`
- Results: `baseline_comparison/metrics.json`

---

### 2. Feature Ablation (RQ2)

**Goal:** Identify feature importance through ablation study

**Outputs:**
- `feature_importance.csv`: Feature rankings
- `ablation_results.json`: Performance drop per feature group
- `shap_global.png`: SHAP global importance plot
- `feature_correlation.png`: Feature correlation heatmap

**Key Files:**
- Results: `feature_ablation/feature_importance.csv`
- SHAP values: `feature_ablation/shap_values.csv`

---

### 3. Data Sufficiency (RQ4)

**Goal:** Evaluate impact of execution history length

**Outputs:**
- `sufficiency_curve.csv`: Performance vs. execution count
- `sufficiency_plot.png`: Performance curve visualization
- `min_threshold.json`: Recommended minimum data requirements
- `confidence_calibration.csv`: Calibration at each threshold

**Key Files:**
- Results: `data_sufficiency/sufficiency_curve.csv`

---

### 4. Generalization (RQ4)

**Goal:** Test generalization across projects or time periods

**Outputs:**
- `generalization_metrics.json`: Within vs. out-of-distribution performance
- `project_performance.csv`: Per-project results
- `temporal_performance.csv`: Performance over time
- `degradation_analysis.json`: Performance drop analysis

**Key Files:**
- Results: `generalization/generalization_metrics.json`

---

### 5. Explainability Evaluation (RQ3)

**Goal:** Assess explanation quality and consistency

**Outputs:**
- `consistency_scores.json`: Explanation consistency metrics
- `alignment_analysis.csv`: SHAP-value alignment with features
- `example_explanations/`: Selected prediction explanations
- `sanity_checks.json`: Sanity check results

**Key Files:**
- Results: `explainability_eval/consistency_scores.json`
- Examples: `explainability_eval/example_explanations/`

---

### 6. Runtime Analysis (RQ4)

**Goal:** Measure practical performance characteristics

**Outputs:**
- `latency_stats.json`: Inference latency (median, p95, p99)
- `throughput.csv`: Tests per second at different batch sizes
- `training_scaling.png`: Training time vs. dataset size
- `resource_usage.json`: Memory and CPU utilization

**Key Files:**
- Results: `runtime_analysis/latency_stats.json`

---

## Running Experiments

### Run All Experiments

```bash
cd backend
source venv/bin/activate
python -m app.ml.experiments.run_all
```

This runs all six experiments sequentially and saves results.

### Run Individual Experiment

```bash
# Baseline comparison
python -m app.ml.experiments.baseline_comparison

# Feature ablation
python -m app.ml.experiments.feature_ablation

# Data sufficiency
python -m app.ml.experiments.data_sufficiency

# Generalization
python -m app.ml.experiments.generalization

# Explainability evaluation
python -m app.ml.experiments.explainability_eval

# Runtime analysis
python -m app.ml.experiments.runtime_analysis
```

### Via API

```bash
curl -X POST "http://localhost:8000/api/v1/experiments/run" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "baseline_comparison_exp1",
    "experiment_type": "baseline_comparison",
    "config": {"models": ["baseline", "logistic", "random_forest", "gradient_boosting"]},
    "dataset_id": 1
  }'
```

---

## Configuration Format

Each experiment uses a `config.json` file:

```json
{
  "experiment_type": "baseline_comparison",
  "dataset_id": 1,
  "models": ["baseline", "logistic", "random_forest", "gradient_boosting"],
  "random_seed": 42,
  "test_size": 0.2,
  "validation_size": 0.2,
  "use_chronological_split": true,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

---

## Results Format

### metrics.json

```json
{
  "experiment_id": 1,
  "experiment_type": "baseline_comparison",
  "timestamp": "2024-01-01T12:00:00Z",
  "models": {
    "baseline": {
      "test_precision": 0.75,
      "test_recall": 0.70,
      "test_f1": 0.72,
      "test_pr_auc": 0.76,
      "test_roc_auc": 0.80,
      "training_time_seconds": 0.5,
      "inference_time_ms": 1.2
    },
    "random_forest": {
      "test_precision": 0.83,
      "test_recall": 0.79,
      "test_f1": 0.81,
      "test_pr_auc": 0.86,
      "test_roc_auc": 0.88,
      "training_time_seconds": 45.3,
      "inference_time_ms": 12.5
    }
  }
}
```

### metrics.csv

```csv
model,precision,recall,f1,pr_auc,roc_auc,training_time,inference_time
baseline,0.75,0.70,0.72,0.76,0.80,0.5,1.2
logistic,0.80,0.75,0.77,0.82,0.84,5.2,2.1
random_forest,0.83,0.79,0.81,0.86,0.88,45.3,12.5
gradient_boosting,0.85,0.80,0.82,0.87,0.89,62.1,15.3
```

---

## Reproducibility

To reproduce experiments:

1. **Use same dataset:** Record dataset_id and version
2. **Fix random seeds:** random_seed=42 throughout
3. **Record environment:** Python version, package versions
4. **Save configurations:** All hyperparameters in config.json
5. **Document splits:** Record train/val/test split details

Each experiment directory contains a `REPRODUCIBILITY.md` with exact reproduction instructions.

---

## Exporting Results

### For Paper

Export experiment results for inclusion in the research paper:

```bash
# Export all metrics as CSV
curl "http://localhost:8000/api/v1/export/metrics?format=csv" -o all_metrics.csv

# Export specific experiment
curl "http://localhost:8000/api/v1/export/metrics?format=json&experiment_id=1" -o exp1_metrics.json
```

### Generate Charts

Charts are automatically generated during experiments and saved in each experiment's `plots/` directory.

To regenerate charts:

```bash
python -m app.ml.experiments.generate_charts --experiment-dir experiments/baseline_comparison
```

---

## Validation Checklist

Before using experiment results in the paper:

- [ ] All experiments completed without errors
- [ ] Configuration files saved
- [ ] Metrics exported as JSON and CSV
- [ ] Plots generated and saved
- [ ] Results match between JSON and CSV exports
- [ ] Random seeds were fixed
- [ ] Dataset version recorded
- [ ] Reproducibility instructions written
- [ ] Statistical significance tested (if applicable)
- [ ] Results interpreted correctly

---

## Important Notes

### Academic Integrity

- ❌ **Never fabricate results**
- ❌ **Never modify saved metrics manually**
- ✅ **Always use actual experiment outputs**
- ✅ **Report negative or unexpected findings honestly**
- ✅ **Document any issues or limitations**

### Results Status

Results sections in `term_paper.md` are marked **PENDING** until actual experiments are run. Do not populate results sections with invented numbers.

### Failure Handling

If an experiment fails:
1. Document the error
2. Fix the issue
3. Re-run the experiment
4. Do not use partial or corrupted results

---

## Storage

- Experiment results are stored in git (small JSON/CSV files)
- Large model files are in `models/` directory (gitignored)
- Raw predictions may be too large for git (use export API)

---

**Status:** Awaiting experiment execution  
**Last Updated:** 2024
