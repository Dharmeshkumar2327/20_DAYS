# 🎯 Python Number Guessing Challenge

**Created and developed by Dharmesh Kumar**

## Project Overview

Python Number Guessing Challenge is a terminal-based mini-project created by me to practice and demonstrate core Python programming concepts. The computer selects a secret number, and the player tries to guess it using hints and a limited number of attempts.

## Features

- Three difficulty levels: Easy, Medium, and Hard
- Random secret number in every round
- Helpful “Too high” and “Too low” hints
- Input validation for invalid and out-of-range entries
- Score based on the number of attempts used
- Session summary with rounds played, rounds won, and total score
- Replay option

## Technologies Used

- Python 3
- Python standard library (`random`, input/output, exception handling)
- `unittest` for basic tests

## Python Concepts Covered

- Variables and data types
- User input and type conversion
- Conditional statements (`if`, `elif`, `else`)
- Loops (`for` and `while`)
- Functions and return values
- Dictionaries and membership operators
- Comparison operators and Boolean logic
- Exception handling (`try` and `except`)
- Random number generation
- Main guard (`if __name__ == "__main__":`)

## Requirements

- Python 3.8 or newer
- No third-party packages required

## How to Run

1. Download or clone this repository.
2. Open the project folder in VS Code or a terminal.
3. Run the command below.

**Windows**
```bash
python number_guessing_game.py
```

**macOS / Linux**
```bash
python3 number_guessing_game.py
```

4. Select a difficulty and start guessing.

## Difficulty Levels

| Level | Number range | Attempts |
|---|---:|---:|
| Easy | 1–50 | 10 |
| Medium | 1–100 | 7 |
| Hard | 1–200 | 6 |

## Scoring

A successful round awards:

`(maximum attempts - attempt number + 1) × 10`

For example, guessing the correct number on the first attempt in Medium mode earns 70 points. An unsuccessful round earns zero points.

## Example Gameplay

```text
============================================
       PYTHON NUMBER GUESSING CHALLENGE
          Created by Dharmesh Kumar
============================================

Choose your difficulty:
1. Easy   (1-50, 10 attempts)
2. Medium (1-100, 7 attempts)
3. Hard   (1-200, 6 attempts)
Enter 1, 2, or 3: 2

Difficulty: Medium
I'm thinking of a number between 1 and 100.
You have 7 attempts. Good luck!

Attempt 1/7 — enter your guess: 40
Too low! Try a higher number.
Attempts remaining: 6
```

*The secret number and resulting hints vary from round to round.*

## Project Structure

```text
python-number-guessing-challenge/
├── number_guessing_game.py
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
└── tests/
    └── test_game_logic.py
```

## Run Tests

Run the included tests using:

```bash
python -m unittest discover -s tests -v
```

## Future Enhancements

- Add a timer for each round
- Save a high score or leaderboard
- Ask for the player's name
- Add sound effects
- Build a graphical interface with Tkinter

## Author

**Dharmesh Kumar**

This mini-project was created and developed by me for learning, practice, and educational demonstration.

## GitHub Repository Setup

Suggested repository name: `python-number-guessing-challenge`

Suggested description:

> A Python number guessing game created by Dharmesh Kumar, featuring difficulty levels, hints, scoring, input validation, replay functionality, and tests.

To upload using Git, create a new repository on GitHub, then run the following commands from this project folder. Replace `YOUR-USERNAME` with your GitHub username.

```bash
git init
git add .
git commit -m "Add Python Number Guessing Challenge"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/python-number-guessing-challenge.git
git push -u origin main
```

## License

This project is shared under the MIT License. See [LICENSE](LICENSE) for details.
