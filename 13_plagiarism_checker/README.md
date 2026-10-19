# Python Plagiarism Checker

A beginner-friendly Python project that compares text documents using **TF-IDF** and **cosine similarity**. It reports similarity scores for every pair of `.txt` files so that a reviewer can identify documents that may need closer examination.

> **Important:** Similarity is only a signal for human review. This tool does not prove plagiarism and may miss paraphrased or cross-language copying.

## Features

- Compares multiple `.txt` files.
- Uses scikit-learn's TF-IDF vectorization.
- Calculates pairwise cosine similarity.
- Sorts document pairs from most to least similar.
- Flags scores at or above a configurable threshold.
- Includes a Jupyter Notebook and a command-line Python script.
- Handles missing folders and insufficient input files with helpful messages.

## Project structure

```text
plagiarism-checker/
├── 019_Plagiarism_Checker.ipynb
├── plagiarism_checker.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
└── documents/
    ├── sample_document_1.txt
    ├── sample_document_2.txt
    └── sample_document_3.txt
```

## Requirements

- Python 3.9 or newer recommended
- pip
- Packages listed in `requirements.txt`

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/plagiarism-checker.git
cd plagiarism-checker
```

Replace `YOUR-USERNAME` with your GitHub username and use your actual repository URL.

### 2. Create and activate a virtual environment (recommended)

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Run the Python script

Place the `.txt` files you want to compare in the `documents/` folder, then run:

```bash
python plagiarism_checker.py
```

Change the similarity threshold (for example, 40%) with:

```bash
python plagiarism_checker.py --threshold 0.40
```

Use a different folder:

```bash
python plagiarism_checker.py --documents path/to/text_files --threshold 0.35
```

The threshold must be between `0` and `1`.

## Run the Jupyter Notebook

1. Install Jupyter if needed: `python -m pip install notebook`
2. Start Jupyter: `jupyter notebook`
3. Open `019_Plagiarism_Checker.ipynb`.
4. Run the cells in order.

The notebook reads `.txt` files from the `documents/` folder.

## How it works

1. **Load documents:** Reads text files from the selected folder.
2. **TF-IDF:** Converts text into numerical features based on term importance.
3. **Cosine similarity:** Compares the document vectors. Scores closer to `1` indicate greater similarity; scores closer to `0` indicate less similarity.
4. **Review results:** Displays each document pair and its score.

## Example interpretation

- `0.85` (85%): high text similarity; review the pair.
- `0.40` (40%): some shared text or vocabulary; review in context.
- `0.05` (5%): low similarity under this method.

These are illustrative examples, not universal thresholds. Common phrases, short documents, quotations, and subject-specific vocabulary can affect results.

## Limitations

- Supports plain-text `.txt` files only.
- Does not directly inspect PDF, DOCX, or web pages.
- TF-IDF/cosine similarity can miss paraphrasing and may flag legitimate shared wording.
- Treat the output as a screening aid, not an academic misconduct decision.

## License

Released under the MIT License. See `LICENSE`.
