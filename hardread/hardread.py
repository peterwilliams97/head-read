"""hardread.py is the command: it turns a Markdown or text file into prose blocks, parses them with
spaCy's en_core_web_trf, runs every detector in features.FEATURES over every sentence, and prints
the findings. It is a report, not a gate, so it exits 0 whatever it finds; only a missing input
file or missing setup exits non-zero.
"""

from __future__ import annotations

import argparse
import dataclasses
import functools
import json
import re
import sys
from collections import Counter
from pathlib import Path

from hardread import features
from hardread.features import PLACEHOLDER, Finding, Report

_FENCE = re.compile(r"^\s{0,3}(```|~~~)")
_ATX_HEADING = re.compile(r"^\s{0,3}#{1,6}(\s|$)")
_SETEXT_UNDERLINE = re.compile(r"^\s{0,3}(=+|-+)\s*$")
_THEMATIC_BREAK = re.compile(r"^\s{0,3}([-*_])(\s*\1){2,}\s*$")
_LIST_ITEM = re.compile(r"^\s*([-*+]|\d+[.)])\s+")
_BLOCKQUOTE = re.compile(r"^\s*(>\s?)+")
_TABLE_ROW = re.compile(r"^\s*\|")
_LINK_LIST_SEP = re.compile(r"\s*[·|—]\s*")
_SENTENCE_END = re.compile(r"[.!?](\s|$)")

