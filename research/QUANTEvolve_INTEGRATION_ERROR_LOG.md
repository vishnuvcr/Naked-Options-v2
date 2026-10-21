# QuantEvolve integration audit log

## QE-ERR-001 — upstream evaluator/data assumptions
- **Date:** 2026-10-22
- **Severity:** HIGH
- **Observation:** Upstream README and default config describe Binance OHLCV collection and default BTCUSDT 1h data. The evaluator's documented signal interface is a generic buy/sell/hold series, not an NSE options contract/order ledger.
- **Risk:** Running the upstream pipeline unchanged would not constitute NIFTY prediction research or an executable options backtest and could create false confidence from a mismatched market/data model.
- **Action:** Do not execute the upstream default collector/evaluator for research results. Require separate NIFTY prediction and options adapters, frozen gates, and explicit cost/statistical evaluation.
- **Status:** OPEN — addressed at design level; implementation/test gates pending.

## QE-ERR-002 — evolutionary multiple-testing and holdout leakage
- **Date:** 2026-10-22
- **Severity:** HIGH
- **Observation:** Evolutionary search repeatedly generates candidates based on previous fitness feedback. A naive final score can be overfit by repeated adaptive selection even when each individual backtest is chronologically ordered.
- **Risk:** Final performance may be optimistic if the holdout informs prompts, fitness, selection, or retries.
- **Action:** Reserve a sealed final holdout; use development-only walk-forward folds for fitness; cap iterations/API budget; record all candidates and correct the final comparison family.
- **Status:** OPEN — design gate; implementation pending.

## QE-ERR-003 — credential isolation
- **Date:** 2026-10-22
- **Severity:** HIGH
- **Observation:** QuantEvolve requires `GOOGLE_API_KEY` for Gemini generation. Generated strategy code is untrusted code and must not run in a process that has secrets or repository write permissions.
- **Risk:** Accidental disclosure, unsafe generated code, or unintended repository changes.
- **Action:** Keep secret use limited to the generation client in a restricted job; execute candidate code in a separate low-privilege/no-secret process. Do not expose Dhan/HF tokens to candidate execution. Log only whether a secret is configured, never its value.
- **Status:** OPEN — security architecture must be implemented and tested.

## QE-ERR-004 — no performance evidence
- **Date:** 2026-10-22
- **Severity:** MEDIUM
- **Observation:** Repository/upstream source audit only; no adapted NIFTY data run or verified out-of-sample candidate evaluation has been executed.
- **Risk:** Treating integration as validated strategy research would overstate the evidence.
- **Action:** All current performance fields remain NOT RUN. No strategy/model is endorsed.
- **Status:** CLOSED AS DOCUMENTED LIMITATION; revisit only after P2/P4 gates.

## Scope and audit note
This log records visible technical findings and corrective actions. It does not include private chain-of-thought or hidden reasoning.


## QE-ERR-005 — audit job initially referenced LLM secret unnecessarily
- **Date:** 2026-10-22
- **Severity:** LOW
- **Observation:** First workflow draft passed `GOOGLE_API_KEY` into a source-audit-only process even though no LLM call is needed.
- **Correction:** Removed the secret environment mapping; the audit workflow has read-only repository permissions and checkout credentials disabled.
- **Status:** RESOLVED — workflow source updated; verify in Actions run.

## Step record — audit scaffold committed
- **Date:** 2026-10-22
- **Branch:** `research/quantevolve-integration`
- **Files added:** integration plan, phase status, error log, static upstream audit script, GitHub Actions audit workflow, governance tests.
- **Execution result:** Source-audit workflow runs succeeded; [run 39662117061](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39662117061) completed successfully for the committed source-audit/policy state. A later workflow edit added pytest governance checks; that revised version still requires its own verified run.
- **Research status:** no NIFTY prediction experiment, options backtest, or out-of-sample performance run has been performed.


