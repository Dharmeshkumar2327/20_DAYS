# 📚 AI-Powered PDF Chatbot

Ask questions about a PDF and find relevant answers with page references. This project combines PDF text extraction, TF-IDF retrieval, and optional LLM-powered answer generation in a Streamlit web app.

## Features

- Upload a PDF directly in the browser.
- Extract text and preserve page numbers.
- Split text into overlapping chunks for retrieval.
- Retrieve relevant passages using TF-IDF and cosine similarity.
- Optionally use an OpenAI model to generate an answer grounded in retrieved passages.
- Display source passages to help verify answers.
- Maintain chat history during the current app session.
- Graceful handling of scanned PDFs and common API issues.

## Tech stack

- Python
- Streamlit
- pypdf
- scikit-learn
- OpenAI Python SDK (optional)

## Project structure

```text
ai-powered-pdf-chatbot/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Run locally

### 1. Install Python

Use Python 3.10 or newer.

### 2. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/ai-powered-pdf-chatbot.git
cd ai-powered-pdf-chatbot
```

### 3. Create and activate a virtual environment

**Windows PowerShell**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Start the app

```bash
streamlit run app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`. Open it in your browser.

## Enable AI-generated answers (optional)

1. Get an API key from your OpenAI account.
2. Start the app and paste the key into the sidebar's **OpenAI API key** field.
3. Confirm that the selected model is available to your account.

Alternatively, copy `.env.example` to `.env` and replace the placeholder with your key. If you use a `.env` file, load it in your shell or add `from dotenv import load_dotenv; load_dotenv()` near the top of `app.py`. **Never commit a real API key to GitHub.** API usage may incur charges.

Without an API key, the app still works as a PDF passage finder and shows the most relevant passages.

## How it works

1. The PDF is uploaded to the Streamlit session.
2. `pypdf` extracts text from each page.
3. Text is divided into overlapping chunks, each tagged with its source page.
4. TF-IDF converts chunks and the user's question into vectors.
5. Cosine similarity ranks the most relevant chunks.
6. If an API key is supplied, an LLM writes an answer using the retrieved passages; otherwise the passages are displayed directly.
7. Source pages and retrieved text are shown so users can verify the response.

## Limitations

- Scanned/image-only PDFs require OCR before upload.
- TF-IDF retrieval is keyword-based and may miss semantically related passages.
- Answers depend on the quality of extracted text and retrieved passages.
- Do not upload confidential or sensitive documents unless you have permission and understand how your chosen services process data.
- The app does not permanently store uploaded PDFs or chat history in a database.

## Future improvements

- Add OCR support for scanned documents.
- Add semantic search using embedding models and a vector database.
- Support multiple PDFs in one knowledge base.
- Add downloadable summaries and automatically generated quizzes.
- Add unit tests, logging, and deployment configuration.

## GitHub topics

`python`, `streamlit`, `pdf-chatbot`, `rag`, `natural-language-processing`, `machine-learning`, `openai`, `document-qa`

## License

This project is provided under the MIT License. Add a `LICENSE` file before distributing it if you want to formally apply that license.
