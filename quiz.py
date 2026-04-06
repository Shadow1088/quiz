from datetime import date, datetime

class Quiz:
    def __init__(self, guess:str, length:int) -> None:
        self.guess = guess
        self.length = length
        self.score = 0
        self.session_start = datetime()

    def __str__(self) -> str:
        return "Handles guess change, string checking, score"

    def check(self, string:str):
        string = string[:len(self.guess)]
        result = []
        for i, c in enumerate(string):
            if c == self.guess[i]:
                result.append(2)
            elif c in self.guess:
                result.append(1)
            else:
                result.append(0)
        print(result)