_INLINE_CODE = re.compile(r"(`+)(.+?)\1")
_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")
_URL = re.compile(r"<https?://[^>]*>|https?://\S+[^\s.,;:)\]]")
_STRONG = re.compile(r"(\*\*|__)(.+?)\1")
_EMPHASIS = re.compile(r"(?<!\w)[*_](\S(?:.*?\S)?)[*_](?!\w)")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="hardread",
        description="Flag sentences built from constructions linked to reading difficulty.")
    ap.add_argument("path", help="Markdown (.md) or plain-text file")
    ap.add_argument("--json", action="store_true", help="print the Report as JSON")
    ap.add_argument("--summary", action="store_true",
                    help="after the findings, print a count per feature and findings per 100 sentences")
    ap.add_argument("--deplen", type=float, default=3.5,
                    help="DependencyLength threshold, mean arc length in words (default 3.5)")
    ap.add_argument("--maxwords", type=int, default=features.MAX_WORDS,
                    help=f"DependencyLength also flags sentences over this many words (default {features.MAX_WORDS})")
    args = ap.parse_args(argv)

    path = Path(args.path)
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as e:
        print(f"hardread: {e}", file=sys.stderr)
        return 2

    nlp = _load_model()
    if nlp is None:
        return 2
    try:
        report = analyze(nlp, args.path, source, args.deplen, args.maxwords)
    except LookupError as e:
        print(f"hardread: NLTK data missing; run `make setup`.\n{e}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(dataclasses.asdict(report), indent=2, ensure_ascii=False))
        return 0
    for f in report.findings:
        print(f"{report.path}:{f.line}  {f.feature}  {mark(f)}")
    if args.summary:
        print(summary(report))
    return 0


def analyze(nlp, path: str, source: str, deplen: float, maxwords: int) -> Report:
    """analyze parses each prose block as its own Doc, so spaCy never sees two blocks at once and a
    sentence cannot cross a paragraph or list-item break."""
    markdown = Path(path).suffix.lower() in (".md", ".markdown")
    blocks = markdown_blocks(source) if markdown else text_blocks(source)
    detectors = [functools.partial(features.DependencyLength, threshold=deplen, max_words=maxwords)
                 if f is features.DependencyLength else f for f in features.FEATURES]

    report = Report(path=path)
    texts = (text for _, _, text in blocks)
    for (first_line, line_starts, _), doc in zip(blocks, nlp.pipe(texts)):
        doc.user_data["first_line"] = first_line
        doc.user_data["line_starts"] = line_starts
        for sent in doc.sents:
            if not sent.text.strip():
                continue
            report.sentences += 1
            for detect in detectors:
                finding = detect(sent)
                if finding is not None:
                    report.findings.append(finding)
    report.findings.sort(key=lambda f: f.line)
    return report


def markdown_blocks(source: str) -> list[tuple[int, list[int], str]]:
    """markdown_blocks returns one (first line, line start offsets, text) per paragraph or list
    item. Fenced code, headings, tables, indented code and `_is_link_list` blocks are dropped;
    inline code and URLs become `PLACEHOLDER`; a link keeps its text. Code, link and URL
    substitution runs per source line, before the lines of a block are joined by one space, so
    inline code broken across two source lines is left as written. Emphasis markers are stripped
    from the joined block by `_strip_emphasis`, so a span may cross lines; `line_starts` indexes
    the text spaCy sees."""
    blocks: list[tuple[int, list[int], str]] = []
    cur: list[tuple[int, str]] = []
    cur_raw: list[str] = []  # `cur`'s lines before `_inline`, for `_is_link_list`
    cur_is_item = False
    in_fence = False

    def flush() -> None:
        nonlocal cur, cur_raw, cur_is_item
        if cur and not _is_link_list(" ".join(cur_raw), " ".join(t for _, t in cur)):
            blocks.append(_strip_emphasis(*_join(cur)))
        cur, cur_raw, cur_is_item = [], [], False

    for n, raw in enumerate(source.splitlines(), start=1):
        if _FENCE.match(raw):
            flush()
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not raw.strip() or _ATX_HEADING.match(raw) or _TABLE_ROW.match(raw):
            flush()
            continue
        if _SETEXT_UNDERLINE.match(raw) and cur and not cur_is_item:
            cur, cur_raw, cur_is_item = [], [], False  # the paragraph above was a setext heading
            continue
        if _THEMATIC_BREAK.match(raw) or _SETEXT_UNDERLINE.match(raw):
            flush()
            continue
        line = _BLOCKQUOTE.sub("", raw)
        item = _LIST_ITEM.match(line)
        if item:
            flush()
            cur, cur_is_item = [(n, _inline(line[item.end():].strip()))], True
            cur_raw = [line[item.end():].strip()]
            continue
        if not cur and raw.startswith(("    ", "\t")):
            continue  # indented code block
        cur.append((n, _inline(line.strip())))
        cur_raw.append(line.strip())
    flush()
    return blocks


def text_blocks(source: str) -> list[tuple[int, list[int], str]]:
    """text_blocks splits plain text on blank lines and touches nothing else."""
    blocks: list[tuple[int, list[int], str]] = []
    cur: list[tuple[int, str]] = []
    for n, raw in enumerate(source.splitlines(), start=1):
        if raw.strip():
            cur.append((n, raw.strip()))
        elif cur:
            blocks.append(_join(cur))
            cur = []
    if cur:
        blocks.append(_join(cur))
    return blocks


def mark(f: Finding) -> str:
    """mark wraps the first occurrence of the finding's span in «» inside its sentence."""
    i = f.sentence.find(f.span)
    if i < 0:
        return f"{f.sentence}  «{f.span}»"
    return f"{f.sentence[:i]}«{f.span}»{f.sentence[i + len(f.span):]}"


def summary(report: Report) -> str:
    counts = Counter(f.feature for f in report.findings)
    rows = [f"{report.path}: {report.sentences} sentences, {len(report.findings)} findings"]
    for f in features.FEATURES:
        n = counts[f.__name__]
        rate = 100 * n / report.sentences if report.sentences else 0.0
        rows.append(f"  {f.__name__:<18} {n:>4}  {rate:6.1f} per 100 sentences")
    total = 100 * len(report.findings) / report.sentences if report.sentences else 0.0
    rows.append(f"  {'all':<18} {len(report.findings):>4}  {total:6.1f} per 100 sentences")
    return "\n".join(rows)


def _join(lines: list[tuple[int, str]]) -> tuple[int, list[int], str]:
    starts, parts, pos = [], [], 0
    for _, text in lines:
        starts.append(pos)
        parts.append(text)
        pos += len(text) + 1
    return lines[0][0], starts, " ".join(parts)


def _inline(text: str) -> str:
    text = _INLINE_CODE.sub(PLACEHOLDER, text)
    text = _IMAGE.sub("", text)
    text = _LINK.sub(r"\1", text)
    return _URL.sub(PLACEHOLDER, text)


def _is_link_list(raw: str, text: str) -> bool:
    """_is_link_list reports a navigation line rather than prose: `text`, the block after `_inline`,
    has no sentence-ending punctuation, and `raw` splits on `_LINK_LIST_SEP` into two or more
    segments of which more than half hold a link."""
    if _SENTENCE_END.search(text):
        return False
    segments = _LINK_LIST_SEP.split(raw)
    linked = sum(1 for seg in segments if _LINK.search(seg))
    return len(segments) >= 2 and 2 * linked > len(segments)


def _strip_emphasis(first_line: int, starts: list[int], text: str) -> tuple[int, list[int], str]:
    """_strip_emphasis deletes the `_STRONG` then `_EMPHASIS` delimiters from a joined block and
    shifts each line start left by the delimiter characters deleted before it."""
    for pattern, group in ((_STRONG, 2), (_EMPHASIS, 1)):
        cut: list[tuple[int, int]] = []
        for m in pattern.finditer(text):
            cut += [(m.start(), m.start(group)), (m.end(group), m.end())]
        if not cut:
            continue
        text = "".join(text[b:e] for b, e in zip([0] + [e for _, e in cut],
                                                 [b for b, _ in cut] + [len(text)]))
        starts = [s - sum(min(e, s) - b for b, e in cut if b < s) for s in starts]
    return first_line, starts, text


def _load_model():
    try:
        import spacy
        return spacy.load("en_core_web_trf")
    except OSError as e:
        print(f"hardread: cannot load en_core_web_trf; run `make setup`.\n{e}", file=sys.stderr)
        return None


if __name__ == "__main__":
    sys.exit(main())
