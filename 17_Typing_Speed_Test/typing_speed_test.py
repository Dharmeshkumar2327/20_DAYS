"""
Typing Speed Test
=================
A terminal-based typing speed test written in pure Python
(no external libraries required).

Features
--------
- Three difficulty levels (Easy, Medium, Hard)
- Single round or multi-round sessions
- Measures Gross WPM, Net WPM, accuracy and time taken
- Colour-coded feedback showing correct and incorrect words
- Persistent leaderboard and personal history (saved to scores.json)

Run:
    python typing_speed_test.py
"""

import difflib
import json
import os
import random
import time
from datetime import datetime

from sentences import SENTENCES

SCORES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scores.json")
DIFFICULTIES = {"1": "easy", "2": "medium", "3": "hard"}


# ---------------------------------------------------------------------------
# Terminal helpers
# ---------------------------------------------------------------------------
class Color:
    """ANSI colour codes for terminal output."""
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def enable_windows_colors():
    """Enable ANSI colours in the Windows terminal (no effect elsewhere)."""
    if os.name == "nt":
        os.system("")


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    print(Color.CYAN + Color.BOLD)
    print("=" * 56)
    print("              ⌨️   TYPING SPEED TEST   ⌨️")
    print("=" * 56 + Color.RESET)


def countdown(seconds=3):
    """Show a short countdown before each round starts."""
    for i in range(seconds, 0, -1):
        print(f"{Color.YELLOW}  Starting in {i}...{Color.RESET}", end="\r", flush=True)
        time.sleep(1)
    print(" " * 30, end="\r")


# ---------------------------------------------------------------------------
# Core logic (pure functions - easy to test)
# ---------------------------------------------------------------------------
def calculate_results(target, typed, elapsed_seconds):
    """
    Calculate typing statistics.

    Gross WPM = (characters typed / 5) / minutes
                (a "word" is standardised as 5 characters)
    Accuracy  = matching characters / longer of the two texts * 100
    Net WPM   = Gross WPM * accuracy
    """
    elapsed_seconds = max(elapsed_seconds, 0.01)  # avoid division by zero
    minutes = elapsed_seconds / 60

    gross_wpm = (len(typed) / 5) / minutes

    matcher = difflib.SequenceMatcher(None, target, typed)
    matched_chars = sum(block.size for block in matcher.get_matching_blocks())
    longest = max(len(target), len(typed), 1)
    accuracy = matched_chars / longest * 100

    net_wpm = gross_wpm * (accuracy / 100)

    target_words = target.split()
    typed_words = typed.split()
    correct_words = 0
    for i in range(min(len(target_words), len(typed_words))):
        if target_words[i] == typed_words[i]:
            correct_words += 1

    return {
        "gross_wpm": round(gross_wpm, 1),
        "net_wpm": round(net_wpm, 1),
        "accuracy": round(accuracy, 1),
        "time": round(elapsed_seconds, 2),
        "correct_words": correct_words,
        "total_words": len(target_words),
    }


def highlight_words(target, typed):
    """Return the typed text with correct words in green and wrong ones in red."""
    target_words = target.split()
    typed_words = typed.split()
    output = []
    for i in range(len(typed_words)):
        word = typed_words[i]
        if i < len(target_words) and word == target_words[i]:
            output.append(Color.GREEN + word + Color.RESET)
        else:
            output.append(Color.RED + word + Color.RESET)
    # Show any words the user missed at the end
    for i in range(len(typed_words), len(target_words)):
        output.append(Color.RED + "_" * len(target_words[i]) + Color.RESET)
    return " ".join(output)


def get_rating(net_wpm):
    """Give a fun rating based on Net WPM."""
    if net_wpm >= 70:
        return "🚀 Lightning Fingers!"
    elif net_wpm >= 50:
        return "🔥 Excellent!"
    elif net_wpm >= 35:
        return "👍 Good job!"
    elif net_wpm >= 20:
        return "🙂 Keep practising!"
    else:
        return "🐢 Slow and steady - practice daily!"


