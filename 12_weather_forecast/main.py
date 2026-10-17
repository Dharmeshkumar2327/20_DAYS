"""Project entry point. Run with: python main.py"""
import sys
from pathlib import Path

# Add src to the module search path so this project runs without installation.
sys.path.insert(0, str(Path(__file__).parent / "src"))
from app import main

if __name__ == "__main__":
    main()
