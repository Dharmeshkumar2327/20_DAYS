# 🏏 Cricket Over Challenge

A beginner-friendly Python terminal game where teams take turns batting against a randomly generated over. Each team faces up to six balls, tries to reach a target of 20 runs, and competes for the highest score.

## Features

- Team-versus-team classroom competition
- Six-ball innings
- Random outcomes: dot ball, 1, 2, 3, four, six, or out
- Early end when a team is out or reaches the target
- Live score updates and a running leader
- Final winner announcement
- Separate, testable game-logic functions
- No third-party Python packages required

## Requirements

- Python 3.10 or newer recommended
- A terminal, Command Prompt, PowerShell, or VS Code
- No extra packages are needed

## Run the game

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

   ```bash
   python cricket_over_challenge.py
   ```

   On some Windows installations, use:

   ```powershell
   py cricket_over_challenge.py
   ```

4. Enter a team name.
5. Press Enter at each ball to reveal the outcome.
6. Enter `Y` when asked whether another team should bat, or `N` to finish.

## Rules

- Every team gets up to one over: six balls.
- Each ball has a random outcome.
- A team’s innings ends immediately if it gets out.
- A team’s innings also ends early if it reaches the target of 20 runs.
- The team with the highest score wins. Reaching the target is not required to win if no other team scores higher.

## Ball outcomes

| Random roll | Outcome | Runs |
|---:|---|---:|
| 1–2 | Dot ball | 0 |
| 3–4 | Single | 1 |
| 5–6 | Double | 2 |
| 7 | Three runs | 3 |
| 8 | Four | 4 |
| 9 | Six | 6 |
| 10 | Out | 0 and innings ends |

These are simplified classroom-game rules, not a complete simulation of official cricket.

## Python concepts practiced

- `import random` and random number generation
- Variables and counters
- `if`, `elif`-style decision logic
- `for` loops and `while` loops
- `break` to stop a loop early
- Functions, parameters, and return values
- User input and formatted output
- Dictionaries and tuples
- Basic unit testing

## Project structure

```text
cricket-over-challenge/
├── cricket_over_challenge.py
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── CONTRIBUTING.md
├── docs/
│   └── teacher_guide.md
└── tests/
    └── test_cricket_over_challenge.py
```

## Run the tests

From the project folder:

```bash
python -m unittest discover -s tests -v
```

The tests check the ball-outcome mapping and invalid random-roll handling.

## Possible future improvements

- Add a graphical interface using Tkinter or Pygame
- Add a batting scorecard and multiple wickets
- Add a tournament bracket
- Save match results to a CSV file
- Add difficulty settings and customizable targets

## Author

**Dharmesh Kumar**

Created as a Python learning project to make loops, conditionals, random numbers, and functions more engaging for students.

## License

This project is released under the MIT License. See [LICENSE](LICENSE).