## QE-ERR-006 — LLM secret readiness is user-reported, not runtime-verified
- **Date:** 2026-10-22
- **Severity:** LOW
- **Observation:** User reports adding `GOOGLE_API_KEY` as a repository Actions secret. The source-audit job deliberately does not use it, and this integration cannot read the secret value or prove that Gemini authentication/quota is valid.
- **Action:** Record it as available by user report; test it only in the bounded generation step when that step is implemented. Keep values out of logs and artifacts; generation credentials must not be exposed to candidate execution.
- **Status:** USER-REPORTED CONFIGURATION; runtime validation pending.

## QE-STEP-006 — core instructions updated
- **Date:** 2026-10-22
- **Branch:** `research/quantevolve-integration`
- **Change:** Added QuantEvolve-specific credential isolation, bounded-cost, sealed-holdout and no-independent-review instructions to `research/EXECUTION_POLICY.md`; reconciled plan/status/error-log text.
- **User governance instruction:** no review needed; do not create a tester handoff for this integration.
- **Performance status:** no QuantEvolve prediction or options performance has been run or claimed.


## QE-STEP-007 — automated test gate added to audit workflow
- **Date:** 2026-10-22
- **Change:** The workflow now installs pytest and runs `tests/test_quantevolve_integration_protocol.py` before fetching/auditing upstream. Trigger filters focus on source code, the protocol tests, and the workflow itself rather than every documentation-only edit.
- **Verification:** Source audit succeeded in previous runs, but the revised workflow containing this test step has not yet been verified to pass. Record as pending rather than assuming success.
- **Review policy:** No independent review/tester handoff will be created, per the user's instruction. Automated checks remain required.


## QE-ERR-007 — assertion wording mismatch in governance tests
- Date: 2026-10-22
- Severity: LOW
- Observed workflow: [run 39662185936](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39662185936).
- Observation: the test required the exact phrase “sealed final holdout,” while the plan says “Freeze a time-based final holdout before evolution.” Two of three tests passed; the failure happened before upstream clone or model execution.
- Correction: assert the actual protocol safeguard semantically by checking that the plan mentions the final holdout and that it is kept out of evolution. Expanded adapter tests also cover literal-only parsing, coefficient/feature limits, causal normalization, final-holdout separation, bootstrap metrics and a source manifest gate.
- Status: CORRECTED IN BRANCH; next hosted run must verify.

## QE-STEP-008 — adapter and bounded workflow implementation
- Date: 2026-10-22
- Upstream pin: 2df1e85758620e8ac0ca88ffc428b379d6cb9620.
- Implemented: safe declarative candidate schema; trusted causal forecasting evaluator; modern Google Gen AI wrapper; maximum four evolution iterations; option-data provenance/contract quality gate; artifact allowlist publisher; automated/manual GitHub Actions research workflow.
- Security: candidate source is parsed only and never executed/imported. The generation job receives GOOGLE_API_KEY; the evaluation and publication steps do not. Raw market data, generated source, logs and checkpoints are not copied into public artifacts or the repository.
- Verification: this commit creates the implementation files, but its hosted test/evolution run is not yet verified. No QuantEvolve-derived performance claim is made.

## QE-DELIVERY-39665389015 — automated run record
- Date: 2026-10-21T19:53:08.803176+00:00
- Run status: BLOCKED_AUTOMATED_TESTS
- Reason/error classification: integration test gate did not pass
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.


## QE-ERR-008 — review-policy test checked the wrong file
- Date: 2026-10-22. Severity: LOW.
- Workflow: [bounded run 39665389015](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39665389015) and [audit run 39665388985](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39665388985).
- Observation: 9 adapter/protocol tests passed and 1 protocol assertion failed because it looked for the no-review instruction in the plan instead of the core execution policy. Data acquisition/validation passed, and the workflow correctly stopped before any Gemini generation request.
- Correction: assert the no-review directive in research/EXECUTION_POLICY.md; both workflows now trigger for QE test-file edits.
- Status: corrected; subsequent run 39665689705 passed source-audit and the bounded research run's combined test step passed all 10 tests.

