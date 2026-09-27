"""Validate survey input without modifying it or assuming a fixed sample size."""

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

SCALE_LENGTHS = {
    "ENP": 6, "PTED": 6, "MEU": 5,
    "REH": 3, "ELA": 3, "ORG": 3, "CRT": 3,
    "MSR": 4, "TSEM": 3, "VLS": 6, "DEL": 7,
    "LPSN": 5, "SFN": 4, "TECN": 6, "PU": 4, "BI": 3,
}
ITEMS = [f"{name}{i:02d}" for name, length in SCALE_LENGTHS.items() for i in range(1, length + 1)]
REFERENCE_SHA256 = "97f296d2e222597976d9a6a5213cfac2f2d51180858b779fcad4437160b73e96"


def read_input(path):
    for encoding in ("utf-8-sig", "utf-8", "cp1258", "cp1252", "latin1"):
        for separator in (",", ";", "\t"):
            try:
                frame = pd.read_csv(path, encoding=encoding, sep=separator, dtype=str)
            except (UnicodeError, pd.errors.ParserError):
                continue
            if set(ITEMS + ["S0_ENGLISH_NECESSARY"]).issubset(frame.columns):
                return frame, encoding, separator
    raise ValueError("Unable to read the required item columns; check CSV encoding and separator.")


def validate(path, official=False):
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    frame, encoding, separator = read_input(path)
    if not frame.columns.is_unique:
        raise ValueError("Input column names must be unique.")
    if "RESPONDENT_ID" in frame:
        ids = frame["RESPONDENT_ID"]
        if ids.isna().any() or ids.str.strip().eq("").any() or not ids.is_unique:
            raise ValueError("RESPONDENT_ID must be present, nonempty, and unique when supplied.")
    columns = ITEMS + ["S0_ENGLISH_NECESSARY"]
    values = frame[columns].apply(pd.to_numeric, errors="coerce")
    if (frame[columns].notna() & values.isna()).any().any():
        raise ValueError("The questionnaire contains values that cannot be parsed as numbers.")
    if not values["S0_ENGLISH_NECESSARY"].isin((0, 1)).all():
        raise ValueError("The S0 routing indicator must contain only 0 and 1.")
    if any(not values[item].dropna().isin(range(1, 6)).all() for item in ITEMS):
        raise ValueError("Likert items must contain only integer values 1 through 5.")
    enp = [f"ENP{i:02d}" for i in range(1, 7)]
    missing_enp = values[enp].isna().sum(axis=1)
    s0 = values["S0_ENGLISH_NECESSARY"]
    if not ((s0.eq(0) & missing_enp.eq(6)) | (s0.eq(1) & missing_enp.eq(0))).all():
        raise ValueError("ENP availability does not match the S0 survey routing rule.")
    if values[[item for item in ITEMS if item not in enp]].isna().any().any():
        raise ValueError("An item outside ENP is missing.")
    result = {
        "rows": len(frame), "complete_71": int(missing_enp.eq(0).sum()),
        "enp_not_applicable": int(missing_enp.eq(6).sum()),
        "item_columns": len(ITEMS), "sha256": digest,
        "encoding": encoding, "separator": separator,
    }
    if official:
        if digest != REFERENCE_SHA256 or (result["rows"], result["complete_71"]) != (904, 894):
            raise ValueError("Input does not match the official 904-row reference file.")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("--official", action="store_true", help="Require the official reference fingerprint.")
    args = parser.parse_args()
    print(json.dumps(validate(args.input_csv, args.official), indent=2))


if __name__ == "__main__":
    main()
