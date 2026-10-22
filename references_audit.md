# References Audit

**Project:** FlakeGuard AI  
**Purpose:** Track and verify all scholarly sources cited in the academic paper

This document ensures all references are:
- ✅ Accurately cited with correct authors, titles, venues, and dates
- ✅ Verified through authoritative sources (IEEE Xplore, ACM DL, publisher sites, arXiv)
- ✅ Accessible via DOI or stable URL
- ✅ Relevant to claims made in the paper

## Verification Process

For each reference:
1. Locate the source through academic databases
2. Verify bibliographic metadata (authors, title, year, venue)
3. Confirm accessibility (DOI, URL, or library access)
4. Document the specific claims supported by this source
5. Record verification date and source

## Status Legend

- ✅ **VERIFIED**: Full bibliographic details confirmed
- 🔍 **TO VERIFY**: Identified but not yet confirmed
- ❌ **UNABLE TO VERIFY**: Could not confirm details
- 📝 **PLACEHOLDER**: Preliminary citation pending verification

---

## Core References

### 1. Flaky Test Foundations

#### 1.1 Google Flaky Test Research

**Status:** 🔍 TO VERIFY

**Preliminary Citation:**
> Luo, Q., Hariri, F., Eloussi, L., & Marinov, D. (2014). An empirical analysis of flaky tests. In Proceedings of the 22nd ACM SIGSOFT International Symposium on Foundations of Software Engineering (FSE 2014), pp. 643-653. ACM.

**DOI:** [TO BE VERIFIED]  
**URL:** [TO BE VERIFIED]

**Claims Supported:**
- Prevalence of flaky tests in Google's infrastructure
- Categories of flakiness root causes
- Impact on developer productivity

**Verification Source:** ACM Digital Library

**Notes:** Need to verify exact title, page numbers, and DOI.

---

#### 1.2 Deflaker Paper

**Status:** 🔍 TO VERIFY

**Preliminary Citation:**
> Bell, J., Legunsen, O., Hilton, M., Eloussi, L., Yung, T., & Marinov, D. (2018). DeFlaker: Automatically detecting flaky tests. In Proceedings of the 40th International Conference on Software Engineering (ICSE 2018), pp. 433-444. ACM.

**DOI:** [TO BE VERIFIED]  
**URL:** [TO BE VERIFIED]

**Claims Supported:**
- Automatic flaky test detection methods
- Evaluation on real-world projects
- Detection accuracy metrics

**Verification Source:** ACM Digital Library / IEEE Xplore

**Notes:** ICSE papers available through both ACM and IEEE.

---

### 2. Flaky Test Detection Methods

#### 2.1 iDFlakies

**Status:** 🔍 TO VERIFY

**Preliminary Citation:**
> Lam, W., Oei, R., Shi, A., Marinov, D., & Xie, T. (2019). iDFlakies: A framework for detecting and partially classifying flaky tests. In Proceedings of the 12th IEEE International Conference on Software Testing, Verification and Validation (ICST 2019), pp. 312-322. IEEE.

**DOI:** [TO BE VERIFIED]  
**URL:** [TO BE VERIFIED]

**Claims Supported:**
- Order-dependent flaky test detection
- Classification of flakiness types
- Dataset availability

**Verification Source:** IEEE Xplore

**GitHub:** https://github.com/idflakies/iDFlakies [TO BE VERIFIED]

---

#### 2.2 FlakeFlagger

**Status:** 🔍 TO VERIFY

**Search Keywords:**
- "FlakeFlagger flaky test detection"
- Recent ICSE, FSE, ASE proceedings
- arXiv pre-prints

**Notes:** Need to verify if this project exists and has associated publications.

---

### 3. Explainable AI

#### 3.1 SHAP Paper

**Status:** 🔍 TO VERIFY

**Preliminary Citation:**
> Lundberg, S. M., & Lee, S. I. (2017). A unified approach to interpreting model predictions. In Advances in Neural Information Processing Systems 30 (NIPS 2017), pp. 4765-4774.

**DOI:** [TO BE VERIFIED]  
**URL:** https://papers.nips.cc/paper/2017/hash/8a20a8621978632d76c43dfd28b67767-Abstract.html [TO BE VERIFIED]

**Claims Supported:**
- Theoretical foundation for SHAP values
- Shapley value properties
- Consistency and local accuracy

**Verification Source:** NeurIPS proceedings

**GitHub:** https://github.com/slundberg/shap

---

#### 3.2 LIME Paper

**Status:** 🔍 TO VERIFY

**Preliminary Citation:**
> Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why should I trust you?" Explaining the predictions of any classifier. In Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD 2016), pp. 1135-1144. ACM.

**DOI:** [TO BE VERIFIED]  
**URL:** [TO BE VERIFIED]

