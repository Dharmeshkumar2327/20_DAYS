"""
Python Number Guessing Challenge
A beginner-friendly mini-project for practicing Python fundamentals.
"""

import random


def get_integer(prompt, minimum=None, maximum=None):
    """Read and validate an integer from the user."""
    while True:
        raw_value = input(prompt).strip()

        try:
            value = int(raw_value)
        except ValueError:
            print("Invalid input. Please enter a whole number.")
            continue

        if minimum is not None and value < minimum:
            print(f"Please enter a number greater than or equal to {minimum}.")
            continue

        if maximum is not None and value > maximum:
            print(f"Please enter a number less than or equal to {maximum}.")
            continue

        return value


def choose_difficulty():
    """Let the player choose a difficulty and return its settings."""
    difficulties = {
        "1": {"name": "Easy", "maximum": 50, "attempts": 10},
        "2": {"name": "Medium", "maximum": 100, "attempts": 7},
        "3": {"name": "Hard", "maximum": 200, "attempts": 6},
    }

    print("\nChoose your difficulty:")
    print("1. Easy   (1-50, 10 attempts)")
    print("2. Medium (1-100, 7 attempts)")
    print("3. Hard   (1-200, 6 attempts)")

    while True:
        choice = input("Enter 1, 2, or 3: ").strip()
        if choice in difficulties:
            return difficulties[choice]
        print("Please choose 1, 2, or 3.")


def play_round():
    """Play one round and return the player's score (0 if not won)."""
    difficulty = choose_difficulty()
    secret_number = random.randint(1, difficulty["maximum"])
    max_attempts = difficulty["attempts"]
    score = 0

    print(f"\nYou chose {difficulty['name']} mode.")
    print(f"I'm thinking of a number between 1 and {difficulty['maximum']}.")
    print(f"You have {max_attempts} attempts. Good luck!")

    for attempt in range(1, max_attempts + 1):
        guess = get_integer(
            f"\nAttempt {attempt}/{max_attempts} — your guess: ",
            minimum=1,
            maximum=difficulty["maximum"],
        )

        if guess == secret_number:
            remaining_attempts = max_attempts - attempt
            score = (remaining_attempts + 1) * 10
            print(f"\n🎉 Correct! The secret number was {secret_number}.")
            print(f"You scored {score} points.")
            break

        if guess < secret_number:
            print("Too low! Try a higher number.")
        else:
            print("Too high! Try a lower number.")

        remaining = max_attempts - attempt
        if remaining > 0:
            print(f"Attempts remaining: {remaining}")
    else:
        print(f"\nGame over! The secret number was {secret_number}.")
        print("You scored 0 points.")

    return score


def main():
    """Run game rounds and keep a session score."""
    total_score = 0
    rounds_played = 0
    rounds_won = 0

    print("=" * 42)
    print("       PYTHON NUMBER GUESSING CHALLENGE")
    print("=" * 42)

    while True:
        score = play_round()
        rounds_played += 1
        total_score += score

        if score > 0:
            rounds_won += 1

        print("\n--- Session Summary ---")
        print(f"Rounds played: {rounds_played}")
        print(f"Rounds won:    {rounds_won}")
        print(f"Total score:   {total_score}")

        again = input("\nPlay another round? (yes/no): ").strip().lower()
        if again not in {"yes", "y"}:
            print("\nThanks for playing. Keep practicing Python!")
            break


if __name__ == "__main__":
    main()
