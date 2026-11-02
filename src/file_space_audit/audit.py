"""Hash files only when needed and never modify the scanned directory."""

from __future__ import annotations

import hashlib
from collections import defaultdict
from pathlib import Path
from typing import Any


def _digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            hasher.update(chunk)
    return hasher.hexdigest()


def audit(root: Path) -> dict[str, Any]:
    """Inventory ordinary files below *root* and identify byte-identical copies."""
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"not a directory: {root}")
    by_size: dict[int, list[Path]] = defaultdict(list)
    skipped: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.is_symlink():
            continue
        try:
            by_size[path.stat().st_size].append(path)
        except OSError:
            skipped.append(str(path.relative_to(root)))
    groups = []
    for size, paths in by_size.items():
        if len(paths) < 2:
            continue
        by_hash: dict[str, list[Path]] = defaultdict(list)
        for path in paths:
            try:
                by_hash[_digest(path)].append(path)
            except OSError:
                skipped.append(str(path.relative_to(root)))
        for digest, copies in by_hash.items():
            if len(copies) > 1:
                groups.append({"sha256": digest, "size_bytes": size, "copies": [str(path.relative_to(root)) for path in sorted(copies)], "recoverable_bytes": size * (len(copies) - 1)})
    files = sum(len(paths) for paths in by_size.values())
    total = sum(size * len(paths) for size, paths in by_size.items())
    return {"root": str(root), "files": files, "total_bytes": total, "duplicate_groups": sorted(groups, key=lambda group: group["recoverable_bytes"], reverse=True), "potentially_recoverable_bytes": sum(group["recoverable_bytes"] for group in groups), "skipped": sorted(set(skipped)), "scope": "read-only analysis; review duplicate groups manually before any deletion"}