**Claims Supported:**
- Model-agnostic explanation methods
- Local interpretability
- Human evaluation of explanations

**Verification Source:** ACM Digital Library

---

### 4. Machine Learning in Software Engineering

#### 4.1 Test Prioritization Survey

**Status:** 🔍 TO VERIFY

**Search Strategy:**
- IEEE TSE, ACM TOSEM journals
- "test prioritization machine learning" surveys
- Recent survey papers (2018-2023)

**Intended Claims:**
- Prior work in ML for testing
- Test selection and prioritization
- Feature engineering approaches

---

#### 4.2 Defect Prediction

**Status:** 🔍 TO VERIFY

**Search Strategy:**
- "software defect prediction machine learning"
- Empirical Software Engineering journal
- TSE journal

**Intended Claims:**
- ML applications in quality assurance
- Feature importance in defect models
- Evaluation methodologies

---

### 5. CI/CD and Software Testing

#### 5.1 TravisTorrent

**Status:** 🔍 TO VERIFY

**Preliminary Citation:**
> Beller, M., Gousios, G., & Zaidman, A. (2017). TravisTorrent: Synthesizing Travis CI and GitHub for full-stack research on continuous integration. In Proceedings of the 14th International Conference on Mining Software Repositories (MSR 2017), pp. 447-450. IEEE.

**DOI:** [TO BE VERIFIED]  
**URL:** https://travistorrent.testroots.org [TO BE VERIFIED]

**Claims Supported:**
- CI/CD data availability
- Build and test execution patterns
- Dataset characteristics

**Verification Source:** IEEE Xplore

---

### 6. Software Testing Fundamentals

#### 6.1 Software Testing Textbook

**Status:** 🔍 TO VERIFY

**Potential Sources:**
- Ammann, P., & Offutt, J. (2016). Introduction to Software Testing (2nd ed.). Cambridge University Press.
- Myers, G. J., Sandler, C., & Badgett, T. (2011). The Art of Software Testing (3rd ed.). Wiley.

**Intended Claims:**
- Software testing foundations
- Test reliability concepts
- Quality assurance principles

---

### 7. Statistical Methods

#### 7.1 Imbalanced Learning

**Status:** 🔍 TO VERIFY

**Search Strategy:**
- "imbalanced classification machine learning"
- JMLR, Machine Learning journal
- Surveys on class imbalance

**Intended Claims:**
- Handling imbalanced datasets
- Evaluation metrics for imbalanced data
- PR-AUC vs ROC-AUC

---

### 8. Empirical Software Engineering

#### 8.1 Threats to Validity

**Status:** 🔍 TO VERIFY

**Potential Sources:**
- Wohlin, C., et al. (2012). Experimentation in Software Engineering. Springer.
- Threats to validity frameworks in ESE

**Intended Claims:**
- Experimental design in SE research
- Validity threat categories
- Mitigation strategies

---

## Reference Format

Using IEEE citation style:

```
[1] A. Author, B. Author, and C. Author, "Title of paper," in Proc. Conference Abbreviation, 
    Location, Year, pp. XX-XX, doi: XX.XXXX/XXXXXX.
    
[2] A. Author and B. Author, "Title of article," Journal Abbreviation, vol. XX, no. X, 
    pp. XX-XX, Month Year, doi: XX.XXXX/XXXXXX.
    
[3] A. Author, Title of Book, Edition ed. City, State: Publisher, Year.
```

---

## Verification Checklist

Before finalizing the paper:

- [ ] All citations have verified authors
- [ ] All titles are exact (not paraphrased)
- [ ] All publication years are correct
- [ ] All venues (conferences/journals) are verified
- [ ] DOIs are confirmed and accessible
- [ ] URLs are stable and working
- [ ] All claims are actually supported by the cited source
- [ ] No fabricated or speculative citations
- [ ] No placeholder citations in final version

---

## Sources for Verification

**Academic Databases:**
- IEEE Xplore: https://ieeexplore.ieee.org
- ACM Digital Library: https://dl.acm.org
- Springer Link: https://link.springer.com
- arXiv: https://arxiv.org
- Google Scholar: https://scholar.google.com (for initial search only)

**Publisher Sites:**
- ACM: https://www.acm.org
- IEEE: https://www.ieee.org
- Elsevier: https://www.elsevier.com
- Wiley: https://www.wiley.com

**DOI Resolution:**
- https://doi.org/ (official DOI resolver)

---

## Notes

- Use web_search or web_fetch to verify citations before finalizing
- Always check publisher websites for official metadata
- Prefer DOI over URL when both are available
- Include accessed dates for URLs without DOI
- Never cite a paper without reading at least the abstract and verifying it supports your claim

---

**Last Updated:** 2024  
**Status:** Preliminary - All references require verification before paper submission
