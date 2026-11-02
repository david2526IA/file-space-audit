from __future__ import annotations

import argparse
import json
from pathlib import Path

from .audit import audit


def main() -> None:
    parser = argparse.ArgumentParser(description="Read-only inventory and duplicate-file analysis.")
    parser.add_argument("directory", type=Path)
    parser.add_argument("--output", type=Path, default=Path("space_audit.json"))
    args = parser.parse_args()
    report = audit(args.directory)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("files", "total_bytes", "potentially_recoverable_bytes")}))
