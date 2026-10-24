#!/usr/bin/env python3
"""Bounded integration smoke audit for the seven vendored research projects.

This script never runs an external agent, contacts paid LLM APIs, or submits orders.
It checks pinned submodule presence and records dependency/API availability. Numerical
claims continue to come only from the deterministic benchmark scripts.
"""
from __future__ import annotations
import importlib.metadata as metadata
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
VENDOR = ROOT / "vendor" / "research-repositories"
OUT = ROOT / "reports" / "nifty-prediction" / "repository_integration_audit.json"
REPOS = {
    "quantevolve": {"url": "https://github.com/tarsyang/quantevolve", "mode": "bounded-search-design-only"},
    "TradingAgents": {"url": "https://github.com/TauricResearch/TradingAgents", "mode": "evidence-hypothesis-workflow-only"},
    "astra-quant-agent": {"url": "https://github.com/0xethanq/astra-quant-agent", "mode": "risk-control-reference-only"},
    "PySR": {"url": "https://github.com/astroautomata/PySR", "mode": "optional-symbolic-regression"},
    "arch": {"url": "https://github.com/bashtage/arch", "mode": "garch-volatility-forecast"},
    "tick": {"url": "https://github.com/X-DataInitiative/tick", "mode": "optional-regularized-model-compatibility"},
    "MAPIE": {"url": "https://github.com/scikit-learn-contrib/MAPIE", "mode": "optional-uncertainty-calibration"},
}
PACKAGES = {"arch": "arch", "PySR": "pysr", "tick": "tick", "MAPIE": "mapie", "scikit-learn": "scikit-learn"}

def main():
    results = {}
    for name, spec in REPOS.items():
        path = VENDOR / name
        exists = path.exists()
        # The GitHub contents API represents submodule pointers as zero-byte files;
        # locally the directory is populated when checkout uses submodules: true.
        pinned_sha = None
        if exists:
            try:
                pinned_sha = subprocess.check_output(
                    ["git", "-C", str(path), "rev-parse", "HEAD"], text=True, stderr=subprocess.DEVNULL
                ).strip()
            except Exception:
                pass
        results[name] = {
            **spec, "local_checkout_present": bool(exists and pinned_sha),
            "pinned_commit": pinned_sha,
            "status": "CHECKED_OUT" if pinned_sha else "PINNED_SUBMODULE_ONLY",
        }
    versions = {}
    for package in PACKAGES:
        try:
            versions[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            versions[package] = None
    result = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "AUDIT_ONLY_NO_EXTERNAL_AGENT_EXECUTION",
        "repositories": results,
        "installed_package_versions": versions,
        "pipeline_contract": {
            "prediction_target": "next-session NIFTY 50 spot direction",
            "feature_timing": "features available through close of session t only",
            "evaluation": "chronological; deterministic baseline metrics remain authoritative",
            "agent_outputs_are_labels": False,
            "live_order_execution_enabled": False,
            "holdout_tuning_allowed": False,
        },
        "notes": [
            "A pinned submodule pointer proves provenance, not empirical integration.",
            "Quantevolve and TradingAgents are not invoked; no API keys or paid LLM calls are made.",
            "AstraQuant's exchange-specific crypto executor is intentionally not imported into NSE/NFO.",
            "PySR and tick require separate compatibility-gated experiments before model inclusion.",
            "MAPIE requires a chronological calibration experiment before uncertainty outputs can be used.",
            "arch GARCH forecast experiment is run separately by evaluate_volatility_forecast.py.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    # Do not fail core benchmark merely because optional repositories/packages are absent.
    if len(results) != 7:
        raise SystemExit("Repository integration audit did not enumerate all seven projects")

if __name__ == "__main__":
    main()
