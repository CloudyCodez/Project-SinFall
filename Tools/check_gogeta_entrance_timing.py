"""Check stretched entrance poses against the downloaded Legends clip."""
from copy import deepcopy
from pathlib import Path
import numpy as np
import UnityPy
from retime_generic_clip import stretch_clip
from tg_run_retarget import curve_samples

root = Path(__file__).resolve().parents[1]
source = UnityPy.load(str(root/'Research/DBLegends/PhoneFiles/streamingassetbundles/0078d08dd86329535d70b2ee86e03e38d82b4df5'))
original = next(o.read_typetree() for o in source.objects
                if o.type.name == 'AnimationClip' and o.read().m_Name == 'GTB_05_BAS_CHANGE_IN')
slower = stretch_clip(deepcopy(original), 6.0)
times = np.linspace(0, original['m_MuscleClip']['m_StopTime'], 101)
before, after = curve_samples(original, times), curve_samples(slower, times*6)
assert before.keys() == after.keys()
for binding in before:
    np.testing.assert_allclose(before[binding], after[binding], atol=2e-5, rtol=2e-5)
assert abs(slower['m_MuscleClip']['m_StopTime']/3 - 5/6) < 1e-5
print('PASS: all entrance curves preserve source poses at 101 samples; x3 duration 0.833s')
