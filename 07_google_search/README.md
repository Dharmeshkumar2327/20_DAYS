# Advanced Google Search Tool in Python

**Created by Dharmesh Kumar**

A beginner-friendly but extensible Python command-line tool that builds Google Search URLs, validates input, opens a search in your default browser, and supports small batches of searches. This project upgrades a basic `pywhatkit` search example using only Python's standard library.

## Features

- Single-query search from the terminal
- Interactive searches and comma-separated batches
- URL encoding for spaces, quotes, and special characters
- Input validation and a 300-character query limit
- Batch limit of 10 queries and configurable delay
- `--print-only` mode to generate URLs without opening a browser
- Unit tests using Python's `unittest`
- Jupyter notebook with examples and explanations
- No API key and no third-party packages required

## Project structure

```text
advanced-google-search/
├── advanced_google_search.py
├── Advanced_Google_Search.ipynb
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── SECURITY.md
├── CHANGELOG.md
├── examples/
│   └── example_queries.txt
└── tests/
    └── test_advanced_google_search.py
```

## Requirements

- Python 3.10 or newer recommended
- A web browser, if you want searches to open automatically

The command-line script uses only the Python standard library. You do not need to install `pywhatkit`.

## Run in VS Code

1. Download and extract the project ZIP.
2. Open the `advanced-google-search` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Run a search:

   ```bash
   python advanced_google_search.py Python programming tutorials
   ```

5. Print a URL without opening a browser:

   ```bash
   python advanced_google_search.py --print-only "site:docs.python.org pathlib"
   ```

6. For an interactive prompt, run:

   ```bash
   python advanced_google_search.py
   ```

On some systems, use `python3` instead of `python`.

## Example queries

```bash
python advanced_google_search.py "Python list comprehension"
python advanced_google_search.py --print-only "site:docs.python.org pathlib"
python advanced_google_search.py --print-only "filetype:pdf machine learning syllabus"
python advanced_google_search.py --print-only "\"data analyst\" SQL Power BI"
```

Google search operators are interpreted by Google and may change over time. The tool creates search URLs; it does **not** scrape Google results or return structured result data.

## Run the notebook

Open `Advanced_Google_Search.ipynb` in VS Code with the Jupyter extension or in Jupyter Notebook. Run the cells from top to bottom.

## Run tests

From the project root:

```bash
python -m unittest discover -s tests -v
```

No third-party test framework is required.

## Upload to GitHub

1. Sign in to GitHub and create a new **public** or **private** repository, for example `advanced-google-search-tool`.
2. Keep the repository name lowercase and use hyphens.
3. Extract this ZIP and upload the *contents* of the `advanced-google-search` folder to the repository root.
4. Commit the files with a message such as `Add advanced Google Search Python project`.

Alternatively, from the project folder, use Git:

```bash
git init
git add .
git commit -m "Add advanced Google Search Python project"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/advanced-google-search-tool.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username and create the repository on GitHub first.

## Privacy and responsible use

When opened, the search URL sends the query to Google. Do not search for passwords, API keys, private records, or other confidential information. This project opens normal Google Search pages and does not bypass access controls or scrape results.

## Author

**Dharmesh Kumar**

This repository is prepared for your GitHub portfolio. Update your GitHub profile link in the repository settings or README if you want to add it later.
