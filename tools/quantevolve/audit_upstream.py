#!/usr/bin/env python3
"""Static compatibility audit for upstream QuantEvolve; never executes generated strategies."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_value(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = args.upstream.resolve()
    required = ["README.md", "LICENSE", "pyproject.toml", "configs/quantevolve_config.yaml"]
    missing = [item for item in required if not (root / item).is_file()]
    if missing:
        raise SystemExit(f"Required upstream files missing: {missing}")

    readme = (root / "README.md").read_text(encoding="utf-8", errors="replace")
    config_path = root / "configs/quantevolve_config.yaml"
    config = config_path.read_text(encoding="utf-8", errors="replace")
    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8", errors="replace")
    license_text = (root / "LICENSE").read_text(encoding="utf-8", errors="replace")
    sha = git_value(root, "rev-parse", "HEAD")
    findings = [
        {
            "id": "QE-AUDIT-001",
            "severity": "HIGH",
            "finding": "Upstream documentation/config references Binance data and defaults to BTCUSDT.",
            "evidence": {
                "readme_mentions_binance": "binance" in readme.lower(),
                "config_mentions_binance": "binance" in config.lower(),
                "config_defaults_btcusdt": "BTCUSDT" in config,
            },
            "required_action": "Replace collector/evaluator assumptions with a validated NIFTY adapter; do not use upstream backtest scores as NSE evidence.",
        },
        {
            "id": "QE-AUDIT-002",
            "severity": "HIGH",
            "finding": "LLM-generated candidate code is untrusted and requires isolation from secrets and repository-write credentials.",
            "evidence": {"gemini_config_present": "llm:" in config and "gemini" in config.lower()},
            "required_action": "Generation and candidate execution must be separate least-privilege steps; candidate execution receives no API secrets.",
        },
        {
            "id": "QE-AUDIT-003",
            "severity": "HIGH",
            "finding": "Default search settings are too large to adopt without an explicit research budget.",
            "evidence": {
                "default_200_iterations": "max_iterations: 200" in config,
                "default_population_50": "population_size: 50" in config,
            },
            "required_action": "Set finite iterations, population, wall time, model-call limits, fixed seed, and checkpoint interval before any LLM run.",
        },
        {
            "id": "QE-AUDIT-004",
            "severity": "HIGH",
            "finding": "The generic buy/sell/hold signal interface does not establish exact option-contract identity, fills, fees, or slippage.",
            "evidence": {"readme_describes_ohlcv": "ohlcv" in readme.lower(), "license_apache_2": "apache license" in license_text.lower() or "apache-2.0" in pyproject.lower()},
            "required_action": "Create a separate options evaluator with exact expiry/strike/type identity and verified Indian fee/slippage arithmetic.",
        },
    ]
    report = {
        "schema_version": 1,
        "audit_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "upstream_url": "https://github.com/tarsyang/quantevolve",
        "upstream_commit": sha,
        "license_indicator": "Apache-2.0 declared in pyproject; verify attribution and retain license on any vendoring",
        "source_hashes": {
            "README.md": sha256(root / "README.md"),
            "LICENSE": sha256(root / "LICENSE"),
            "pyproject.toml": sha256(root / "pyproject.toml"),
            "configs/quantevolve_config.yaml": sha256(config_path),
        },
        "status": "AUDIT_ONLY_NO_PERFORMANCE_RUN",
        "google_api_key_configured": bool(os.environ.get("GOOGLE_API_KEY")),
        "findings": findings,
        "performance_claim": None,
        "next_gate": "P1 reproducible integration shell; no NIFTY/options performance inference is authorized",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "upstream_commit": sha,
        "finding_count": len(findings),
        "google_api_key_configured": report["google_api_key_configured"],
        "output": str(args.output),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
