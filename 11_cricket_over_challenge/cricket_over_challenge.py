"""
Cricket Over Challenge
A beginner-friendly terminal game for learning Python control flow.

Run:
    python cricket_over_challenge.py

Concepts demonstrated:
    random numbers, functions, loops, conditionals, counters, input/output,
    return values, and break.
"""

import random

TARGET = 20
BALLS_PER_OVER = 6


def get_ball_result(roll):
    """Convert a random number from 1 to 10 into a ball outcome.

    Returns a tuple: (description, runs_scored, is_out).
    This function is kept separate so it is easy to understand and test.
    """
    if roll in (1, 2):
        return "🔴 Dot ball! No run.", 0, False
    if roll in (3, 4):
        return "🏃 1 run.", 1, False
    if roll in (5, 6):
        return "🏃🏃 2 runs.", 2, False
    if roll == 7:
        return "🏃🏃🏃 3 runs! Great running!", 3, False
    if roll == 8:
        return "💥 FOUR! Beautiful shot!", 4, False
    if roll == 9:
        return "🚀 SIX! Out of the stadium!", 6, False
    if roll == 10:
        return "❌ OUT! The stumps are flying!", 0, True
    raise ValueError("roll must be an integer from 1 to 10")


def play_innings(team, target=TARGET, input_fn=input, output_fn=print, roll_fn=None):
    """Play one team's innings and return its score details.

    roll_fn is injectable so the game logic can be tested without relying
    on random outcomes. Normal gameplay uses random.randint(1, 10).
    """
    if roll_fn is None:
        roll_fn = lambda: random.randint(1, 10)

    runs = 0
    balls_faced = 0
    is_out = False

    output_fn(f"\n{team} is coming out to bat! Target: {target} runs.\n")

    for ball in range(1, BALLS_PER_OVER + 1):
        input_fn(f"Ball {ball}: press Enter to face the ball...")

        roll = roll_fn()
        description, runs_scored, is_out = get_ball_result(roll)
        balls_faced = ball

        output_fn(f"   {description}")
        runs += runs_scored
        wickets = 1 if is_out else 0
        output_fn(f"   Score: {runs}/{wickets} after {ball} ball(s)\n")

        # break ends the innings immediately after a wicket.
        if is_out:
            break

        # Stop early when the team reaches the target.
        if runs >= target:
            output_fn(f"   🎉 Target chased in {ball} balls!\n")
            break

    return {
        "team": team,
        "runs": runs,
        "balls_faced": balls_faced,
        "out": is_out,
        "target_reached": runs >= target,
    }


def run_game(input_fn=input, output_fn=print):
    """Run the team competition until the user chooses to stop."""
    best_score = -1
    best_team = ""
    next_team = "Y"

    output_fn("=" * 50)
    output_fn("        🏏  CRICKET OVER CHALLENGE  🏏")
    output_fn("=" * 50)
    output_fn(f"Each team gets ONE over ({BALLS_PER_OVER} balls). Target: {TARGET} runs.")
    output_fn("If you get OUT, your innings ends!")
    output_fn("The team with the highest score wins.\n")

    while next_team == "Y":
        team = input_fn("Enter batting team name: ").strip()
        if not team:
            team = "Unnamed Team"

        result = play_innings(team, target=TARGET, input_fn=input_fn, output_fn=output_fn)

        output_fn("-" * 50)
        output_fn(f"{team} scored {result['runs']} runs.")
        if result["target_reached"]:
            output_fn("🏆 TARGET CHASED! Well played!")
        else:
            output_fn(f"Missed the target by {TARGET - result['runs']} runs.")

        if result["runs"] > best_score:
            best_score = result["runs"]
            best_team = team
            output_fn("⭐ New highest score!")

        output_fn(f"Leader: {best_team} with {best_score} runs")
        output_fn("-" * 50)

        next_team = input_fn("\nNext team to bat? (Y/N): ").strip().upper()
        output_fn("")

    if best_team:
        output_fn("=" * 50)
        output_fn(f"🏆 WINNER: {best_team} with {best_score} runs! 🏆")
        output_fn("=" * 50)
    else:
        output_fn("No teams played this game.")

    return best_team, best_score


if __name__ == "__main__":
    run_game()
