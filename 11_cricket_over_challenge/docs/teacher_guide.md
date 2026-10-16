# Teacher Guide — Cricket Over Challenge

## Suggested classroom activity

**Duration:** 15–25 minutes  
**Grouping:** 4–8 teams, depending on class size  
**Goal:** Reinforce Python control flow through a simple game.

## Before class

1. Confirm Python is installed.
2. Open a terminal in the project folder.
3. Run `python cricket_over_challenge.py`.
4. Explain the rules and the ball-outcome table.

## Concepts to discuss

- Why is `random.randint(1, 10)` used?
- Why does `for ball in range(1, 7)` represent six balls?
- How do the `if` conditions map a roll to an outcome?
- Why does `break` end the innings early?
- What is the purpose of `best_score` and `best_team`?
- Why is `get_ball_result()` a separate function?
- What does `return` give back to the calling function?

## Extension challenges

1. Let a team lose more than one wicket before its innings ends.
2. Allow the teacher to set the target at the start.
3. Track fours and sixes separately.
4. Add a CSV match-history file.
5. Create a Tkinter interface.
6. Add a unit test for every possible ball outcome.

## Important note

This is a simplified classroom game. Its rules are intentionally smaller than official cricket rules so students can focus on Python fundamentals.
