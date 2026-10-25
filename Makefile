.PHONY: setup check

# setup installs the locked environment, en_core_web_trf included, then the WordNet corpus that
# DenominalVerb and InanimateSubject read. WordNet goes in .venv so nothing lands in ~/nltk_data.
setup:
	uv sync
	uv run python -m nltk.downloader -d .venv/nltk_data wordnet

check:
	./test.sh