# ---------------------------------------------------------------------------
# Score storage
# ---------------------------------------------------------------------------
def load_scores():
    if not os.path.exists(SCORES_FILE):
        return []
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_score(name, difficulty, result):
    scores = load_scores()
    scores.append({
        "name": name,
        "difficulty": difficulty,
        "net_wpm": result["net_wpm"],
        "accuracy": result["accuracy"],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    with open(SCORES_FILE, "w", encoding="utf-8") as f:
        json.dump(scores, f, indent=2)


# ---------------------------------------------------------------------------
# Game screens
# ---------------------------------------------------------------------------
def play_round(round_no, total_rounds, difficulty):
    """Play one round and return its results."""
    target = random.choice(SENTENCES[difficulty])

    print(f"\n{Color.BOLD}Round {round_no}/{total_rounds}  "
          f"[{difficulty.upper()}]{Color.RESET}")
    print("Type the sentence below exactly, then press Enter.\n")
    countdown()

    print(f"{Color.CYAN}{Color.BOLD}  {target}{Color.RESET}\n")
    start = time.time()
    typed = input("  ➜ ").strip()
    elapsed = time.time() - start

    result = calculate_results(target, typed, elapsed)

    print("\n  Your typing: " + highlight_words(target, typed))
    print(f"\n  ⏱  Time taken  : {result['time']} s")
    print(f"  ⚡ Gross speed : {result['gross_wpm']} WPM")
    print(f"  🎯 Accuracy    : {result['accuracy']} %")
    print(f"  ✅ Correct words: {result['correct_words']}/{result['total_words']}")
    print(f"  {Color.BOLD}🏁 Net speed   : {result['net_wpm']} WPM{Color.RESET}")
    print(f"  {get_rating(result['net_wpm'])}")
    return result


def start_test(name):
    print("\nChoose difficulty:  1) Easy   2) Medium   3) Hard")
    difficulty = DIFFICULTIES.get(input("Enter choice (1-3): ").strip(), "medium")

    rounds_input = input("How many rounds? (1-5, default 3): ").strip()
    rounds = int(rounds_input) if rounds_input.isdigit() and 1 <= int(rounds_input) <= 5 else 3

    results = []
    for r in range(1, rounds + 1):
        results.append(play_round(r, rounds, difficulty))
        if r < rounds:
            input(f"\n{Color.YELLOW}Press Enter for the next round...{Color.RESET}")

    # Session summary (average of all rounds)
    avg = {
        "net_wpm": round(sum(x["net_wpm"] for x in results) / rounds, 1),
        "accuracy": round(sum(x["accuracy"] for x in results) / rounds, 1),
    }
    best = max(x["net_wpm"] for x in results)

    print(Color.CYAN + "\n" + "=" * 56)
    print("                 📊 SESSION SUMMARY")
    print("=" * 56 + Color.RESET)
    print(f"  Player        : {name}")
    print(f"  Difficulty    : {difficulty.capitalize()}")
    print(f"  Rounds played : {rounds}")
    print(f"  Average speed : {avg['net_wpm']} WPM")
    print(f"  Average accuracy: {avg['accuracy']} %")
    print(f"  Best round    : {best} WPM")
    print(f"  {get_rating(avg['net_wpm'])}")

    save_score(name, difficulty, avg)
    print(f"\n{Color.GREEN}Score saved to the leaderboard!{Color.RESET}")


def show_leaderboard():
    scores = load_scores()
    if not scores:
        print("\nNo scores yet. Be the first to play!")
        return
    for level in ("easy", "medium", "hard"):
        level_scores = [s for s in scores if s["difficulty"] == level]
        if not level_scores:
            continue
        level_scores.sort(key=lambda s: s["net_wpm"], reverse=True)
        print(f"\n{Color.BOLD}🏆 Top 5 - {level.capitalize()}{Color.RESET}")
        print(f"  {'Rank':<6}{'Name':<15}{'WPM':<8}{'Accuracy':<10}Date")
        rank = 1
        for s in level_scores[:5]:
            print(f"  {rank:<6}{s['name'][:14]:<15}{s['net_wpm']:<8}"
                  f"{str(s['accuracy']) + '%':<10}{s['date']}")
            rank += 1


def show_history(name):
    mine = [s for s in load_scores() if s["name"].lower() == name.lower()]
    if not mine:
        print(f"\nNo history for {name} yet.")
        return
    print(f"\n{Color.BOLD}📈 History for {name}{Color.RESET}")
    for s in mine[-10:]:
        print(f"  {s['date']}  {s['difficulty']:<7} {s['net_wpm']:>6} WPM  {s['accuracy']:>5}%")
    avg = sum(s["net_wpm"] for s in mine) / len(mine)
    print(f"\n  Tests taken: {len(mine)} | Average: {avg:.1f} WPM | "
          f"Best: {max(s['net_wpm'] for s in mine)} WPM")


def show_instructions():
    print(f"""
{Color.BOLD}How it works{Color.RESET}
  1. Pick a difficulty and number of rounds.
  2. After the countdown, a sentence appears.
  3. Type it exactly (capitals and punctuation count) and press Enter.

{Color.BOLD}How scores are calculated{Color.RESET}
  • Gross WPM = (characters typed ÷ 5) ÷ minutes taken
  • Accuracy  = how closely your text matches the sentence
  • Net WPM   = Gross WPM × Accuracy   ← your real score

{Color.BOLD}Speed guide{Color.RESET}
  < 20 WPM beginner | 20-35 average | 35-50 good | 50-70 fast | 70+ pro
""")


# ---------------------------------------------------------------------------
# Main menu
# ---------------------------------------------------------------------------
def main():
    enable_windows_colors()
    clear_screen()
    print_banner()

    name = input("\nEnter your name: ").strip() or "Player"
    print(f"\nWelcome, {Color.BOLD}{name}{Color.RESET}! Let's test your typing speed.")

    while True:
        print(f"\n{Color.BOLD}--- MAIN MENU ---{Color.RESET}")
        print("1) Start typing test")
        print("2) Leaderboard")
        print("3) My history")
        print("4) Instructions")
        print("5) Exit")
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            start_test(name)
        elif choice == "2":
            show_leaderboard()
        elif choice == "3":
            show_history(name)
        elif choice == "4":
            show_instructions()
        elif choice == "5":
            print(f"\nThanks for playing, {name}! Keep practising. 👋\n")
            break
        else:
            print(f"{Color.RED}Invalid choice, please enter 1-5.{Color.RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExited. Goodbye! 👋\n")
