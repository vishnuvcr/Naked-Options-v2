import subprocess
import sys
from pathlib import Path


def test_audit_script_is_syntax_valid():
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", "tools/quantevolve/audit_upstream.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_workflow_has_safe_triggers_and_read_only_permissions():
    workflow = Path(".github/workflows/quantevolve-integration-audit.yml").read_text()
    assert "workflow_dispatch:" in workflow
    assert "schedule:" in workflow
    assert "permissions:" in workflow and "contents: read" in workflow
    assert "persist-credentials: false" in workflow
    assert "upload-artifact@v4" in workflow


def test_plan_separates_prediction_and_options_and_blocks_unverified_pnl():
    plan = Path("research/QUANTEvolve_INTEGRATION_PLAN.md").read_text()
    assert "separate experimental tracks" in plan
    assert "final holdout" in plan and "before evolution" in plan
    assert "Never run LLM-generated code with repository write credentials" in plan
    assert "Do not use the upstream Binance BTC/USDT evaluator unchanged" in plan
    policy = Path("research/EXECUTION_POLICY.md").read_text().lower()
    assert "independent tester/review branch or sign-off is required" in policy
