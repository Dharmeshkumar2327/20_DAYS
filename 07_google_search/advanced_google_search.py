"""Advanced Google Search Tool | Created by Dharmesh Kumar.

Build Google Search URLs and optionally open them in the default browser.
Uses only Python's standard library; does not scrape search results.
"""
from __future__ import annotations

import argparse
import sys
import time
import webbrowser
from urllib.parse import quote_plus

AUTHOR = "Dharmesh Kumar"
MAX_QUERY_LENGTH = 300
MAX_BATCH_QUERIES = 10


def build_google_url(query: str) -> str:
    """Return a Google Search URL for a validated query."""
    if not isinstance(query, str):
        raise TypeError("Search query must be a string.")
    query = query.strip()
    if not query:
        raise ValueError("Search query cannot be empty.")
    if len(query) > MAX_QUERY_LENGTH:
        raise ValueError(f"Search query must be {MAX_QUERY_LENGTH} characters or fewer.")
    return f"https://www.google.com/search?q={quote_plus(query)}"


def search_google(query: str, open_tab: bool = True) -> str:
    """Print a search URL and optionally open it in a browser."""
    url = build_google_url(query)
    print(f"Query: {query.strip()}\nURL: {url}")
    if open_tab and not webbrowser.open(url, new=2):
        print("Browser did not report success. Copy the URL above into your browser.")
    return url


def search_many(queries: list[str], open_tabs: bool = True, delay_seconds: float = 1.0) -> list[str]:
    """Search up to ten non-empty queries in sequence."""
    if not isinstance(queries, (list, tuple)):
        raise TypeError("queries must be a list or tuple of strings.")
    cleaned = []
    for query in queries:
        if not isinstance(query, str):
            raise TypeError("Every search query must be a string.")
        if query.strip():
            cleaned.append(query.strip())
    if not cleaned:
        raise ValueError("Provide at least one non-empty search query.")
    if len(cleaned) > MAX_BATCH_QUERIES:
        raise ValueError(f"A maximum of {MAX_BATCH_QUERIES} searches is allowed per batch.")
    if not isinstance(delay_seconds, (int, float)) or not 0 <= delay_seconds <= 10:
        raise ValueError("delay_seconds must be between 0 and 10.")
    urls = []
    for index, query in enumerate(cleaned):
        urls.append(search_google(query, open_tab=open_tabs))
        if open_tabs and delay_seconds and index < len(cleaned) - 1:
            time.sleep(delay_seconds)
    return urls


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Advanced Google Search Tool by Dharmesh Kumar")
    parser.add_argument("query", nargs="*", help="Search query; quote phrases with spaces")
    parser.add_argument("--print-only", action="store_true", help="Print URLs without opening a browser")
    parser.add_argument("--delay", type=float, default=1.0, help="Seconds between batch searches (0-10; default: 1)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    print(f"Advanced Google Search | Created by {AUTHOR}")
    if args.query:
        query = " ".join(args.query)
        try:
            search_google(query, open_tab=not args.print_only)
        except (TypeError, ValueError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            return 2
        return 0

    print("Enter a search query. Use --help for command-line options.")
    try:
        raw = input("Search: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nCancelled.")
        return 1
    if not raw:
        print("No query entered.")
        return 1
    try:
        # Interactive comma-separated batch; quote a query containing commas by using CLI mode.
        queries = [part.strip() for part in raw.split(",") if part.strip()]
        if len(queries) == 1:
            search_google(queries[0], open_tab=not args.print_only)
        else:
            search_many(queries, open_tabs=not args.print_only, delay_seconds=args.delay)
    except (TypeError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
