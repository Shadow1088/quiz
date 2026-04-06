**Overview**

This program is a Python-based implementation of a word-guessing game using the Pygame library. It challenges the user to identify a hidden surname through a series of logical deductions.

**Core Logic**

The program operates on a feedback loop based on user input:

    Target Word: A surname is randomly selected from a JSON database at the start of each round.

    Attempt Limit: The user is granted 10 attempts to guess the correct word.

    Feedback System:

        Correct Position (2): The letter is in the correct spot (marked Green).

        Correct Letter, Wrong Position (1): The letter exists in the word but is in the wrong spot (marked Orange).

        Incorrect Letter (0): The letter does not exist in the word (marked Red).

**Continuous Play**

    Success: If a word is guessed correctly, the current score increments, and a new word is immediately loaded while maintaining the session ID and timer.

    Failure: If the user exhausts all 10 attempts, the game enters a Game Over state. The correct word is revealed, and the user must press the SPACEBAR to reset the score and start a fresh session.

**Controls**

    A-Z Keys: Input letters for the current guess.

    Backspace: Remove the last letter typed.

    Enter: Submit the completed guess.

    Spacebar: Restart the game after a loss.

**UI Structure**

The display is divided into a header and a game grid:

    Header: Displays the current score in a clear format (e.g., Score: 5), the elapsed session time, and a unique 3-byte hexadecimal session ID.

    Grid: A dynamic grid that centers itself based on the length of the target surname.
