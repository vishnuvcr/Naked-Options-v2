import sys
from pathlib import Path
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from merge_results import read_csv_safe

def test_missing_or_empty_csv_is_treated_as_no_data(tmp_path):
    missing=tmp_path/"absent.csv"
    empty=tmp_path/"empty.csv";empty.write_text("",encoding="utf-8")
    newline=tmp_path/"empty-newline.csv";newline.write_text("\n",encoding="utf-8")
    assert read_csv_safe(missing).empty
    assert read_csv_safe(empty).empty
    assert read_csv_safe(newline).empty

def test_nonempty_csv_is_loaded(tmp_path):
    path=tmp_path/"valid.csv"
    pd.DataFrame({"task":["return"],"horizon":[1],"status":["OOS_EVALUATED"]}).to_csv(path,index=False)
    out=read_csv_safe(path)
    assert len(out)==1
    assert out.loc[0,"task"]=="return"