## QE-ERR-009 — expected holdout status did not match the runner validator
- Date: 2026-10-22. Severity: HIGH (result disposition), not a forecast-metric defect.
- Workflow: [bounded run 39665689785](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39665689785).
- Observation: development report status PASS and holdout status PREDICTION_HOLDOUT_EVALUATED were both emitted, but the runner incorrectly required every stage to be PASS. It marked the run HOLDOUT_REPORT_INVALID after valid metric files had already been written.
- Correction: runner now expects PASS for development and PREDICTION_HOLDOUT_EVALUATED for holdout. A constrained reconciliation validated the persisted report bundle's data/source hashes, selected-spec identity, holdout sample size, selection flag, MAE-skill formula, and confidence interval ordering before correcting only the manifest status label. The metrics were not rerun.
- Status: reconciled in the repository; future runner uses the corrected expected status and keeps generated source/checkpoints outside public artifacts.

## QE-ERR-010 — direction accuracy was reported for a zero-return forecast
- Date: 2026-10-22. Severity: MEDIUM (metric interpretation).
- Observation: selected specification has zero intercept and every coefficient zero, so every forecast equals zero. Counting the sign of zero forecast as matching the actual return produces a near-zero numeric “direction accuracy” that is not a meaningful directional evaluation.
- Correction: direction accuracy is now null/undefined when there are no non-zero predictions; reports also include directional prediction count and coverage. The persisted report was corrected from the known zero specification (directional coverage 0, directional accuracy undefined).
- Status: code corrected and new regression test added; hosted test result pending.

## QE-ERR-011 — upstream generated files initially shared the reports directory
- Date: 2026-10-22. Severity: MEDIUM (artifact hygiene).
- Observation: the earlier runner passed the tracked reports directory as upstream's working output and returned early on the status mismatch before its cleanup step. The artifact contained more files than the intended sanitized report allowlist, so generated code/checkpoint files may have been included in that run's downloadable artifact. They were not committed to the repository by the publisher, and no secret was written to the code or reports.
- Correction: the upstream controller now writes its temporary strategy files/checkpoints/logs under /tmp. Only allowlisted JSON summaries can appear under reports/quantevolve; the publisher receives the sanitised JSON artifact only.
- Status: future path corrected; the previous workflow artifact remains governed by GitHub artifact retention because this integration has no artifact-delete action.

## QE-ERR-012 — documentation batch incorrectly used an unset content property
- Date: 2026-10-22. Severity: MEDIUM (audit-trail integrity).
- Observation: one multi-file metadata update wrote the literal word “undefined” at the start of README.md, EXPERIMENT_LOG.md, QUANTEvolve_INTEGRATION_STATUS.md, and QUANTEvolve_INTEGRATION_ERROR_LOG.md.
- Correction: restored these files from the immediately preceding valid commit, reapplied the factual run/error appendices to their full source content, and verified each resulting file no longer starts with “undefined”.
- Status: corrected in this commit; check latest file contents after merge/commit.

## QE-DELIVERY-39666799180 — automated run record
- Date: 2026-10-21T20:03:03.004060+00:00
- Run status: LLM_EVOLUTION_NOT_REQUESTED
- Reason/error classification: automatic workflow ran offline gate only; no model-generation API call was requested
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.

## QE-DELIVERY-39667156299 — automated run record
- Date: 2026-10-21T20:07:02.694500+00:00
- Run status: PREDICTION_HOLDOUT_EVALUATED
- Reason/error classification: No runtime error reported in the sanitized manifest.
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.


