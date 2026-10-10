# 🎯 Python Number Guessing Challenge

A beginner-friendly, terminal-based Python mini-project. The computer chooses a secret number and the player tries to guess it using hints and a limited number of attempts.

## Features

- Three difficulty levels: Easy, Medium, and Hard
- Random secret number for every round
- “Too high” and “Too low” hints
- Input validation for non-numeric and out-of-range entries
- Score based on the number of attempts remaining
- Session summary showing rounds played, rounds won, and total score
- Option to play multiple rounds

## Python concepts practiced

- Variables and data types
- `input()` and `print()`
- Type conversion with `int()`
- Conditional statements: `if`, `elif`, and `else`
- Loops: `while` and `for`
- Functions and return values
- Lists/dictionaries and membership checks
- Boolean logic and comparison operators
- Exception handling with `try` / `except`
- The `random` module
- `if __name__ == "__main__":`

## Requirements

- Python 3.8 or newer
- No third-party packages are required

## Run the game

1. Download or clone this repository.
2. Open the project folder in a terminal or VS Code.
3. Run one of these commands:

   **Windows**
   ```bash
   python number_guessing_game.py
   ```

   **macOS / Linux**
   ```bash
   python3 number_guessing_game.py
   ```

4. Choose a difficulty and start guessing.

## Scoring

The score for a winning round is:

`(attempts remaining + 1) × 10`

For example, guessing correctly on the first attempt in Medium mode earns 70 points. An unsuccessful round earns 0 points.

## Example gameplay

```text
==========================================
       PYTHON NUMBER GUESSING CHALLENGE
==========================================

Choose your difficulty:
1. Easy   (1-50, 10 attempts)
2. Medium (1-100, 7 attempts)
3. Hard   (1-200, 6 attempts)
Enter 1, 2, or 3: 2

You chose Medium mode.
I'm thinking of a number between 1 and 100.
You have 7 attempts. Good luck!

Attempt 1/7 — your guess: 40
Too low! Try a higher number.
Attempts remaining: 6
```

*The secret number and hints vary each time the game runs.*

## Project structure

```text
python-number-guessing-game/
├── number_guessing_game.py
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
└── tests/
    └── test_game_logic.py
```

## Learning activities

Try these extensions after the basic game works:

1. Add a “hint” that tells the player whether the number is even or odd.
2. Track the best score across rounds.
3. Add a timer for each round.
4. Ask for the player's name and personalize the welcome message.
5. Create a graphical version using Tkinter.

## Testing

Run the basic automated tests with:

```bash
python -m unittest discover -s tests -v
```

The tests check the score calculation and difficulty settings without requiring external libraries.

## Upload to GitHub

1. Sign in to GitHub and create a repository named `python-number-guessing-game`.
2. Keep the repository Public if you want to showcase it in a student portfolio.
3. Upload the files and folders in this project, or use Git commands:

   ```bash
   git init
   git add .
   git commit -m "Add Python Number Guessing Challenge"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/python-number-guessing-game.git
   git push -u origin main
   ```

   Replace `YOUR-USERNAME` with your GitHub username.

## Author

Student Python Mini-Project
