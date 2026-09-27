# Reproducing the analysis

## First run

Download the repository from GitHub (or clone it). It includes both the 904-respondent reference CSV and `data/questionnaire.json`. Create this folder in Google Drive and upload a copy of both bundled inputs:

```text
MyDrive/SOICT-2026/data/
  soict_2026_survey_responses.csv
  questionnaire.json
```

The supplied `questionnaire.json` maps each of the 71 item codes to its question text. If using another file name or location, edit `QUESTION_TEXT_PATH` in the phase 1 configuration cell. The survey CSV must meet the documented input schema. The `config/item_labels_en.csv` descriptions are not questionnaire text.

In Colab, open each notebook from the downloaded repository, select its initial path/configuration cell, and confirm that the paths match your Drive. Run cells in order in each notebook and approve the Drive mount when prompted. Colab will install missing dependencies during phases 1 and 2; these phases invoke R/lavaan. The complete reference workflow runs phase 1, phase 2, phase 3, then phase 4. Phase 1 and phase 2 do not supply input files to the later phases: phase 3 reads the CSV directly, and phase 4 reads the CSV **and** the phase 3 ZIP.

After phase 3 completes, copy the full path to the generated `phase_03_<timestamp>.zip` from its last cell. In the **first code cell of phase 4**, set the fallback in this existing line to that path before running cells:

```python
PHASE3_RESULTS_PATH = os.environ.get(
    'PHASE4_PHASE3_RESULTS',
    '/content/drive/MyDrive/SOICT-2026/results/phase_03/phase_03_<actual-timestamp>.zip',
)
```

Replace `<actual-timestamp>` with the filename printed by phase 3. Do not execute the literal placeholder. When changing input CSVs, create a new phase 3 output from the same CSV and explicitly set its ZIP path here. The ancillary notebook is independent of the four-phase sequence and can run after you set its input/output form fields.

## Runtime

Use Google Colab or a local Python environment with packages from `requirements.txt`. Phases 1 and 2 additionally require `Rscript` and the R package `lavaan`. Install lavaan using `install.packages("lavaan", repos="https://cloud.r-project.org")`; the phase 2 Monte Carlo code checks that its version is at least 0.7-2. Record the Python and R package versions and preserve every run manifest. On Colab, notebooks mount Google Drive for reading input and writing results. For local execution, install JupyterLab (`python -m pip install jupyterlab`), install the Python requirements (`python -m pip install -r requirements.txt`), and install R and lavaan before opening the notebooks. Edit their first configuration cells to use absolute local input/output paths instead of the Colab defaults.

## Input paths

1. Place the bundled CSV and `questionnaire.json` in a directory accessible to the runtime. Do not replace the question document with the English gloss file.
2. Run `python scripts/check_inputs.py data/soict_2026_survey_responses.csv --official` from the repository root for the bundled reference dataset. Without `--official`, the same script accepts any matching future input.
3. Set the notebook paths as shown below. They may point to local storage or Drive.

| Notebook | Required path settings | Optional path settings |
| --- | --- | --- |
| Phase 1 | `PHASE1_INPUT_CSV`, `PHASE1_QUESTION_FILE`, `PHASE1_OUTPUT_DIR` | None |
| Phase 2 | `PHASE2_INPUT_CSV`, `PHASE2_OUTPUT_DIR` | None |
| Phase 3 | `PHASE3_INPUT_DATA`, `PHASE3_OUTPUT_DIR` | `PHASE3_PHASE2_RESULTS` to enable additional SEM-based weighting. |
| Phase 4 | `PHASE4_INPUT_CSV`, `PHASE4_OUTPUT_DIR`, `PHASE4_PHASE3_RESULTS` | Thresholds in the configuration cell. |
| Ancillary | `INPUT_DATA_PATH`, `OUTPUT_DIR_PATH` in the first code cell | None |

Phase 1, phase 2, and phase 3 read the same input CSV independently. For phase 4, provide the phase 3 ZIP generated from that CSV; the notebook validates the source fingerprint and respondent IDs. To reproduce the supplied phase 3 reference results exactly, leave `PHASE3_PHASE2_RESULTS` empty: SEM-weighted configurations were unavailable in that reference run. Setting it to a matching phase 2 ZIP runs additional sensitivity configurations and therefore defines a different analysis run.

## Audit trail and interpretation

Run the notebook cells top to bottom. Keep the exported ZIP, logs, configuration JSON, and SHA-256 manifests. A run timestamp identifies each output directory. Bootstrap and Monte Carlo seeds and thresholds are declared in configuration cells. Preserve the settings used for any reported estimates.

The official reference results were generated from the 904-row CSV. Python syntax, paths, input checks, and the phase 4 computational outputs can be checked in the release environment; full CFA and SEM recomputation requires an R/lavaan installation. The ancillary ordinal models require `statsmodels`.

The reported quantities are descriptive associations, scale diagnostics, model comparisons, conditional rule metrics, and simulation intervals. Interpret them as tests of proposed relationships in a cross sectional survey.