## QE-ERR-013 — bounded controller run lacked provider-call success telemetry
- Date: 2026-10-22. Severity: MEDIUM (LLM run reproducibility).
- Observation: Both bounded four-iteration controller runs selected the zero-return specification. Saved manifests did not record whether a successful Gemini response was received, so the controller run cannot be used as evidence that LLM mutations occurred.
- Correction: provider records only model name, request attempts/successes/failures and exception-class counts to a run-local audit file; runner requires at least one successful generation response before labeling a run as LLM evolution. No prompts, responses, API key or raw provider error text are captured.
- Status: code and a regression assertion committed; future manually enabled LLM run must verify call counters. Automatic request is reset to offline so code pushes will not spend API quota.

## QE-ERR-014 — options source/contract acquisition remains unverified
- Date: 2026-10-22. Severity: HIGH (options experiment blocked at source gate).
- Observation: the current workflow workspace has no licensed options dataset file and source manifest at the required paths. Existing earlier HF contract audit run 38807375042 was cancelled before its audit stage; it cannot be treated as successful.
- Correction: continue finite free-source checks using the publicly documented HF NIFTY options archive and NSE official UDiFF/contract files. Keep raw CC-BY-NC source data in the cache/acquisition runtime, not Git-tracked artifacts. Write a sanitized provenance/schema/expiry/lot-size report. Do not compute P&L or optimize candidates unless source and contract gates pass.
- Status: OPEN — source acquisition and official reconciliation phase next.

## QE-DELIVERY-39667767456 — automated run record
- Date: 2026-10-21T20:09:34.577276+00:00
- Run status: LLM_EVOLUTION_NOT_REQUESTED
- Reason/error classification: automatic workflow ran offline gate only; no model-generation API call was requested
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.

## QE-DELIVERY-39667889681 — automated run record
- Date: 2026-10-21T20:10:29.755713+00:00
- Run status: BLOCKED_AUTOMATED_TESTS
- Reason/error classification: integration test gate did not pass
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.


## QE-ERR-015 — telemetry unit test imported upstream-only package
- Date: 2026-10-22. Severity: LOW (test isolation).
- Workflow: [audit run 39667889731](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39667889731).
- Observation: 12 tests passed and one new telemetry-counter test failed because the audit job intentionally does not install the upstream `quantevolve` package; importing the provider module pulled in `quantevolve.config`.
- Correction: the test now AST-extracts only the telemetry function and runs it with explicit standard-library dependencies, testing cumulative JSON counters without requiring the upstream package or making network/API calls.
- Status: corrected; tests passed in [39668092561](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39668092561) and later audits [39669940816](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39669940816), [39670352181](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39670352181).

## QE-DELIVERY-39668093032 — automated run record
- Date: 2026-10-21T20:12:02.681024+00:00
- Run status: LLM_EVOLUTION_NOT_REQUESTED
- Reason/error classification: automatic workflow ran offline gate only; no model-generation API call was requested
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.

## QE-DELIVERY-39668183031 — automated run record
- Date: 2026-10-21T20:16:51.439416+00:00
- Run status: EVOLUTION_NO_SUCCESSFUL_LLM_RESPONSES
- Reason/error classification: controller returned without a verified successful Gemini generation response
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.


## QE-ERR-016 — Gemini generation requests did not succeed
- Date: 2026-10-22. Severity: MEDIUM (LLM candidate generation unavailable).
- Workflow: [run 39668183031](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39668183031).
- Observation: data validation and integration tests passed, but all four bounded generation attempts failed: three `TimeoutError` and one `ServerError`; successful responses=0. The runner correctly emitted `EVOLUTION_NO_SUCCESSFUL_LLM_RESPONSES` and did not score a candidate or claim prediction performance.
- Model availability check: the configured `gemini-3.8-flash` endpoint is listed as a stable Gemini API model in Google's current model documentation. This does not prove the API key has quota or that the service was available during the run.
- Correction/next step: make one bounded one-iteration retry with the listed stable `gemini-3.6-flash` model to distinguish a transient model/service issue from a general credential/quota/network issue. If it fails, stop further API retries and keep offline gates active until an explicit configuration change.
- Status: first attempt logged; fallback run pending. No prompts, response bodies, key, or raw provider errors stored.

