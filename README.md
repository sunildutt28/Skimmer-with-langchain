# Skimmer-with-langchain

Light, fast, skims news for you — a minimal news skimming/summarization tool built with LangChain.

Skimmer-with-langchain fetches news (web pages, RSS, or other sources), extracts the main content, and uses LangChain to produce concise summaries and highlights so you can quickly stay informed.

## Features

- Lightweight and fast pipeline for skimming articles and feeds
- Summarization using LangChain + your preferred LLM
- Configurable summary length and style
- Optional vector store for semantic search / retrieval (optional)
- Simple CLI and programmatic usage (examples below)

## Quick Start

Prerequisites
- Python 3.8+ (confirm exact supported version)
- An OpenAI-compatible API key (or other LLM provider supported by your LangChain setup)
- git

Install
1. Clone the repo:
   git clone https://github.com/sunildutt28/Skimmer-with-langchain.git
   cd Skimmer-with-langchain

2. Create a virtual environment and install dependencies:
   python -m venv .venv
   source .venv/bin/activate  # macOS / Linux
   .venv\Scripts\activate     # Windows

   pip install -r requirements.txt
   # or, if you use poetry:
   # poetry install

Configuration
- Copy the example env/config file and set required keys:
  cp .env.example .env
  # Edit .env and add your API key(s)
  OPENAI_API_KEY=your_key_here

- If you use a config file (config.yaml or config.json), update summary length, sources, and storage options there. (TODO: replace with actual config file name and options)

Run (example)
- Skim a single URL:
  python main.py --url "https://example.com/article"

- Skim an RSS feed:
  python main.py --rss "https://example.com/feed.xml"

- Run in watch mode to poll feeds periodically:
  python main.py --rss "https://example.com/feed.xml" --poll-interval 3600

(Replace `main.py` with your actual entrypoint script if different.)

Example Output
- The tool prints a short summary and key points, for example:
  Title: Example Article
  Summary (3 sentences): ...
  Key points:
  - ...
  - ...

## Usage (Programmatic)

Python example:
```python
from skimmer import Skimmer 

sk = Skimmer(api_key="YOUR_API_KEY")
summary = sk.skim_url("https://example.com/article", max_sentences=3)
print(summary)
```

CLI example:
```bash
# Skim an article to stdout
python main.py --url "https://example.com/article" --max-sentences 3
```

## How it works (high-level)

1. Fetch: retrieve content from a URL, RSS feed, or local file.
2. Parse: extract the main article text (remove navigation, ads).
3. Chunk: split long content into chunks suitable for the LLM.
4. Summarize: use LangChain to build prompts and produce concise summaries.
5. (Optional) Store: optionally store embeddings in a vector store for retrieval and search.

## Configuration & Environment Variables

Common environment variables (adjust to match your implementation):
- OPENAI_API_KEY — API key for OpenAI (or set provider-specific variables)
- VECTOR_STORE_URL — URL or path for a vector DB (if used)
- LOG_LEVEL — logging level (INFO, DEBUG)

## Development

- Run tests:
  pytest  # or the appropriate test command

- Linting:
  flake8  # or black/isort

- Run the app locally:
  python main.py --help

## Deployment

- For a simple deployment, run on a server and schedule recurring runs (cron or systemd timers) to poll feeds.
- For web/GUI usage, integrate the summarizer into a web service or use Streamlit/Flask.

## Contributing

Contributions are welcome! Please open an issue or submit a PR with:
- a clear description of the change
- tests where applicable
- adherence to code style guidelines

## Roadmap / TODOs
- Add examples and a quick demo notebook

## License
-

## Acknowledgements

Built with:
- LangChain
- (Add any other libraries: newspaper3k, BeautifulSoup, feedparser, OpenAI, faiss, etc.)

Contact
- Repo: https://github.com/sunildutt28/Skimmer-with-langchain
- Author: sunildutt28
