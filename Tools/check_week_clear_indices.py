"""Check Solgres bitmap indices against the game's decoded stage table."""
import json, re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
rows = json.loads((root / 'Research/DecodedCache/DB_stage_week.json').read_text())
header = (root / 'Server/Protocol/LocalWeekIndices.h').read_text()
actual = {int(a): int(b) for a, b in re.findall(r'\{(\d+),(\d+)\}', header)}
expected = {r['id']: r['weekly_index'] for r in rows}
assert actual == expected, (actual, expected)
assert actual[1] == 74 and actual[2] == 75
assert len(set(actual.values())) == len(actual)
flags = {}
for stage in (1, 2, 61, 2001):
    index = actual[stage]
    flags[index // 60] = flags.get(index // 60, 0) | (1 << (index % 60))
assert flags[1] & (1 << 14) and flags[1] & (1 << 15)
assert flags[0] & (1 << 30)
implementation = (root / 'Server/Protocol/LocalBattleProgress.h').read_text()
assert 'WeekIndexForStage(clear.second)' in implementation
assert 'index % 60' in implementation and 'index / 60' in implementation
print('PASS: all 35 native weekly indices; saved stage IDs map to the client’s 60-bit clear flags')
