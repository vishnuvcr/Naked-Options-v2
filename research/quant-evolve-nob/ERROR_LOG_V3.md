# QE-NOB-3.0 error and source-failure log

Only observed errors and deviations belong here. Do not store credentials or hidden reasoning.

| ID | Date | Severity | Event | Correction / action | Status |
|---|---|---|---|---|---|
| QE-NOB3-E001 | 2026-10-23 | HIGH | QE-NOB-2.0 lacked stable dated contract identity and executable quote evidence, so old OOS cannot be reused to select new rules. | New protocol prohibits reuse of the old OOS period; fresh-data gate precedes empirical testing. | OPEN — data feasibility not yet verified |

| QE-NOB3-E002 | 2026-10-23 | HIGH | Fresh empirical testing is blocked pending authentication and untouched-data eligibility. | Repository secret values cannot be inspected through this integration; old OOS has already been examined. | Added branch-scoped regression workflow with manual trigger; do not claim workflow pass until run result is checked. | OPEN — auth and data gates pending |
| QE-NOB3-E003 | 2026-10-23 | MEDIUM | Actions execution result for the new regression workflow was not retrievable through available GitHub tools. | Integration exposes run/job artifact readers but no reliable workflow-dispatch/list operation for this branch. | Workflow is committed with push and manual triggers; verify its run in GitHub Actions UI/API before proceeding. | OPEN — workflow result unverified |

| QE-NOB3-E004 | 2026-10-23 | LOW | Initial data-probe workflow artifact path did not match the source client's configured report directory. | Inspected `run_research.py` constants and corrected artifact path to `reports/quant_evolve_nob_v2/source_probe.json` in commit `22440705cf416c7ece6d87bcc9245059ff996d1e`. | Corrected; workflow execution still unverified |

| QE-NOB3-E005 | 2026-10-23 | LOW | Regression test failed because its expected sentence did not exactly match the plan's actual wording; all other tests in the run passed (25 passed, 1 failed). | Screenshot-confirmed failure at `test_run_research.py:320`; replaced the brittle sentence assertion with the exact preregistered phrase already present in the plan. Commit `79a81636803ba56f2aea638368a91e703504809e`. | Fix committed; awaiting automatic workflow rerun and verification |
