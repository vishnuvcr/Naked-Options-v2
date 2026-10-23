# QE-NOB-3.0 error and source-failure log

Only observed errors and deviations belong here. Do not store credentials or hidden reasoning.

| ID | Date | Severity | Event | Correction / action | Status |
|---|---|---|---|---|---|
| QE-NOB3-E001 | 2026-10-23 | HIGH | QE-NOB-2.0 lacked stable dated contract identity and executable quote evidence, so old OOS cannot be reused to select new rules. | New protocol prohibits reuse of the old OOS period; fresh-data gate precedes empirical testing. | OPEN — data feasibility not yet verified |

| QE-NOB3-E002 | 2026-10-23 | HIGH | Fresh empirical testing is blocked pending authentication and untouched-data eligibility. | Repository secret values cannot be inspected through this integration; old OOS has already been examined. | Added branch-scoped regression workflow with manual trigger; do not claim workflow pass until run result is checked. | OPEN — auth and data gates pending |
| QE-NOB3-E003 | 2026-10-23 | MEDIUM | Actions execution result for the new regression workflow was not retrievable through available GitHub tools. | Integration exposes run/job artifact readers but no reliable workflow-dispatch/list operation for this branch. | Workflow is committed with push and manual triggers; verify its run in GitHub Actions UI/API before proceeding. | OPEN — workflow result unverified |

| QE-NOB3-E004 | 2026-10-23 | LOW | Initial data-probe workflow artifact path did not match the source client's configured report directory. | Inspected `run_research.py` constants and corrected artifact path to `reports/quant_evolve_nob_v2/source_probe.json` in commit `22440705cf416c7ece6d87bcc9245059ff996d1e`. | Corrected; workflow execution still unverified |

| QE-NOB3-E005 | 2026-10-23 | LOW | Regression test failed because its expected sentence did not exactly match the plan's actual wording; all other tests in the run passed (25 passed, 1 failed). | Screenshot-confirmed failure at `test_run_research.py:320`; replaced the brittle sentence assertion with the exact preregistered phrase already present in the plan. Commit `79a81636803ba56f2aea638368a91e703504809e`. | Fix committed; awaiting automatic workflow rerun and verification |

| QE-NOB3-E006 | 2026-10-23 | INFO | Post-fix regression workflow and bounded source probe were verified successful. | Regression run `39913031868` passed; probe run `39912434371` passed, with sanitized artifact `12482469675`. Probe observed weekly source 728 rows and underlying probe 709 rows. | Closed for workflow wiring; full fresh-data eligibility remains open |

| QE-NOB3-E007 | 2026-10-23 | HIGH | The strict fresh-data gate rejected the current rolling option payload for strategy research. | Workflow run `39933612441` completed technically, but audit output was `BLOCKED_DATA_LIMITED`; 746 underlying rows and 765 rolling-option rows; no stable dated contract identity fields or executable bid/ask quote fields. | Keep strategy discovery blocked. Investigate alternative legitimate dated-contract data sources and validate historical coverage and execution evidence before retesting. | OPEN — data eligibility blocker |

| QE-NOB3-E008 | 2026-10-23 | MEDIUM | Initial source gate does not establish historical executable bid/ask or stable dated contract identity. | Reviewed Dhan rolling endpoint documentation and official NSE contract-wise/bhavcopy report pages; documented the distinction between daily contract records and intraday execution evidence in `ALTERNATIVE_DATA_SOURCE_AUDIT_V3.md`. | OPEN — implement bounded free-source coverage/identity validation; do not start strategy search yet |

| QE-NOB3-E009 | 2026-10-24 | MEDIUM | Existing source research identified official NSE daily F&O archives, but no automated sample schema test had been run. | Added a bounded probe using the documented UDiFF archive naming convention; it tests up to three recent weekdays, stores only public compressed sample archives and a schema/count manifest, and never substitutes daily closes for intraday fills. | OPEN — wait for workflow result and inspect schema report |

| QE-NOB3-E010 | 2026-10-24 | INFO | Official NSE daily archive route was unverified for this repository's own client before the latest step. | Workflow `40009611140` fetched three daily UDiFF archives; all had expected daily NIFTY option fields, with 5,865–5,941 detected NIFTY option rows per day. Regression run `40009667755` passed. Artifact `12526450061` preserves samples and report. | Closed for daily schema feasibility; intraday execution/contract mapping gap remains open |

| QE-NOB3-E011 | 2026-10-24 | INFO | Bounded source-feasibility phase reached its preregistered stopping condition. | NSE daily schema sample passed for three archives; strict Dhan rolling payload audit lacks stable dated contract identity and bid/ask fields; full coverage and executable fills are not established. Published `FINAL_RESEARCH_MANUSCRIPT_V3.md`. | CLOSED — DATA-LIMITED; Phases 2–6 intentionally not started |
