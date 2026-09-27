# Analysis specification

The four phases address different aspects of the same survey. The primary research objective is to test the observed chain of hypothesized relationships. All phases use the survey's recorded responses; none by itself establishes a causal chain.

| Phase | Main operation | Output to inspect |
| --- | --- | --- |
| 1 | Validate items, examine all 16 scales and selected overlap pairs, fit ordered categorical CFA using WLSMV. | Measurement fit, item loadings, HTMT, model comparison, diagnostic log. |
| 2 | Fit the prespecified SEM alternatives with R/lavaan; estimate structural links and three indirect effects; compare Delta and Monte Carlo intervals. | Model fit, coefficients, indirect effects, interval and sensitivity tables. |
| 3 | Compare cluster counts and fit, evaluate a two-profile solution and alternative clustering configurations. | Cluster quality, stability, external validation, profile assignments. |
| 4 | Encode low and high item states, mine directional association rules, apply multiple-testing correction, respondent bootstrap, encoding sensitivity and profile comparisons. | Rule table, bootstrap intervals, robustness and profile comparison tables. |

The ancillary notebook analyzes each of the 90 barrier-feature pairs in forward and reverse ordinal models and adjusts the corresponding significance tests. It does not make two independent causal claims from the same data.

All analysis thresholds, seeds, bootstrap counts, and Monte Carlo counts are declared in notebook configuration cells rather than estimated from the observed significance levels. Keep a run's configuration JSON and manifest when citing its results. English item descriptions are convenience glosses; for measurement interpretation use the bundled `data/questionnaire.json`.
