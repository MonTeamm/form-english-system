## Start here: Google Colab

The repository contains both inputs for the four-phase analysis. For Google Colab, copy these bundled files to the same folder in Google Drive:

| File | Place in Google Drive | Used by |
| --- | --- | --- |
| `data/soict_2026_survey_responses.csv` (904 rows; see the [schema](docs/data_contract.md)) | `MyDrive/SOICT-2026/data/soict_2026_survey_responses.csv` | All four phases and the optional ancillary analysis. |
| `data/questionnaire.json` (71 item texts) | `MyDrive/SOICT-2026/data/questionnaire.json` | Phase 1. |

The bundled `data/questionnaire.json` is the complete 71-item question-text input used for the reproducible workflow. The included `config/item_labels_en.csv` is only a navigation aid.

1. Download this repository from GitHub and upload **both included input files** to the Drive paths above. Open `notebooks/phase_01_measurement.ipynb` in Google Colab, run its cells from the top, and authorize the Google Drive mount when asked.
2. Open and run `notebooks/phase_02_structural_model.ipynb`. Phase 2 reads the same CSV directly; it does not need phase 1 output.
3. Open and run `notebooks/phase_03_learner_profiles.ipynb`. Leave `PHASE3_PHASE2_RESULTS` empty for the reference workflow. At the end, copy the path printed for `phase_03_<timestamp>.zip` under `MyDrive/SOICT-2026/results/phase_03/`.
4. Open `notebooks/phase_04_association_rules.ipynb`. In its first code cell, replace the empty fallback in `PHASE3_RESULTS_PATH = os.environ.get('PHASE4_PHASE3_RESULTS', '')` with the **actual full path** to the phase 3 ZIP, then run all cells. Phase 4 verifies that the CSV and phase 3 output correspond.

Each notebook writes timestamped results under `MyDrive/SOICT-2026/results/phase_0x/`; keep its logs, manifests, and ZIP. `notebooks/ancillary/barrier_feature_analysis.ipynb` is optional and uses the same CSV; check its two path fields before running. For another Drive location or local execution, see [full reproduction instructions](docs/reproduction.md).

## Repository layout

| Location | Purpose |
| --- | --- |
| `notebooks/phase_01_measurement.ipynb` | Validate 71 items, examine scale separation, and estimate ordered CFA. |
| `notebooks/phase_02_structural_model.ipynb` | Fit four SEM specifications and evaluate indirect effects using Monte Carlo. |
| `notebooks/phase_03_learner_profiles.ipynb` | Run the 3A, 3B, and 3C profile analyses in order. |
| `notebooks/phase_04_association_rules.ipynb` | Prepare item states and validate association rules against phase 3 profiles. |
| `notebooks/ancillary/barrier_feature_analysis.ipynb` | Analyze 6 barriers against 15 desired features in two conditional directions. |
| `config/item_labels_en.csv` | English descriptions for navigation and rule narratives; not official question wording. |
| `data/questionnaire.json` | 71 questionnaire item texts used by phase 1. |
| `data/soict_2026_survey_responses.csv` | De-identified 904-respondent reference data. |
| `scripts/check_inputs.py` | Check input structure and the official reference fingerprint. |
| `docs/` | Data contract, analysis decisions, and execution instructions. |

Each phase has one notebook. Run all cells in order. Python drives every workflow; phases 1 and 2 call R/lavaan for ordered CFA and SEM. No SPSS procedure is needed.

## Inputs and execution

The official 904-row CSV and the 71-item questionnaire are bundled in `data/`. Set their locations in the notebook configuration cells when running locally or using other files. Phase 3 can use matching phase 2 output for additional SEM-weighted configurations. Phase 4 requires the matching phase 3 ZIP. See [reproduction instructions](docs/reproduction.md) and [input schema](docs/data_contract.md).

Reference SHA-256 of the official CSV: `97f296d2e222597976d9a6a5213cfac2f2d51180858b779fcad4437160b73e96`. The notebooks also accept future CSVs with the documented schema when their sample size and response variation support each model. The fingerprint is required only when checking the official reference run or matching phase outputs.

The de-identified reference dataset is included with its original bytes preserved. The 71-item question file is bundled with the documented TECN source choice. Generated results are produced by running the notebooks.
