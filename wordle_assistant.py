#!/usr/bin/env python3
import sys
import re
from enum import Enum
from util import download_answers
from filter import FeedbackColor, Feedback, WordleFilter


class ExitCondition(Enum):
    PUZZLE_SOLVED = 1
    PUZZLE_UNSOLVED = 2
    NO_SUGGESTIONS = 3


def exit_wa(exit_condition: ExitCondition) -> None:
    message = {
        ExitCondition.PUZZLE_SOLVED: "Solved!",
        ExitCondition.PUZZLE_UNSOLVED: "Out of guesses!",
        ExitCondition.NO_SUGGESTIONS: "No more suggestions!",
    }[exit_condition]
    print()
    print(message)
    sys.exit(0)


def main():
    try:
        vocabulary = download_answers()
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    wordle_filter = WordleFilter()
    for i in range(6):
        # get user inputs
        while True:
            guessed_word = input("Guessed Word: ").lower()
            if re.fullmatch(r'[a-z]{5}', guessed_word):
                break
            print("Invalid guessed word! "
                  "Must be 5 letters.")
        while True:
            feedback_colors = input("Feedback Colors: ").upper()
            if re.fullmatch(r'[GYB]{5}', feedback_colors):
                break
            print("Invalid feedback colors! "
                  "Must be 5 colors that are 'G' (for green), 'Y' (for yellow), and/or 'B' (for black).")
        # update parameters and vocabulary
        feedback = Feedback(guessed_word, feedback_colors)
        if set(feedback.feedback_colors) == {FeedbackColor.G}:
            exit_wa(ExitCondition.PUZZLE_SOLVED)
        wordle_filter.update(Feedback(guessed_word, feedback_colors))
        filtered_vocabulary = list(filter(wordle_filter.passes_filter, vocabulary))
        if len(filtered_vocabulary) == 0:
            exit_wa(ExitCondition.NO_SUGGESTIONS)
        # output suggestions
        num_suggestions = min(10, len(filtered_vocabulary))
        suggestions_title = f"Top {num_suggestions} Suggestion(s) for Next Guess"
        print(suggestions_title)
        print("-" * len(suggestions_title))
        for suggestion in filtered_vocabulary[:num_suggestions]:
            print(f"* {suggestion}")
    exit_wa(ExitCondition.PUZZLE_UNSOLVED)


if __name__ == "__main__":
    main()
