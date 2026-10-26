#!/usr/bin/env bash
# demo.sh runs `hard-read --summary` on every .md file in testdata/, one report per file. It is a
# showcase, not a gate: hard-read always exits 0, so a non-zero exit here means testdata/ held no
# .md files or a run crashed.
set -euo pipefail
cd "$(dirname "$0")"
# curated_transformers, which en_core_web_trf loads, calls the deprecated `torch.jit.script`, and
# torch warns on every model load. Silence that one warning; every other one still prints.
export PYTHONWARNINGS=ignore::FutureWarning:torch.jit._script

shopt -s nullglob
files=(testdata/*.md)
if [ "${#files[@]}" -eq 0 ]; then
	echo "demo.sh: no .md files in testdata/" >&2
	exit 1
fi

for f in "${files[@]}"; do
	echo "== $f"
	uv run --no-sync hard-read --summary "$f"
	echo
done
echo "${#files[@]} files"
