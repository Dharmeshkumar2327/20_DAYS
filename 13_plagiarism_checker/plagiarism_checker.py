"""
Plagiarism Checker
------------------
Compares .txt documents using TF-IDF vectors and cosine similarity.

Usage:
    python plagiarism_checker.py
    python plagiarism_checker.py --documents documents --threshold 0.30
"""

from argparse import ArgumentParser
from itertools import combinations
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_documents(folder: Path) -> dict[str, str]:
    """Read all .txt files from the specified folder."""
    if not folder.exists():
        raise FileNotFoundError(f"Documents folder not found: {folder}")

    documents = {}
    for file_path in sorted(folder.glob("*.txt")):
        try:
            documents[file_path.name] = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"Skipping {file_path.name}: file is not valid UTF-8 text.")

    return documents


def compare_documents(documents: dict[str, str]) -> list[tuple[str, str, float]]:
    """Return pairwise cosine similarity scores from 0 to 1."""
    if len(documents) < 2:
        return []

    names = list(documents)
    contents = [documents[name] for name in names]

    # TF-IDF converts text into numerical features.
    # Cosine similarity estimates how similar two feature vectors are.
    matrix = TfidfVectorizer().fit_transform(contents)
    similarity_matrix = cosine_similarity(matrix)

    results = []
    for i, j in combinations(range(len(names)), 2):
        results.append((names[i], names[j], float(similarity_matrix[i, j])))

    return sorted(results, key=lambda item: item[2], reverse=True)


def main() -> None:
    parser = ArgumentParser(description="Compare text files for potential plagiarism.")
    parser.add_argument(
        "--documents",
        default="documents",
        help="Folder containing .txt files (default: documents)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.30,
        help="Similarity threshold from 0 to 1 for flagging pairs (default: 0.30)",
    )
    args = parser.parse_args()

    if not 0 <= args.threshold <= 1:
        parser.error("--threshold must be between 0 and 1")

    folder = Path(args.documents)
    documents = load_documents(folder)

    if len(documents) < 2:
        print(f"Found {len(documents)} text file(s) in '{folder}'.")
        print("Add at least two .txt files to compare.")
        return

    try:
        results = compare_documents(documents)
    except ValueError as error:
        print(f"Could not compare the documents: {error}")
        print("Make sure the text files contain meaningful text.")
        return

    print(f"Compared {len(documents)} documents.")
    print("-" * 72)
    print(f"{'Document A':30} {'Document B':30} Similarity")
    print("-" * 72)

    for name_a, name_b, score in results:
        flag = "  <-- REVIEW" if score >= args.threshold else ""
        print(f"{name_a[:29]:30} {name_b[:29]:30} {score:.1%}{flag}")

    print("-" * 72)
    print("Note: Similarity scores are indicators for human review, not proof of plagiarism.")


if __name__ == "__main__":
    main()
