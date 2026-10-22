# Dataset Acquisition Documentation

**Project:** FlakeGuard AI - Explainable Flaky Test Detection  
**Date:** 2024  
**Status:** Research Phase

## Overview

This document tracks the investigation, acquisition, and preprocessing of datasets used in this research project. All datasets must be verified for availability, licensing, format compatibility, and research suitability before use.

## Dataset Requirements

For training and evaluation, we require test execution histories with:

**Minimum Required Fields:**
- `test_id`: Unique test identifier
- `execution_id`: Unique execution record
- `timestamp`: When the test ran
- `outcome`: Test result (PASSED, FAILED, SKIPPED, ERROR)

**Highly Desired Fields:**
- `duration`: Execution time
- `retry_count`: Number of retries
- `error_message`: Failure message
- `environment`: Execution context
- Ground-truth flaky labels

**Minimum Data Requirements:**
- At least 100 unique tests
- At least 1000 total executions
- Multiple executions per test (for pattern detection)
- Time-ordered execution history

## Investigated Datasets

### 1. Google Flaky Test Dataset

**Description:** Google's research on flaky tests in their internal infrastructure.

**Status:** 🔍 **TO BE VERIFIED**

**References:**
- Paper: "Deflaker: Automatically Detecting Flaky Tests" (ICSE 2018)
- Paper: "An Empirical Analysis of Flaky Tests" (FSE 2014)

**Next Steps:**
1. Search IEEE Xplore and ACM Digital Library for official papers
2. Check if accompanying dataset is publicly available
3. Verify download URL and format
4. Document exact fields available
5. Record licensing terms

**Preliminary Search:**
- Check: https://research.google/pubs/
- Check: https://github.com/google/flaky-tests (if exists)
- Check paper supplementary materials

### 2. iDFlakies Dataset

**Description:** Dataset from the iDFlakies tool research project, detecting order-dependent flaky tests.

**Status:** 🔍 **TO BE VERIFIED**

**References:**
- Paper: "iDFlakies: A Framework for Detecting and Partially Classifying Flaky Tests" (ICST 2019)
- Authors: August Shi et al., University of Illinois

**Next Steps:**
1. Locate official paper and verify DOI
2. Check if dataset is in paper supplementary materials
3. Search GitHub for iDFlakies tool and associated data
4. Verify dataset format matches our requirements
5. Document preprocessing needed

**Preliminary Search:**
- Check: https://github.com/idflakies/iDFlakies
- Check ACM Digital Library for paper
- Check author websites for dataset links

### 3. FlakeFlagger Dataset

**Description:** Dataset from FlakeFlagger project on flaky test detection.

**Status:** 🔍 **TO BE VERIFIED**

**References:**
- Check recent ICSE, FSE, ASE conferences for FlakeFlagger papers
- Search arXiv for pre-prints

**Next Steps:**
1. Verify project existence
2. Locate associated research papers
3. Check for public dataset availability

### 4. TravisTorrent / GHTorrent CI Data

**Description:** Large-scale dataset of Travis CI build histories from GitHub projects.

**Status:** 🔍 **TO BE VERIFIED**

**Source:** https://travistorrent.testroots.org/

**Next Steps:**
1. Verify data is still available
2. Assess if test-level granularity is available (or only build-level)
3. Check download size and format
4. Document how to extract flaky test patterns
5. Verify licensing (typically academic use allowed)

**Challenges:**
- May only have build-level data, not individual test results
- Requires significant preprocessing
- May need to parse build logs to extract test outcomes

### 5. Public GitHub Repositories

**Description:** Mine test execution histories from open-source projects with public CI logs.

**Status:** 🔍 **TO BE INVESTIGATED**

**Potential Sources:**
- Projects with GitHub Actions workflows
- Projects with public Travis CI logs
- Projects with CircleCI public builds
- JUnit XML reports in public repositories

**Next Steps:**
1. Identify 5-10 candidate repositories with:
   - Active test suites
   - Public CI history
   - Multiple years of commits
   - Known flaky test issues (check GitHub issues)
