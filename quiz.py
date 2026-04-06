import random
import secrets
from datetime import datetime

class Quiz:
    def __init__(self, target_word: str, max_attempts: int) -> None:
        self.target_word = target_word.upper()
        self.max_attempts = max_attempts
        self.guesses = []  # List of strings
        self.current_guess = ""
        self.score = 0
        self.session_id = secrets.token_hex(3).upper() # 3-byte hex
        self.start_time = datetime.now()
        self.game_over = False
        self.won = False

    def submit_guess(self):
        if len(self.current_guess) == len(self.target_word):
            self.guesses.append(self.current_guess)
            if self.current_guess == self.target_word:
                self.won = True
                self.game_over = True
            elif len(self.guesses) >= self.max_attempts:
                self.game_over = True

            result = self.get_color_map(self.current_guess)
            self.current_guess = ""
            return result
        return None

    def get_color_map(self, guess):
        """Returns 2 for Green, 1 for Orange, 0 for Red"""
        result = []
        for i, char in enumerate(guess):
            if char == self.target_word[i]:
                result.append(2)
            elif char in self.target_word:
                result.append(1)
            else:
                result.append(0)
        return result

    def get_duration(self):
        delta = datetime.now() - self.start_time
        seconds = int(delta.total_seconds())
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        return f"{hours:02}:{mins:02}:{secs:02}"
