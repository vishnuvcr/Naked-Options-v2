"""Render a factual, data-driven GitHub Pages research status page."""
import html,json
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; R=ROOT/"reports"; DOCS=ROOT/"docs"
REPO="https://github.com/vishnuvcr/Naked-Options-v2"
def read(p):
 f=R/p
 if not f.exists():return {}
 try:return json.loads(f.read_text())
 except Exception:return {}
def main():
 DOCS.mkdir(exist_ok=True)
 data=read("data_manifest.json"); quality=read("data_quality.json")
 run=read("experiment_run_global.json") or read("experiment_run.json")
 rows=[]
 m=R/"metrics.csv"
 if m.exists() and m.stat().st_size:
  try: rows=pd.read_csv(m).query("status == 'OOS_EVALUATED'")
  except Exception: rows=[]
 links=[("Research plan","RESEARCH_PLAN.md"),("Questions","RESEARCH_QUESTIONS.md"),("Literature","LITERATURE_REVIEW.md"),("Data catalog","DATA_CATALOG.md"),("Results","RESULTS.md"),("Tester report","TESTER_REPORT.md"),("Manuscript","MANUSCRIPT.md")]
 nav=" | ".join(f'<a href="{REPO}/blob/main/research/{p}">{html.escape(n)}</a>' for n,p in links)
 blocks=[]
 if quality.get("validation")=="PASS" and len(rows):
  show=rows.sort_values(["task","horizon","feature_set","model"])
  cols=[c for c in ("task","horizon","model","feature_set","n","mae","rmse","accuracy","brier","p_holm","selected_by_validation") if c in show.columns]
  table=show[cols].head(150).to_html(index=False,border=0,classes="results",float_format=lambda v:f"{v:.5g}")
  status="Metrics generated; interpret by target and horizon. The validation-selected model is identified separately from the locked-holdout result."
 else:
  table="<p>No verified out-of-sample metrics are available yet. Data and experiment workflows must pass before results appear.</p>"
  status="NO EMPIRICAL RESULT CLAIMED"
 body=f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NIFTY 50 Prediction Research</title>
<style>body{{font:16px/1.6 system-ui,sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#202124}}h1,h2{{line-height:1.25}}table{{border-collapse:collapse;font-size:.88rem;width:100%;overflow-wrap:anywhere}}th,td{{border-bottom:1px solid #ddd;padding:.45rem;text-align:left}}th{{background:#f4f4f4}}.note{{border-left:3px solid #777;padding:.5rem 1rem}}code{{white-space:pre-wrap}}a{{color:#1558a6}}</style></head><body>
<h1>Fresh NIFTY 50 Prediction Research</h1><p><b>Protocol:</b> NIFTY-PRED-1.0 · <b>Scope:</b> forecasting only; no trading strategy.</p>
<div class="note"><b>Current status:</b> {html.escape(status)}<br><b>Data gate:</b> {html.escape(str(quality.get('validation','NOT RUN')))} · <b>Selected source:</b> {html.escape(str(data.get('selected_target_source','unknown')))} · <b>Rows:</b> {html.escape(str(data.get('target_rows','unknown')))}<br><b>Experiment status:</b> {html.escape(str(run.get('status','NOT RUN')))}</div>
<p>{nav}</p><h2>Out-of-sample results</h2>{table}
<h2>Research integrity</h2><p>Predictions are evaluated chronologically. Price-level performance is not equated with return or direction skill. The latest chronological holdout is not used for tuning. Missing data or unavailable model families are recorded as blocked/not run, not fabricated. P-values are adjusted within task/horizon groups.</p>
<h2>Repository</h2><p><a href="{REPO}">Source repository</a> · <a href="{REPO}/tree/main/scripts">Code</a> · <a href="{REPO}/tree/main/research">Research records</a></p>
<p>Page generated from artifacts in the current research workflow. Page deployment status is defined by GitHub Actions, not assumed.</p></body></html>"""
 (DOCS/"index.html").write_text(body,encoding="utf-8")
 print(f"Wrote {DOCS/'index.html'}; data_gate={quality.get('validation','NOT RUN')}; oos_rows={len(rows) if hasattr(rows,'__len__') else 0}")
if __name__=="__main__":main()
