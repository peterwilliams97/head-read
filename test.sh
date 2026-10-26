#!/usr/bin/env bash
# test.sh is the gate: exit 0 means the change is ready to commit. It byte-compiles the package,
# runs every unittest module and checks the run covered every test method the sources define, then
# runs hard-read on its own README and fails if that parsed zero sentences. It then runs hard-read
# on every testdata/*.md and fails unless each detector in `features.FEATURES` fires on at least one
# of them. That keeps the demo corpus a real-text example for every feature: a new detector arrives
# with a testdata file that triggers it. Unfinished-work marker sites are listed at the end and
# never fail the run.
#
# The "package without tests" check from ~/CLAUDE.md is dropped: there is one package, and it has
# tests for both of its modules.
set -euo pipefail
cd "$(dirname "$0")"
# curated_transformers, which en_core_web_trf loads, calls the deprecated `torch.jit.script`, and
# torch warns on every model load. Silence that one warning; every other one still prints.
export PYTHONWARNINGS=ignore::FutureWarning:torch.jit._script

echo "== compile"
uv run --no-sync python -m compileall -q hardread

echo "== unittest"
want=$(grep -ch '^    def test_' hardread/test_*.py | paste -sd+ - | bc)
out=$(uv run --no-sync python -m unittest hardread.test_hardread hardread.test_features 2>&1) \
	|| { echo "$out"; exit 1; }
echo "$out" | grep -E '^(Ran|OK)'
ran=$(echo "$out" | sed -n 's/^Ran \([0-9]*\) tests.*/\1/p')
if [ "${ran:-0}" -eq 0 ] || [ "$ran" -ne "$want" ]; then
	echo "FAIL: ran ${ran:-0} tests, sources define $want"
	exit 1
fi

echo "== hard-read on README.md"
json=$(uv run --no-sync hard-read --json README.md)
sentences=$(echo "$json" | uv run --no-sync python -c 'import json,sys; print(json.load(sys.stdin)["sentences"])')
echo "README.md: $sentences sentences"
if [ "$sentences" -eq 0 ]; then
	echo "FAIL: zero sentences parsed from README.md"
	exit 1
fi

echo "== every feature fires on testdata/"
shopt -s nullglob
corpus=(testdata/*.md)
if [ "${#corpus[@]}" -eq 0 ]; then
	echo "FAIL: no .md files in testdata/"
	exit 1
fi
reports=$(mktemp -d "${TMPDIR:-/tmp}/hardread-XXXXXX")
trap 'rm -rf "$reports"' EXIT
for i in "${!corpus[@]}"; do
	uv run --no-sync hard-read --json "${corpus[$i]}" > "$reports/$i.json" 2>/dev/null
done
uv run --no-sync python - "$reports"/*.json <<'EOF'
import json, sys
from collections import Counter
from hardread import features

want = [f.__name__ for f in features.FEATURES]
hits, failed = Counter(), False
for p in sys.argv[1:]:
    r = json.load(open(p))
    if r["sentences"] == 0:
        print(f"FAIL: zero sentences parsed from {r['path']}")
        failed = True
    hits.update(f["feature"] for f in r["findings"])
for name in want:
    print(f"  {name:<18} {hits[name]:>5}")
    if hits[name] == 0:
        print(f"FAIL: {name} fires on no file in testdata/")
        failed = True
print(f"{len(sys.argv) - 1} files, {len(want)} features")
sys.exit(1 if failed else 0)
EOF

echo "== unfinished (non-fatal)"
grep -rn --include='*.py' --include='*.md' -F '!@#$' hardread README.md || echo "none"
echo "PASS"
