import string
import re
from enum import Enum


class FeedbackColor(Enum):
    G = 1  # green: The letter is in the word and in the correct spot.
    Y = 2  # yellow: The letter is in the word but in the wrong spot.
    B = 3  # black: The letter is not in the word in any spot.


class Feedback:
    def __init__(self, guess: str, feedback_string: str):
        assert re.fullmatch(r'[a-z]{5}', guess), f"invalid guess {guess}"
        self.guess = guess
        assert re.fullmatch(r'[GYB]{5}', feedback_string), f"invalid feedback_string {feedback_string}"
        self.feedback_colors = [FeedbackColor[c] for c in feedback_string]


class WordleFilter:
    def __init__(self):
        # a set of letters that each letter slot could take
        self.letter_possibilities = [set(string.ascii_lowercase) for i in range(5)]
        # a word-level minimum count of each letter
        self.letter_to_minimum_count = dict.fromkeys(string.ascii_lowercase, 0)

    def update(self, feedback: Feedback) -> None:
        # update letter_possibilities
        y_letters = set()
        for i, feedback_color in enumerate(feedback.feedback_colors):
            if feedback_color == FeedbackColor.G:
                self.letter_possibilities[i] = {feedback.guess[i]}
            elif feedback_color == FeedbackColor.Y:
                self.letter_possibilities[i].discard(feedback.guess[i])
                y_letters.add(feedback.guess[i])
            else:  # feedback_color == FeedbackColor.B
                for j, letter_possibility in enumerate(self.letter_possibilities):
                    # Wordle will mark a letter slot as black if there are no more such letters left to guess.
                    # This includes cases where one or more other slots are already confirmed to be that letter,
                    # so do not erroneously remove the possibility from those slots.
                    if letter_possibility != {feedback.guess[i]} and (feedback.guess[i] not in y_letters or i == j):
                        letter_possibility.discard(feedback.guess[i])
        # update letter_count_requirements
        for letter in self.letter_to_minimum_count.keys():
            minimum_count = 0
            saw_y = False  # we want to count yellow-feedback letters only once
            for i in range(5):
                if self.letter_possibilities[i] == {letter}:
                    minimum_count += 1
                if letter == feedback.guess[i]:
                    if feedback.feedback_colors[i] == FeedbackColor.Y and not saw_y:
                        minimum_count += 1
                        saw_y = True
            self.letter_to_minimum_count[letter] = max(self.letter_to_minimum_count[letter], minimum_count)

    def passes_filter(self, word: str) -> bool:
        assert re.fullmatch(r'[a-z]{5}', word), f"invalid word {word}"
        # verify against letter_possibilities
        for i, letter in enumerate(word):
            if letter not in self.letter_possibilities[i]:
                return False
        # verify against letter_count_requirements
        for letter, minimum_count in self.letter_to_minimum_count.items():
            if word.count(letter) < minimum_count:
                return False
        return True
