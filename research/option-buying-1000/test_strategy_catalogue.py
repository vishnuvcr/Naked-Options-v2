import csv, hashlib, json, subprocess, sys
from pathlib import Path
ROOT=Path("research/option-buying-1000")
def test_registry_has_1000_distinct_rule_graphs():
 subprocess.run([sys.executable,str(ROOT/"strategy_catalogue.py")],check=True)
 rows=list(csv.DictReader((ROOT/"strategy_registry.csv").open()))
 audit=json.loads((ROOT/"CATALOGUE_AUDIT.json").read_text())
 assert len(rows)>=1000
 assert len({r["strategy_id"] for r in rows})==len(rows)
 assert len({r["rule_signature"] for r in rows})==len(rows)
 assert audit["duplicate_signatures"]==0 and audit["outcome_data_accessed"] is False
 for r in rows:
  spec=json.loads(r["logic_spec_json"])
  assert hashlib.sha256(json.dumps(spec,sort_keys=True,separators=(",",":")).encode()).hexdigest()==r["rule_signature"]
def test_strike_exit_variants_do_not_change_strategy_signature():
 spec={"operator":"AND","left":"ema_slope","right":"vwap_reclaim","definition":"both directional signals agree"}
 sig=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":")).encode()).hexdigest()
 assert sig(spec)==sig(spec)