## QE-DELIVERY-39669107291 — automated run record
- Date: 2026-10-21T20:19:04.095512+00:00
- Run status: EVOLUTION_NO_SUCCESSFUL_LLM_RESPONSES
- Reason/error classification: controller returned without a verified successful Gemini generation response
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.

## QE-DELIVERY-39669141475 — automated run record
- Date: 2026-10-21T20:19:45.272070+00:00
- Run status: LLM_EVOLUTION_NOT_REQUESTED
- Reason/error classification: automatic workflow ran offline gate only; no model-generation API call was requested
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.


## QE-ERR-017 — final bounded fallback generation also failed
- Date: 2026-10-22. Severity: MEDIUM (candidate generation unavailable).
- Workflow: [run 39669107291](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39669107291).
- Observation: a one-iteration diagnostic using the listed stable `gemini-3.6-flash` model produced one request, zero successes, and one `ServerError`. No candidate was selected or scored. This followed the four-attempt `gemini-3.8-flash` run (three timeouts, one server error).
- Disposition: stop API retries for this research run to avoid unbounded spend. Keep LLM evolution disabled by default; continue offline integration tests and options-source acquisition. A future LLM run requires an explicit manual dispatch after API availability/quota is checked.
- Status: bounded diagnostic complete; LLM evolution BLOCKED_NO_SUCCESSFUL_RESPONSES. No performance result is claimed.

## QE-ERR-018 — fallback model label in run manifest was hard-coded
- Date: 2026-10-22. Severity: LOW (provenance accuracy).
- Observation: run 39669107291's sanitized telemetry correctly reported `gemini-3.6-flash`, but the top-level manifest model label retained the default `gemini-3.8-flash`.
- Correction: runner now reads the model name from the pinned YAML config when constructing the manifest. The default config is restored to `gemini-3.8-flash`; the fallback diagnostic remains recorded as `gemini-3.6-flash` in the original telemetry.
- Status: corrected in code; source audit pending.

## QE-DELIVERY-39669633087 — automated run record
- Date: 2026-10-21T20:22:22.795946+00:00
- Run status: LLM_EVOLUTION_NOT_REQUESTED
- Reason/error classification: automatic workflow ran offline gate only; no model-generation API call was requested
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.

## QE-DELIVERY-39669708490 — automated run record
- Date: 2026-10-21T20:23:18.221112+00:00
- Run status: NO_RUN_MANIFEST
- Reason/error classification: No runtime error reported in the sanitized manifest.
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.


## QE-ERR-019 — options source audit ran but publisher omitted its report
- Date: 2026-10-22. Severity: MEDIUM (evidence publication).
- Workflow: [options-source run 39669708490](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39669708490).
- Observation: the bounded source audit and options gate steps both completed successfully, but the sanitized report was not committed because the publisher allowlist only copied files adjacent to a run manifest and did not include the top-level `options_source_audit.json`.
- Correction: publisher now explicitly allowlists and copies the sanitized options source audit report. Raw parquet remains in the cache and is not copied.
- Status: corrected; one bounded options-source audit rerun is required to persist the evidence.

## QE-DELIVERY-39670001128 — automated run record
- Date: 2026-10-21T20:25:04.924319+00:00
- Run status: NO_RUN_MANIFEST
- Reason/error classification: No runtime error reported in the sanitized manifest.
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.

## QE-DELIVERY-39670041315 — automated run record
- Date: 2026-10-21T20:25:42.699029+00:00
- Run status: LLM_EVOLUTION_NOT_REQUESTED
- Reason/error classification: automatic workflow ran offline gate only; no model-generation API call was requested
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.


## QE-ERR-020 — options source run was mislabeled by publisher
- Date: 2026-10-22. Severity: LOW (status classification).
- Workflows: [39669708490](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39669708490) and [39670001128](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39670001128).
- Observation: options-source workflows have no prediction run manifest; the publisher therefore logged NO_RUN_MANIFEST and used prediction-oriented wording even though the options audit step ran.
- Correction: options track now writes an explicit options run manifest, and publisher generates options-specific status summaries using the sanitized source report. Publisher allowlist includes options_source_audit.json.
- Status: corrected in workflow/publisher; source audit report now committed at reports/quantevolve/options_source_audit.json.


