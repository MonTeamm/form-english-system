# Release verification

The package was checked against the official 904-row input with SHA-256 `97f296d2e222597976d9a6a5213cfac2f2d51180858b779fcad4437160b73e96`.

| Check | Observed result |
| --- | --- |
| Input contract | 904 rows, 71 item columns, 894 fully observed questionnaires, 10 routed away from ENP. |
| Phase 1 preprocessing | Loaded all 904 respondents and all 71 texts in the bundled questionnaire; validation passed. |
| Phase 2 preprocessing | Loaded the official CSV; both the 894-person primary set and 10-person ENP routing set passed input checks. |
| Phase 3 complete run | Recomputed 3A, 3B, and 3C from the bundled CSV without SEM-based weighting; all 49 comparable numeric CSV files matched the earlier reference to relative tolerance `1e-9` and absolute tolerance `1e-10`. |
| Phase 4 computation | Recomputed 4A and 4B with the newly generated matching phase 3 ZIP. The numeric columns in 32 CSV files matched the earlier reference within the same tolerance; five additional text-only CSV files matched exactly. |
| Phase 4 candidate and sensitivity counts | 26,301 candidate rules; 120 entered deep analysis; 16 passed the strict encoding sensitivity check; 30 rules were listed in the final priority table. |
| Source integrity | All five notebook files are valid JSON; every Python code cell parses; saved notebooks contain no execution output. The publication-language audit flags zero non-English prose letters in Markdown, string literals, and comments. |

Three phase 3 manifests and two phase 4 manifests contain file sizes and hashes; these change when paths, descriptive text, or run timestamps change. The 49 phase 3 and 37 phase 4 comparisons exclude those manifests. R/lavaan is not available in this release workspace; phase 1 CFA and phase 2 SEM need to be rerun in an environment with the required R package before claiming a full clean-room reproduction. The ancillary ordinal models require `statsmodels` in the execution environment.
