"""
Hangman Word Guessing Game
--------------------------
A beginner-friendly command-line game built with Python.

Features:
- Random word and category selection
- Input validation
- Duplicate-guess protection
- Six lives with ASCII hangman stages
- Score tracking across multiple rounds
"""

import random

WORDS = {
    "Programming": [
        "python", "variable", "loop", "function", "string", "integer", "keyboard"
    ],
    "Animals": ["elephant", "giraffe", "tiger", "peacock", "dolphin", "kangaroo"],
    "Fruits": ["mango", "banana", "papaya", "guava", "pineapple", "orange"],
    "Indian Cities": [
        "bengaluru", "mysuru", "chennai", "mumbai", "kolkata", "hyderabad"
    ],
}

STAGES = [
    r"""
   +---+
   |   |
       |
       |
       |
       |
=========""",
    r"""
   +---+
   |   |
   O   |
       |
       |
       |
=========""",
    r"""
   +---+
   |   |
   O   |
   |   |
       |
       |
=========""",
    r"""
   +---+
   |   |
   O   |
  /|   |
       |
       |
=========""",
    r"""
   +---+
   |   |
   O   |
  /|\  |
       |
       |
=========""",
    r"""
   +---+
   |   |
   O   |
  /|\  |
  /    |
       |
=========""",
    r"""
   +---+
   |   |
   O   |
  /|\  |
  / \  |
       |
=========""",
]


def choose_word():
    """Return a random category and a random word from that category."""
    category = random.choice(list(WORDS))
    return category, random.choice(WORDS[category])


def display_word(secret, guessed_letters):
    """Show guessed letters and underscores for letters not yet found."""
    return " ".join(letter if letter in guessed_letters else "_" for letter in secret)


def get_guess(guessed_letters):
    """Ask for one valid, new alphabetic character."""
    while True:
        guess = input("Guess a letter: ").strip().lower()
        if len(guess) != 1 or not guess.isalpha() or not guess.isascii():
            print("Please enter a single English letter (a-z).")
        elif guess in guessed_letters:
            print(f"You already guessed '{guess}'. Try another letter.")
        else:
            return guess


def play_round():
    """Play one round and return True if the player wins."""
    category, secret = choose_word()
    guessed_letters = set()
    wrong_guesses = 0
    max_wrong = len(STAGES) - 1

    print(f"\nCategory: {category} | Word has {len(secret)} letters")

    while wrong_guesses < max_wrong:
        print(STAGES[wrong_guesses])
        print("Word:", display_word(secret, guessed_letters))
        print("Guessed letters:", " ".join(sorted(guessed_letters)) or "-")
        print("Lives left:", max_wrong - wrong_guesses)

        if all(letter in guessed_letters for letter in secret):
            print(f"\nCongratulations! You guessed '{secret}'!")
            return True

        guess = get_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in secret:
            occurrences = secret.count(guess)
            print(f"Correct! '{guess}' appears {occurrences} time(s).")
        else:
            wrong_guesses += 1
            print(f"Sorry, '{guess}' is not in the word.")

    print(STAGES[max_wrong])
    print(f"\nGame over! The word was '{secret}'.")
    return False


def main():
    """Run the game until the player chooses to stop."""
    print("=" * 42)
    print("          WELCOME TO HANGMAN")
    print("=" * 42)
    name = input("Enter your name: ").strip() or "Player"

    games_played = 0
    total_wins = 0

    while True:
        won = play_round()
        games_played += 1
        total_wins += int(won)
        print(f"\n{name}, score: {total_wins} win(s) out of {games_played} game(s).")

        play_again = input("Play again? (y/n): ").strip().lower()
        if play_again not in {"y", "yes"}:
            break

    print(f"\nThanks for playing, {name}! Final score: {total_wins}/{games_played}.")


if __name__ == "__main__":
    main()