## QE-ERR-021 — report publisher lost a fast-forward race
- Date: 2026-10-22. Severity: MEDIUM (automatic publication reliability).
- Workflow: [run 39670338776](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39670338776).
- Observation: the research job completed, but the publisher's push was rejected because the branch advanced while the job was preparing its report commit.
- Correction: publisher now retries up to three times; on a non-fast-forward rejection it fetches the current branch, resets the workspace to that head, reruns the sanitized publisher from the downloaded artifact, and attempts a fresh commit. No force push is used.
- Status: correction committed; audit passed at [39670352181](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39670352181). A subsequent workflow run will verify the push-retry path.

## QE-DELIVERY-39670494972 — automated run record
- Date: 2026-10-21T20:28:30.360971+00:00
- Run status: LLM_EVOLUTION_NOT_REQUESTED
- Reason/error classification: automatic workflow ran offline gate only; no model-generation API call was requested
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.

## QE-DELIVERY-39671741090 — automated run record
- Date: 2026-10-21T20:36:59.137048+00:00
- Run status: LLM_EVOLUTION_NOT_REQUESTED
- Reason/error classification: automatic workflow ran offline gate only; no model-generation API call was requested
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.

## QE-DELIVERY-39671900967 — automated run record
- Date: 2026-10-21T20:38:06.559428+00:00
- Run status: BLOCKED_OFFICIAL_EXPIRY_AND_HISTORICAL_LOT_SIZE_UNVERIFIED
- Reason/error classification: No runtime error reported in the sanitized manifest.
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.


## QE-ERR-022 — circular-backed sample row checks omitted Pandas import
- Date: 2026-10-22. Severity: LOW (bounded source-audit implementation defect).
- Workflow: [options audit run 39671900967](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39671900967).
- Observation: the new row-level reconciliation raised `NameError` for each sampled file because the audit code used Pandas conversions without importing `pandas as pd`. The report therefore did not verify file expiry consistency, strikes, option type, or symbols.
- Correction: add the missing import and a regression assertion. Keep all source/contract and P&L gates blocked until a new run verifies the sample checks; no metrics or P&L were produced by the failed checks.
- Status: corrected in source; one bounded validation rerun pending.

## QE-DELIVERY-39672382046 — automated run record
- Date: 2026-10-21T20:41:43.644443+00:00
- Run status: BLOCKED_OFFICIAL_EXPIRY_AND_HISTORICAL_LOT_SIZE_UNVERIFIED
- Reason/error classification: No runtime error reported in the sanitized manifest.
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.

## QE-DELIVERY-39672476827 — automated run record
- Date: 2026-10-21T20:42:28.121600+00:00
- Run status: LLM_EVOLUTION_NOT_REQUESTED
- Reason/error classification: automatic workflow ran offline gate only; no model-generation API call was requested
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.

## QE-DELIVERY-39672831979 — automated run record
- Date: 2026-10-21T20:44:37.099025+00:00
- Run status: LLM_EVOLUTION_NOT_REQUESTED
- Reason/error classification: automatic workflow ran offline gate only; no model-generation API call was requested
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.


## QE-ERR-023 — Dhan probe test confused header name with credential leakage
- Date: 2026-10-22. Severity: LOW (test assertion).
- Observation: a new test initially asserted that the source must not contain the literal HTTP header key `access-token`. That header name is required to send the credential to Dhan; the safety requirement is that the secret value is never printed, persisted, or included in artifacts.
- Correction: assert the header value is passed from the token variable while retaining assertions that the response rows and raw text are not persisted.
- Status: test corrected in commit 9269422; latest automated run pending.

