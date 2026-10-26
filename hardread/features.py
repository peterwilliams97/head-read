"""features.py holds one detector per construction from Clark, Martin & Mahowald 2026
(arXiv:2610.29162, §3.1). Each detector takes one spaCy sentence and returns a Finding or None —
at most one Finding per feature per sentence, so a count is a count of sentences.

The n-gram measures in §3.1 are absent on purpose: they need a reference corpus this repo does not
carry.
"""

from __future__ import annotations

import bisect
import functools
from collections import Counter
from dataclasses import dataclass, field

from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from spacy.tokens import Span, Token


@dataclass
class Finding:
    feature: str
    sentence: str
    span: str
    line: int
    note: str


@dataclass
class Report:
    path: str
    findings: list[Finding] = field(default_factory=list)
    sentences: int = 0


# DENOMINAL_SEEDS are verbs the paper's examples use as denominals that always flag, whatever
# their Brown counts — several are too rare in Brown for `BROWN_MIN_COUNT`, or newer than it.
DENOMINAL_SEEDS = frozenset({
    "calendar", "footnote", "dogfood", "surface", "gate", "action", "sunset", "whiteboard",
    "bucket", "wordsmith",
})

# BROWN_MIN_COUNT and BROWN_MAX_VERB_COUNT are `DenominalVerb`'s frequency rule: a lemma Brown tags
# as a noun at least BROWN_MIN_COUNT times and as a verb at most BROWN_MAX_VERB_COUNT times — 0,
# so any verb use in Brown rules the lemma out.
BROWN_MIN_COUNT = 5
BROWN_MAX_VERB_COUNT = 0

# ANIMATE_VERBS take a thinking, wanting or eating subject; an inanimate subject on one of them is
# the construction `InanimateSubject` flags.
ANIMATE_VERBS = frozenset({
    "eat", "bite", "swallow", "want", "hope", "promise", "forget", "remember", "ask", "decide",
    "know", "believe", "insist", "refuse", "expect", "complain", "pretend", "lie", "cheat",
    "assume", "think", "feel", "notice", "learn", "understand", "worry", "care", "love", "hate",
    "suffer", "enjoy",
})

# MAX_WORDS is the length past which `DependencyLength` flags a sentence whatever its mean arc.
MAX_WORDS = 30

# PLACEHOLDER is what hardread.py substitutes for inline code and URLs.
PLACEHOLDER = "CODE"

_INANIMATE_PRONOUNS = frozenset({"it", "this", "that", "which"})
_RELATIVIZER_TAGS = frozenset({"WDT", "WP", "WP$"})
_ANIMATE_ROOTS = frozenset({"person.n.01", "organism.n.01", "social_group.n.01"})
_ANIMATE_ENTS = frozenset({"PERSON", "ORG", "NORP"})
# Brown's common-noun and verb tags; NP is a proper noun. A suffix after "-" ("NN-TL", "VB-HL")
# marks a title or headline and is dropped before lookup.
_BROWN_NOUN_TAGS = frozenset({"NN", "NNS", "NN$", "NNS$"})
_BROWN_VERB_TAGS = frozenset({"VB", "VBD", "VBG", "VBN", "VBZ"})


def ORCNoRelativizer(sent: Span) -> Finding | None:
    """ORCNoRelativizer flags a noun modified by a relative clause that has its own subject and no
    "that"/"which"/"who" — "the policy you are considering". The reader has to supply the missing
    object position without a word marking where the clause begins."""
    for tok in sent:
        if tok.pos_ not in ("NOUN", "PROPN", "PRON"):
            continue
        for verb in tok.children:
            if verb.dep_ != "relcl" or verb.i < tok.i:
                continue
            subj = [c for c in verb.children if c.dep_ == "nsubj" and c.i > tok.i]
            if not subj or _has_relativizer(verb):
                continue
            span = sent.doc[tok.i : verb.right_edge.i + 1]
            return _finding("ORCNoRelativizer", sent, span.text,
                            f"subject {subj[0].text!r} inside a clause with no relativizer")
    return None


