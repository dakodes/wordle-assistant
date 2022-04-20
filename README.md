Wordle Assistant is a command-line Python hint-giving companion application for [Wordle](https://www.nytimes.com/games/wordle/index.html).

### Usage

Wordle Assistant repeatedly asks for your guessed word, and the color feedback given by the game. Each time the guess and feedback are received, the program updates a filter, subsequently allowing only the words that may plausibly be the solution based on the information provided so far. Each time input is given, the top 10 (or however many are possible) words to guess next are presented as suggestions.

When providing the color feedback, you must encode as follows:

* `g` (or `G`): Green, indicating that the given letter is in the word and in the correct spot.
* `y` (or `Y`): Yellow, indicating that the given letter is in the word but in the wrong spot.
* `b` (or `B`): Black, indicating that the letter is not in the word in any spot (except possibly in other spot(s) where that letter has been marked green in the same guess).

Note: All inputs are case-insensitive.

### Sample Puzzle Solved
For example:
```
$ ./wordle_assistant.py 
Guessed Word: adieu
Feedback Colors: bbbgb
Top 10 Suggestion(s) for Next Guess
-----------------------------------
* sower
* totem
* wooer
* greet
* goner
* golem
* hyper
* comet
* other
* sweet
Guessed Word: hyper
Feedback Colors: bybgg
Top 2 Suggestion(s) for Next Guess
----------------------------------
* foyer
* flyer
Guessed Word: foyer
Feedback Colors: ggggg

Solved!
```

### Exit Conditions

Wordle Assistant will exit if any of the following conditions occur:

* You provide a list of feedback colors that is all green, indicating that you solved the puzzle.
* You used all six guess attempts and so did not solve the puzzle.
* Wordle Assistant is unable to provide any more word guess suggestions.