2. Develop scraping/parsing tools
3. Document legal and ethical considerations
4. Check robots.txt and Terms of Service

**Challenges:**
- Time-consuming to collect
- Inconsistent formats across projects
- May lack ground-truth labels
- Requires careful ethical review

### 6. Academic Benchmark Datasets

**Description:** Standardized benchmark datasets from software engineering research.

**Status:** 🔍 **TO BE VERIFIED**

**Potential Sources:**
- Defects4J (known bugs in Java projects)
- Software Heritage
- Zenodo deposits from published papers
- FigShare academic datasets

**Next Steps:**
1. Search Zenodo for "flaky test" datasets
2. Review recent ASE, ICSE, FSE papers for shared datasets
3. Check data availability and format

## Dataset Selection Criteria

A dataset is suitable if it meets ALL of the following:

✅ **Availability:** Publicly accessible or obtainable through documented process  
✅ **Licensing:** Permits academic research use  
✅ **Format:** Can be parsed into our schema  
✅ **Size:** Sufficient for training and evaluation (min 100 tests, 1000 executions)  
✅ **Quality:** Has minimal corruption, reasonable completeness  
✅ **Labels:** Has ground-truth labels OR sufficient execution history to infer labels  
✅ **Documentation:** Has provenance information and field definitions

## Synthetic Dataset Fallback

If no suitable real dataset is found or if real datasets are insufficient, a **clearly labeled synthetic dataset** will be generated with:

**Characteristics:**
- Realistic test execution patterns
- Multiple test types:
  - Stable passing tests (high pass rate, low variability)
  - Consistently failing tests (high fail rate, consistent errors)
  - Flaky tests (intermittent failures with patterns)
  - Insufficient data tests (few executions)
- Temporal patterns matching real CI/CD behavior
- Environment and error variation
- Duration variability

**Labeling:**
- All synthetic data clearly marked with `is_synthetic = True`
- Flagged in database
- Displayed in UI with "SYNTHETIC DATA" badges
- Never represented as real-world evidence

**Usage Limitations:**
- Used for development and interface testing
- Used to demonstrate methodology
- NOT used to claim real-world performance
- NOT used as evidence in paper results section without disclosure

**Generation Script:** `/backend/app/utils/generate_synthetic_data.py`

## Current Dataset Status

**Real Datasets Acquired:** 0  
**Synthetic Datasets Generated:** 0  
**Datasets In Progress:** 6 under investigation

**Next Action:** Systematically verify each dataset source above, starting with Google and iDFlakies datasets.

## Preprocessing Requirements

Once a dataset is acquired, preprocessing must:

1. **Validate Schema:**
   - Check required fields exist
   - Identify missing optional fields
   - Record missingness patterns

2. **Data Cleaning:**
   - Remove duplicates (same execution_id)
   - Validate timestamps are parseable
   - Check outcome values are valid
   - Handle malformed records

3. **Temporal Ordering:**
   - Sort by timestamp
   - Verify chronological consistency
   - Identify any timestamp anomalies

4. **Ground-Truth Labels:**
   - If provided: validate label format
   - If not provided: document inference approach
   - Separate inference from evaluation labels

5. **Data Splits:**
   - Create chronological train/validation/test splits
   - Ensure no test_id leakage across splits
   - Document split ratios and dates

6. **Quality Metrics:**
   - Count total tests and executions
   - Calculate outcome distribution
   - Measure feature completeness
   - Identify class imbalance

## Licensing and Attribution

All datasets used will be:
- Properly attributed in the paper
- Cited with correct references
- Used within license terms
- Acknowledged in the application UI

## Ethical Considerations

When using real-world data:
- Do not expose proprietary information
- Do not reveal individual developer information
- Respect project privacy expectations
- Follow all applicable data protection regulations

## References Audit

All dataset sources will be documented in `references_audit.md` with:
- Full citation
- Verified URL or DOI
- License terms
- Date accessed
- Specific claims supported by this source

---

**Last Updated:** 2024  
**Status:** Investigation phase - datasets to be verified before use  
**Maintained By:** FlakeGuard AI Research Team