def DenominalVerb(sent: Span) -> Finding | None:
    """DenominalVerb flags a verb made from a noun whose verb use is rare — "calendar the review".
    Rare means Brown tags the lemma a noun at least `BROWN_MIN_COUNT` times and a verb at most
    `BROWN_MAX_VERB_COUNT` times, so an ordinary verb that is also a noun ("mirrors", "run") is not
    a hit; `DENOMINAL_SEEDS` flag regardless."""
    for tok in sent:
        if tok.pos_ != "VERB" or tok.text == PLACEHOLDER:
            continue
        lemma = tok.lemma_.lower()
        if lemma in DENOMINAL_SEEDS:
            return _finding("DenominalVerb", sent, tok.text, f"{lemma!r} is in DENOMINAL_SEEDS")
        nouns, verbs = _brown_counts()
        n, v = nouns[lemma], verbs[lemma]
        if n >= BROWN_MIN_COUNT and v <= BROWN_MAX_VERB_COUNT:
            return _finding("DenominalVerb", sent, tok.text,
                            f"{lemma!r} is a noun {n} times and a verb {v} times in Brown")
    return None


def InanimateSubject(sent: Span) -> Finding | None:
    """InanimateSubject flags an inanimate subject on a verb from `ANIMATE_VERBS` — "the docstring
    promises". A relative "that"/"which" is judged by the noun it attaches to, so "the person who
    knows" is not a hit; when that noun is `PLACEHOLDER` the clause is skipped, since the code it
    stands for is not seen. `PLACEHOLDER` as the `nsubj` itself is still inanimate."""
    for tok in sent:
        if tok.dep_ != "nsubj" or tok.head.pos_ != "VERB":
            continue
        verb = tok.head
        if verb.lemma_.lower() not in ANIMATE_VERBS:
            continue
        subj = tok
        if tok.lower_ in ("that", "which", "who") and verb.dep_ == "relcl":
            subj = verb.head
            if subj.text == PLACEHOLDER:
                continue
        if _is_inanimate(subj):
            span = sent.doc[min(tok.i, verb.i) : max(tok.i, verb.i) + 1]
            return _finding("InanimateSubject", sent, span.text,
                            f"{subj.text!r} is inanimate, {verb.lemma_!r} wants an animate subject")
    return None


def StackedNouns(sent: Span) -> Finding | None:
    """StackedNouns flags three or more nouns in one `compound` chain — "summer park district
    classes". Each modifier narrows the next and the reader holds them all until the head noun.
    Chain members joined by an unspaced hyphen count as one noun, so "word-pair measures" is two.
    `PLACEHOLDER` is not a noun here: "the hand list CODE" is two."""
    for tok in sent:
        if tok.pos_ not in ("NOUN", "PROPN") or tok.dep_ == "compound":
            continue
        chain = [t for t in _compound_chain(tok) if t.text != PLACEHOLDER]
        if not chain:
            continue
        nouns = len(chain) - _hyphen_joins(chain)
        if nouns >= 3:
            lo, hi = min(t.i for t in chain), max(t.i for t in chain)
            span = sent.doc[lo : hi + 1]
            return _finding("StackedNouns", sent, span.text, f"{nouns} nouns in a compound")
    return None


def DependencyLength(
    sent: Span,
    threshold: float = 3.5,
    max_words: int = MAX_WORDS,
) -> Finding | None:
    """DependencyLength flags a sentence whose mean distance from word to head, in words, exceeds
    `threshold`, or that has more than `max_words` words. Punctuation arcs and the root are excluded
    from the mean, as the paper does; punctuation and `PLACEHOLDER` are not counted as words."""
    arcs = [abs(t.i - t.head.i) for t in sent
            if t.dep_ != "ROOT" and not t.is_punct and not t.is_space]
    words = sum(1 for t in sent if not t.is_punct and not t.is_space and t.text != PLACEHOLDER)
    mean = sum(arcs) / len(arcs) if arcs else 0.0
    if mean > threshold:
        return _finding("DependencyLength", sent, sent.text,
                        f"mean arc {mean:.2f} > {threshold}; sentence {words} words")
    if words > max_words:
        return _finding("DependencyLength", sent, sent.text,
                        f"sentence {words} words > {max_words}; mean arc {mean:.2f}")
    return None


