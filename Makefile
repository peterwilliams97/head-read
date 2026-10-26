.PHONY: setup check

# setup installs the locked environment, en_core_web_trf included, then the NLTK corpora: WordNet,
# which DenominalVerb and InanimateSubject read, and Brown, whose tags DenominalVerb counts. Both go
# in .venv so nothing lands in ~/nltk_data.
setup:
	uv sync
	uv run python -m nltk.downloader -d .venv/nltk_data wordnet brown

check:
	./test.sh
