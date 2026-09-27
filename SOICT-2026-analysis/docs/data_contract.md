# Input data contract

The bundled `data/soict_2026_survey_responses.csv` contains one row per respondent and 71 five-point Likert question columns grouped into 16 scales. It is UTF-8 encoded with semicolon separators. Keep stable item codes and numeric values. The input may contain other columns; analysis uses the documented fields.

| Field | Requirement |
| --- | --- |
| `RESPONDENT_ID` | Stable nonempty unique respondent identifier; notebooks can derive position-based IDs when absent. For cross-phase joins, provide the same IDs and row order. |
| `S0_ENGLISH_NECESSARY` | Binary 0 or 1 routing indicator. |
| `ENP01`–`ENP06` | Values 1–5 when S0 = 1; all six missing when S0 = 0. |
| Remaining 65 item codes | Integer values from 1 to 5 with no missing values. |

The 16 scales are `ENP`, `PTED`, `MEU`, `REH`, `ELA`, `ORG`, `CRT`, `MSR`, `TSEM`, `VLS`, `DEL`, `LPSN`, `SFN`, `TECN`, `PU`, and `BI`. Exact 71 item names and group membership are defined in the phase 1 notebook; run `python scripts/check_inputs.py path/to/input.csv` before starting.

For the official reference input, there are 904 rows, 894 complete 71-item responses, and 10 rows routed away from all six ENP questions. The official reference SHA-256 is recorded in the root README. These counts are reference observations, not hardcoded acceptance criteria for structurally compatible future inputs.

Phase 1 reads the bundled `data/questionnaire.json`, a mapping of all 71 item codes to complete question texts. Supported replacement formats are CSV, TSV, XLSX, JSON, Markdown, TXT, and DOCX. The English descriptions in `config/item_labels_en.csv` are explanatory glosses, not question wording.
