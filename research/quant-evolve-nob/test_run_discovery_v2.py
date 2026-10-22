import importlib.util
import sys
from pathlib import Path
import numpy as np
BASE=Path(__file__).parent
sys.path.insert(0,str(BASE))
SPEC=importlib.util.spec_from_file_location('runner',BASE/'run_discovery_v2.py')
RUNNER=importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name]=RUNNER
SPEC.loader.exec_module(RUNNER)

def test_holm_adjustment_is_monotone_and_bounded():
    result=RUNNER.holm_adjust({'a':0.01,'b':0.04,'c':0.03})
    assert result=={'a':0.03,'c':0.06,'b':0.06}

def test_bootstrap_is_reproducible():
    x=np.asarray([2.0,-1.0,3.0,0.0,4.0,-2.0,1.0,3.0])
    assert RUNNER.moving_block_bootstrap(x,29,200,3)==RUNNER.moving_block_bootstrap(x,29,200,3)
