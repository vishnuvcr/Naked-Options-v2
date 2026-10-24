#!/usr/bin/env python3
"""Quarantine the old ambiguous 5-minute cache path before source-specific acquisition."""
from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path("data/cache/zigzag_expiry_direction")
LEGACY = ROOT / "nifty50_5m.csv"
REPORT = Path("reports/zigzag_legacy_5m_cache_migration.json")


def migrate(root: Path = ROOT) -> dict:
    legacy = root / LEGACY.name
    report = {
        "status": "NO_LEGACY_FILE",
        "legacy_path": str(legacy),
        "source_identity": "UNKNOWN_OLD_MIXED_SOURCE",
        "raw_file_modified": False,
        "note": (
            "Older workflow runs reused the same 5m filename for Dhan, Yahoo, and "
            "the public archive. This file is not used as a verified source."
        ),
    }
    if not legacy.exists():
        return report
    digest = hashlib.sha256(legacy.read_bytes()).hexdigest()
    destination = root / f"nifty50_5m_legacy_unverified_{digest[:12]}.csv"
    if destination.exists():
        existing = hashlib.sha256(destination.read_bytes()).hexdigest()
        if existing != digest:
            raise RuntimeError("Legacy 5m quarantine target exists but has a different hash")
    else:
        shutil.copy2(legacy, destination)
    legacy.unlink()
    report.update({
        "status": "QUARANTINED",
        "legacy_sha256": digest,
        "quarantined_path": str(destination),
        "quarantined_sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
        "bytes": destination.stat().st_size,
        "raw_file_modified": False,
        "legacy_path_removed_from_active_namespace": True,
    })
    return report


def main() -> int:
    report = migrate()
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
