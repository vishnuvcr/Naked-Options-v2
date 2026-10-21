undefined

## QE-ERR-008 — review-policy test checked the wrong file
- Date: 2026-10-22
- Severity: LOW
- Observed workflow: [bounded run 39665389015](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39665389015) and [audit run 39665388985](https://github.com/vishnuvcr/Naked-Options-v2/actions/runs/39665388985).
- Observation: 9 adapter/protocol tests passed and 1 protocol assertion failed because it looked for the no-independent-review instruction in the research plan, where it was not stated. The instruction exists in the core execution policy as required. Daily market data acquisition and target validation passed; the workflow correctly did not start Gemini evolution because the test gate failed.
- Correction: assert the no-review directive in research/EXECUTION_POLICY.md rather than searching the plan. Add the QE test file glob to both relevant workflow triggers so test-only fixes automatically rerun the bounded workflow and audit.
- Status: CORRECTED IN BRANCH; next run must verify.
