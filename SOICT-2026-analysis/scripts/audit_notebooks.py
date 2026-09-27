"""Check repository notebook syntax, output hygiene, and publication language."""

import ast
import json
from pathlib import Path
import sys
import tokenize
from io import StringIO
import unicodedata


def non_english_letters(value):
    """Allow Unicode math and punctuation, but flag non-ASCII prose letters."""
    return any(ord(character) > 127 and unicodedata.category(character).startswith('L')
               for character in value)


def inspect(notebook):
    result = []
    payload = json.loads(notebook.read_text(encoding="utf-8"))
    for index, cell in enumerate(payload["cells"]):
        source = "".join(cell["source"])
        if cell["cell_type"] == "markdown":
            if non_english_letters(source):
                result.append((index, "Non-English Markdown content"))
            continue
        if cell.get("outputs") or cell.get("execution_count") is not None:
            result.append((index, "Saved execution state"))
        try:
            ast.parse(source)
        except SyntaxError as error:
            result.append((index, f"Invalid Python syntax: {error}"))
            continue
        checked_types = (tokenize.STRING, tokenize.COMMENT, tokenize.FSTRING_MIDDLE)
        for token in tokenize.generate_tokens(StringIO(source).readline):
            if token.type not in checked_types:
                continue
            if non_english_letters(token.string):
                result.append((index, f"Localize {tokenize.tok_name[token.type]} at line {token.start[0]}"))
    return result


def main():
    base = Path(__file__).resolve().parents[1] / "notebooks"
    issues = [(path.relative_to(base), cell, detail)
              for path in sorted(base.rglob("*.ipynb"))
              for cell, detail in inspect(path)]
    for path, cell, detail in issues:
        print(f"{path}: cell {cell}: {detail}")
    print(f"Notebook publication issues: {len(issues)}")
    return bool(issues)


if __name__ == "__main__":
    sys.exit(main())