## QE-DELIVERY-39672923539 — automated run record
- Date: 2026-10-21T20:45:29.129229+00:00
- Run status: BLOCKED_AUTOMATED_TESTS
- Reason/error classification: integration test gate did not pass
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.


## QE-ERR-024 — Dhan API probe unit test omitted constant namespace
- Date: 2026-10-22. Severity: LOW (unit-test fixture defect).
- Workflow: [audit run 39672923582](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39672923582).
- Observation: the sanitized unit test extracted `inspect_response` via AST but initially omitted module constants (`API_URL`, `NIFTY_SECURITY_ID`, `FROM_DATE`, `TO_DATE`), causing a `NameError`; 15 other tests passed.
- Correction: provide all four non-secret constants in the test namespace. No network/API call was made by the test and no Dhan credential was involved.
- Status: expanded in commit a2a8f34; automated verification pending.

## QE-DELIVERY-39673276814 — automated run record
- Date: 2026-10-21T20:47:45.092701+00:00
- Run status: BLOCKED_AUTOMATED_TESTS
- Reason/error classification: integration test gate did not pass
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.

## QE-DELIVERY-39673437932 — automated run record
- Date: 2026-10-21T20:48:49.402937+00:00
- Run status: LLM_EVOLUTION_NOT_REQUESTED
- Reason/error classification: automatic workflow ran offline gate only; no model-generation API call was requested
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.

## QE-DELIVERY-39673574590 — automated run record
- Date: 2026-10-21T20:49:48.425703+00:00
- Run status: BLOCKED_OFFICIAL_EXPIRY_AND_HISTORICAL_LOT_SIZE_UNVERIFIED
- Reason/error classification: No runtime error reported in the sanitized manifest.
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.

## QE-DELIVERY-39673603711 — automated run record
- Date: 2026-10-21T20:50:43.641117+00:00
- Run status: LLM_EVOLUTION_NOT_REQUESTED
- Reason/error classification: automatic workflow ran offline gate only; no model-generation API call was requested
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.


## QE-ERR-025 — Dhan expired-options endpoint returned HTTP 400 with opaque first report
- Date: 2026-10-22. Severity: MEDIUM (source acquisition diagnostic).
- Workflow: [bounded Dhan probe run 39673574590](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39673574590).
- Observation: one request returned HTTP 400 and no `data` object. The first sanitizer retained top-level response keys but not the API's sanitized error type, so the cause could not be discriminated.
- Correction: classifier now records only bounded error-code/type and a coarse error-message class (not raw provider message, response body, token, or market rows); regression test added. One further single-call diagnostic may use this classification; no retry loop is permitted.
- Status: code and test committed; one bounded diagnostic pending.

## QE-DELIVERY-39673809637 — automated run record
- Date: 2026-10-21T20:51:31.557623+00:00
- Run status: LLM_EVOLUTION_NOT_REQUESTED
- Reason/error classification: automatic workflow ran offline gate only; no model-generation API call was requested
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.

## QE-DELIVERY-39673874887 — automated run record
- Date: 2026-10-21T20:53:28.339543+00:00
- Run status: LLM_EVOLUTION_NOT_REQUESTED
- Reason/error classification: automatic workflow ran offline gate only; no model-generation API call was requested
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.

## QE-DELIVERY-39674271641 — automated run record
- Date: 2026-10-21T20:54:50.087688+00:00
- Run status: BLOCKED_OFFICIAL_EXPIRY_AND_HISTORICAL_LOT_SIZE_UNVERIFIED
- Reason/error classification: No runtime error reported in the sanitized manifest.
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.

## QE-DELIVERY-39674310202 — automated run record
- Date: 2026-10-21T20:55:31.163470+00:00
- Run status: LLM_EVOLUTION_NOT_REQUESTED
- Reason/error classification: automatic workflow ran offline gate only; no model-generation API call was requested
- Options data gate: BLOCKED_NO_VERIFIED_CONTRACT_DATA; P&L permitted=False.
- No API key or credential value is persisted.
