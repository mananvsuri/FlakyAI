# FlakeGuard AI - Datasets

This directory contains test execution datasets used for training and evaluating the FlakeGuard AI models.

## Directory Structure

```
datasets/
├── README.md                    # This file
├── synthetic_test_data.csv      # Generated synthetic dataset (if created)
├── [real_dataset_name].csv      # Real datasets (if acquired)
├── dataset_manifest.json        # Metadata about all datasets
└── raw/                         # Raw data before preprocessing (if applicable)
```

## Dataset Requirements

FlakeGuard AI requires test execution histories with the following schema:

### Required Fields

- **test_id** (string): Unique identifier for the test
- **execution_id** (string): Unique identifier for each execution
- **timestamp** (ISO 8601): When the test was executed
- **outcome** (string): Test result - one of: PASSED, FAILED, SKIPPED, ERROR

### Optional Fields (Highly Recommended)

- **project_id** (string): Project or repository identifier
- **duration** (float): Execution time in seconds
- **retry_count** (integer): Number of retries (0 = no retry)
- **error_message** (string): Error message if test failed
- **stack_trace** (string): Stack trace if available
- **environment** (string): Execution environment (staging, production, etc.)
- **commit_hash** (string): Git commit hash
- **branch** (string): Git branch name
- **changed_files** (integer): Number of files changed in commit
- **runner_id** (string): CI runner or machine identifier

### Ground Truth Labels (If Available)

- **is_flaky_label** (string): Ground truth label - one of: FLAKY, NOT_FLAKY, UNKNOWN
- **label_source** (string): Source of label (e.g., "manual", "inferred", "dataset")

## CSV Format Example

```csv
test_id,execution_id,timestamp,outcome,duration,retry_count,error_message,environment,is_flaky_label
test_login_001,exec_0001,2024-01-01T10:00:00Z,PASSED,1.2,0,,staging,UNKNOWN
test_login_001,exec_0002,2024-01-01T11:00:00Z,FAILED,2.5,1,Timeout error,staging,UNKNOWN
test_login_001,exec_0003,2024-01-01T12:00:00Z,PASSED,1.1,0,,staging,UNKNOWN
test_checkout_002,exec_0004,2024-01-01T10:05:00Z,PASSED,0.8,0,,production,UNKNOWN
```

## JSON Format Example

```json
[
  {
    "test_id": "test_login_001",
    "execution_id": "exec_0001",
    "timestamp": "2024-01-01T10:00:00Z",
    "outcome": "PASSED",
    "duration": 1.2,
    "retry_count": 0,
    "environment": "staging"
  },
  {
    "test_id": "test_login_001",
    "execution_id": "exec_0002",
    "timestamp": "2024-01-01T11:00:00Z",
    "outcome": "FAILED",
    "duration": 2.5,
    "retry_count": 1,
    "error_message": "Timeout error",
    "environment": "staging"
  }
]
```

## JUnit XML Format Support

FlakeGuard AI can also parse JUnit XML reports. These should contain test execution results with timestamps and outcomes.

Example:
```xml
<testsuite name="TestSuite" tests="2" failures="1" time="3.7">
  <testcase name="test_login_001" classname="tests.TestLogin" time="1.2">
    <!-- Passed test -->
  </testcase>
  <testcase name="test_login_002" classname="tests.TestLogin" time="2.5">
    <failure message="Timeout error">
      Stack trace here...
    </failure>
  </testcase>
</testsuite>
```

## Dataset Manifest

The `dataset_manifest.json` file tracks metadata for all datasets:

```json
{
  "datasets": [
    {
      "name": "synthetic_test_data",
      "filename": "synthetic_test_data.csv",
      "source": "generated",
      "is_synthetic": true,
      "generated_date": "2024-01-01",
      "num_tests": 150,
      "num_executions": 1500,
      "num_projects": 5,
      "description": "Synthetic dataset for development and testing"
    }
  ]
}
```

## Data Quality Checks

Before using a dataset, verify:

1. ✅ All required fields are present
2. ✅ Timestamps are in ISO 8601 format and chronologically ordered
3. ✅ Outcomes are valid (PASSED, FAILED, SKIPPED, ERROR)
4. ✅ No duplicate execution_ids
5. ✅ Duration values are non-negative (if present)
6. ✅ Each test has multiple executions for pattern detection

The upload API performs these validations automatically.

## Privacy and Licensing

### For Real Datasets

- Ensure you have permission to use the data
- Check licensing terms
- Respect project and developer privacy
- Do not include sensitive information
- Attribute data sources properly

### For Synthetic Datasets

- Clearly mark as synthetic in all interfaces
- Document generation methodology
- Do not represent as real-world data
- Use only for development and demonstration

## Generating Synthetic Data

To generate a synthetic dataset:

```bash
cd backend
python -m app.utils.generate_synthetic_data --num-tests 150 --num-executions 1500 --output ../datasets/synthetic_test_data.csv
```

Parameters:
- `--num-tests`: Number of unique tests (default: 100)
- `--num-executions`: Total number of executions (default: 1000)
- `--flaky-ratio`: Proportion of tests that are flaky (default: 0.15)
- `--output`: Output file path

The generator creates:
- Stable passing tests (~50%)
- Persistently failing tests (~30%)
- Flaky tests with various patterns (~15%)
- Insufficient data tests (~5%)

## Uploading Datasets

### Via Web Interface

1. Navigate to Dataset Management page
2. Click "Upload Dataset" or drag and drop file
3. Fill in metadata (name, description, source)
4. Mark "is_synthetic" if applicable
5. Click "Import"

### Via API

```bash
curl -X POST "http://localhost:8000/api/v1/datasets/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@datasets/synthetic_test_data.csv" \
  -F "name=my_test_dataset" \
  -F "description=Test execution history" \
  -F "is_synthetic=false"
```

## Dataset Size Recommendations

### Minimum for Training
- 100+ unique tests
- 1000+ total executions
- 5+ executions per test on average

### Recommended for Research
- 500+ unique tests
- 5000+ total executions
- 10+ executions per test on average
- Multiple projects if possible

### Optimal
- 1000+ unique tests
- 10000+ total executions
- 20+ executions per test on average
- Diverse projects and environments

## Known Public Datasets

See `docs/dataset_acquisition.md` for information on:

1. **Google Flaky Test Dataset**
2. **iDFlakies Dataset**
3. **TravisTorrent**
4. **FlakeFlagger Dataset** (if available)

Each must be verified for availability and compatibility before use.

## Troubleshooting

### Upload Fails

- Check file format matches schema
- Ensure required fields are present
- Verify timestamps are valid ISO 8601
- Check file size (limit: 100MB)

### Validation Errors

- Review error messages from API
- Check sample records for format issues
- Ensure outcome values are valid
- Verify no duplicate execution_ids

### Missing Features

- Some features require optional fields
- Duration features need `duration` field
- Error analysis needs `error_message` field
- Environment features need `environment` field

The system will calculate features from available data only.

## Security Notes

- Never commit sensitive data to git
- datasets/*.csv is in .gitignore
- Sanitize error messages before upload
- Review data for PII before sharing

## Citation

If using a public dataset, cite appropriately in your research:

```
# In term_paper.md references section
[X] Dataset Author(s), "Dataset Name," Source, Year. [Online]. 
    Available: URL. Accessed: Date.
```

---

**Last Updated:** 2024  
**Status:** Awaiting dataset acquisition or generation
