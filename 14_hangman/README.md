# Hangman Game in Python

A command-line Hangman game where players guess a hidden word one letter at a time before the hangman drawing is complete. Words are selected randomly from categories such as Programming, Animals, Fruits, and Indian Cities.

## Features

- Random word and category selection
- Interactive command-line gameplay
- Input validation (one English letter at a time)
- Prevents repeated guesses
- Six incorrect guesses allowed
- ASCII hangman drawing
- Score tracking across rounds
- Functions and docstrings for readable, maintainable code

## Requirements

- Python 3.9 or newer (the project uses only the Python standard library)
- A terminal or command prompt

## Quick Start

1. Install Python from [python.org](https://www.python.org/downloads/) if it is not installed.
2. Download or clone this repository.
3. Open a terminal in the project folder.
4. Run:

```bash
python hangman.py
```

On some systems, use `python3 hangman.py` instead.

## How to Play

1. Enter your name.
2. Read the displayed category and word length.
3. Guess one letter at a time.
4. Correct guesses reveal the letter in the word.
5. Each incorrect guess adds a part to the hangman drawing.
6. Guess the full word before six incorrect guesses to win.
7. Enter `y` to play another round.

## Project Structure

```text
hangman-python-game/
├── hangman.py
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
└── assets/
    └── gameplay-demo.txt
```

## Python Concepts Demonstrated

- Variables, strings, lists, dictionaries, and sets
- `if` / `elif` / `else` conditional logic
- `while` and `for` loops
- Functions and return values
- User input and validation
- Random selection with the `random` module
- String formatting with f-strings
- Basic program structure with `if __name__ == "__main__"`

## Customization Ideas

- Add new categories and words in `WORDS`
- Add difficulty levels
- Add hints or a hint limit
- Save scores to a file
- Add a graphical interface using Tkinter or Pygame
- Add unit tests

## Troubleshooting

**`python` is not recognized:** Try `py hangman.py` on Windows or `python3 hangman.py` on macOS/Linux. If needed, install Python and enable it in your PATH.

**The program closes immediately:** Run it from a terminal so you can interact with the input prompts.

**Want to contribute?** Fork the repository, create a branch, and open a pull request with your improvement.

## License

This project is released under the MIT License. See [LICENSE](LICENSE).