FEATURES = (ORCNoRelativizer, DenominalVerb, InanimateSubject, StackedNouns, DependencyLength)


def _finding(feature: str, sent: Span, span: str, note: str) -> Finding:
    return Finding(feature, sent.text, span, sentence_line(sent), note)


def sentence_line(sent: Span) -> int:
    """sentence_line maps a sentence to its source line through the `line_starts` and
    `first_line` that hardread.py stores on each block's Doc. A Doc built without them is line 1
    onward, counted from the Doc's own newlines."""
    user = sent.doc.user_data
    starts = user.get("line_starts")
    if starts is None:
        return 1 + sent.doc.text.count("\n", 0, sent.start_char)
    return user["first_line"] + bisect.bisect_right(starts, sent.start_char) - 1


def _has_relativizer(verb: Token) -> bool:
    for t in verb.subtree:
        if t.tag_ in _RELATIVIZER_TAGS:
            return True
        if t.lower_ == "that" and t.dep_ in ("mark", "dobj", "nsubj"):
            return True
    return False


def _is_inanimate(tok: Token) -> bool:
    if tok.text == PLACEHOLDER or tok.lower_ in _INANIMATE_PRONOUNS:
        return True
    if tok.pos_ not in ("NOUN", "PROPN"):
        return False
    # Entity types are trusted on proper nouns only: the NER tags "docstring" ORG, and a common
    # noun's animacy is WordNet's to decide.
    if tok.pos_ == "PROPN" and tok.ent_type_ in _ANIMATE_ENTS:
        return False
    senses = wn.synsets(tok.lemma_.lower(), pos=wn.NOUN)
    if not senses:
        # A common noun WordNet lacks is usually a technical term ("docstring"); a proper noun it
        # lacks may be anyone's name.
        return tok.pos_ == "NOUN"
    # The first sense is WordNet's most frequent; "chaos" has a mythological person sense further
    # down that would otherwise make it animate.
    for path in senses[0].hypernym_paths():
        if any(s.name() in _ANIMATE_ROOTS for s in path):
            return False
    return True


def _compound_chain(head: Token) -> list[Token]:
    chain = [head]
    for child in head.children:
        if child.dep_ == "compound" and child.pos_ in ("NOUN", "PROPN"):
            chain.extend(_compound_chain(child))
    return chain


def _hyphen_joins(chain: list[Token]) -> int:
    """_hyphen_joins counts chain members followed by "-" and then another member, with no
    whitespace on either side of the hyphen: spaCy splits "word-pair" into three tokens."""
    members = {t.i for t in chain}
    doc = chain[0].doc
    joins = 0
    for t in chain:
        if t.i + 2 not in members or t.whitespace_:
            continue
        hyphen = doc[t.i + 1]
        if hyphen.text == "-" and not hyphen.whitespace_:
            joins += 1
    return joins


@functools.cache
def _brown_counts() -> tuple[Counter[str], Counter[str]]:
    """_brown_counts returns (noun, verb) token counts per lemma over the tagged Brown corpus,
    lemmatised with WordNet's morphy. Built once per process; it takes a few seconds."""
    nouns: Counter[str] = Counter()
    verbs: Counter[str] = Counter()
    lemmas: dict[tuple[str, str], str] = {}
    for word, tag in brown.tagged_words():
        base = tag.split("-")[0]
        if base in _BROWN_NOUN_TAGS:
            pos, counts = wn.NOUN, nouns
        elif base in _BROWN_VERB_TAGS:
            pos, counts = wn.VERB, verbs
        else:
            continue
        key = (word.lower(), pos)
        lemma = lemmas.get(key)
        if lemma is None:
            lemma = lemmas[key] = wn.morphy(key[0], pos) or key[0]
        counts[lemma] += 1
    return nouns, verbs
