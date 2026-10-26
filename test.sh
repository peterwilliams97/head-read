#!/usr/bin/env bash
# test.sh is the gate: exit 0 means the change is ready to commit. It byte-compiles the package,
# runs every unittest module and checks the run covered every test method the sources define, then
# runs hard-read on its own README and fails if that parsed zero sentences. Unfinished-work marker
# sites are listed at the end and never fail the run.
#
# The "package without tests" check from ~/CLAUDE.md is dropped: there is one package, and it has
# tests for both of its modules.
set -euo pipefail
cd "$(dirname "$0")"

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

echo "== unfinished (non-fatal)"
grep -rn --include='*.py' --include='*.md' -F '!@#$' hardread README.md || echo "none"
echo "PASS"
