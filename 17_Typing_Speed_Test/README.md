# ⌨️ Typing Speed Test (Python)

A colourful, terminal-based **typing speed test** written in pure Python. It shows a sentence, times how long you take to type it, and reports your **words per minute (WPM)** and **accuracy**. No external libraries are needed.

## ✨ Features

- **Three difficulty levels**: Easy, Medium and Hard sentences
- **Multi-round sessions** (1–5 rounds) with a session summary
- **Detailed results**: Gross WPM, Net WPM, accuracy, time taken and correct words
- **Colour-coded feedback**: correct words in green, mistakes in red, missed words shown as `___`
- **Leaderboard**: top 5 scores for each difficulty, saved to `scores.json`
- **Personal history**: your last 10 tests, average and best speed
- **Fun ratings** from 🐢 *Slow and steady* to 🚀 *Lightning Fingers*
- Works on **Windows, macOS and Linux**

## 🚀 Getting Started

### Requirements
- Python 3.8 or newer

### Run it

```bash
git clone https://github.com/<your-username>/typing-speed-test.git
cd typing-speed-test
python typing_speed_test.py
```

## 🎮 How to Play

1. Enter your name.
2. Choose **Start typing test** from the menu.
3. Pick a difficulty and the number of rounds.
4. After the 3-second countdown, type the sentence exactly (capitals and punctuation count) and press **Enter**.
5. See your results, then check the leaderboard!

```
========================================================
              ⌨️   TYPING SPEED TEST   ⌨️
========================================================

Round 1/3  [MEDIUM]
Type the sentence below exactly, then press Enter.

  Python is a popular programming language used around the world.

  ➜ Python is a popular programing language used around the world.

  ⏱  Time taken  : 14.2 s
  ⚡ Gross speed : 52.4 WPM
  🎯 Accuracy    : 98.4 %
  ✅ Correct words: 9/10
  🏁 Net speed   : 51.6 WPM
  🔥 Excellent!
```

## 📐 How Scores Are Calculated

| Metric | Formula |
|---|---|
| **Gross WPM** | (characters typed ÷ 5) ÷ minutes taken. A "word" is standardised as 5 characters. |
| **Accuracy** | matching characters ÷ length of the longer text × 100 (uses Python's `difflib`) |
| **Net WPM** | Gross WPM × Accuracy. **This is your real score.** |

**Speed guide:** < 20 beginner · 20–35 average · 35–50 good · 50–70 fast · 70+ pro

## 📁 Project Structure

```
typing-speed-test/
├── typing_speed_test.py   # Main program: menu, game rounds, scoring, leaderboard
├── sentences.py           # Sentence bank grouped by difficulty
├── tests/
│   └── test_typing_speed_test.py   # Unit tests for the scoring logic
├── README.md
├── LICENSE
└── .gitignore
```

## 🧪 Running Tests

```bash
python -m unittest discover tests
```

## 🛠️ Customise It

- **Add your own sentences:** edit the lists in `sentences.py`.
- **Change the rating levels:** edit `get_rating()` in `typing_speed_test.py`.
- **Reset the leaderboard:** delete `scores.json`.

## 💡 Python Concepts Used

Loops, conditionals, functions, dictionaries, list comprehensions, f-strings, the `time`, `random`, `json`, `difflib` and `datetime` modules, file handling, exception handling and ANSI terminal colours.

## 🔮 Future Ideas

- Live character-by-character feedback using `curses`
- Timed mode (type as much as you can in 60 seconds)
- A GUI version with Tkinter
- Load sentences from a text file

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
