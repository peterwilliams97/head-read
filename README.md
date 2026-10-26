# hardread

Some sentences are harder to read than others, even when every word is easy. Clark, Martin &
Mahowald (2026, arXiv:2610.29162, §3.1) measured five sentence shapes that slow human readers down,
and found AI-written text uses them more than people do. hardread reads a Markdown or text file and
points at each sentence that uses one of those shapes.

It is a report, not a test. It always exits 0.

## Where things are

| File                        | What it does  |
|-----------------------------|---------------|
| `hardread/features.py`      | One function per shape. Each looks at one sentence and returns a `Finding` or nothing. |
| `hardread/hardread.py`      | The command. Strips the Markdown, splits sentences with spaCy, runs every function, prints. |
| `hardread/test_features.py` | For each shape, one sentence that must be flagged and one that must not. |
| `hardread/test_hardread.py` | Checks the Markdown stripping and the line numbers. |
| `test.sh`                   | Runs everything. Exit 0 means all passed. |

## The five shapes

Each example sentence comes from the paper's Table 2.

- **ORCNoRelativizer.** A noun is followed by a clause about it, with its own subject and no
  "that", "which" or "who" to mark where the clause starts. *"I am writing to share my thoughts on
  the cell phone policy you are considering."*
- **DenominalVerb.** hardread flags a noun used as a verb only when that verb use is rare in
  English, as in *"calendar it"*. Rare means the Brown corpus has the word at least 5 times as a
  noun and never as a verb, or it is in the hand list `DENOMINAL_SEEDS`. The paper's Table 2
  examples ("mirrors", "cushions") are ordinary verbs and are not flagged.
- **InanimateSubject.** A thing that cannot think or eat is the subject of a verb that needs
  something that can, such as "ask", "want" or "promise". *"A song doesn't ask you to turn
  melancholy into a calendar item."* The verbs are listed in `ANIMATE_VERBS`. Inline code counts as
  a thing.
- **StackedNouns.** Three or more nouns in a row, each describing the next. *"Summer park district
  classes are a whole thing in Chicago and people actually do them."*
- **DependencyLength.** On average, words sit far from the word they attach to. hardread measures
  that distance in words, skipping punctuation, and flags the sentence when the average is over 3.0.
  *"Has the building had water, mold, structural, or insurance claims?"*

The paper also uses two word-pair measures, unattested word pairs and trigram surprisal. hardread
leaves them out. Both need a large reference corpus to count word pairs against, and this repo does
not carry one.

## Running it

    make setup                                # installs the venv, en_core_web_trf, WordNet and Brown
    uv run hardread README.md                 # one line per finding
    uv run hardread --summary README.md       # adds a count per shape and a rate per 100 sentences
    uv run hardread --json README.md          # the whole report as JSON
    uv run hardread --deplen 4 README.md      # a different DependencyLength cut-off
    ./test.sh                                 # all the tests

Each output line reads `path:line  SHAPE  sentence`, with the flagged words inside `«»`.

Before it reads the sentences, hardread drops code blocks, headings and tables. It puts the word
`CODE` in place of each inline code span and each URL, and keeps a link's text. A sentence never
runs across a paragraph break or from one list item into the next.
