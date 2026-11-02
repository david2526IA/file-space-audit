# File Space Audit

A read-only local disk inventory tool that detects byte-identical duplicate files using SHA-256 hashes and estimates potentially recoverable space.

It never deletes, moves or alters files. The output is a JSON report intended to support a manual review.

## Run

```bash
pip install .
file-space-audit /path/to/folder --output space_audit.json
```

The tool first groups files by size and hashes only candidates with matching sizes, avoiding unnecessary reads. It ignores symlinks and reports files it could not access.

## Safety

Duplicate bytes do not automatically mean duplicate value: users should inspect paths and retain the appropriate copy before any deletion. This project deliberately has no deletion option.

## Development

```bash
pip install ".[dev]"
pytest -q
```

## License

MIT
