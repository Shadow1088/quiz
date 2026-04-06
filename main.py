import pygame as pg
import json, hashlib, secrets, unicodedata, os
from datetime import datetime

# Configuration
SIZE = 720
GRID_SIZE = 55
MARGIN = 10
FPS = 60
C_BG = pg.Color("aquamarine3")
C_ORANGE, C_RED = (255, 152, 0), (244, 67, 54)

class CompetitionApp:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SIZE, SIZE))
        self.clock = pg.time.Clock()
        self.font_ui = pg.font.SysFont("monospace", 22, bold=True)
        self.font_grid = pg.font.SysFont("monospace", 32, bold=True)

        # Session Data
        self.score = 120
        self.session_id = secrets.token_hex(3).upper()
        self.start_time = datetime.now()

        # Load Levels (Assumes security hashing script was run)
        try:
            with open("names.json", "r") as f:
                self.levels = json.load(f)
        except:
            self.levels = []

        self.current_lvl_idx = 0
        self.load_level()

    def load_level(self):
        if self.current_lvl_idx >= len(self.levels):
            return

        lvl = self.levels[self.current_lvl_idx]
        self.target_hash = lvl["hash"]
        # Note: In a real contest, you'd store the 'answer' as a secret
        # or load it only for color-checking to keep the hash secure.
        # For this demo, we assume lvl['answer'] exists for Wordle logic.
        self.target_word = lvl.get("answer", "PYTHON").upper()

        self.guesses = [] # Stores (string, color_map)
        self.current_str = ""
        self.game_over = False
        self.won = False

        # Image Loading Logic
        img_path = f"{lvl.get('image', 'missing.png')}"
        if not os.path.exists(img_path):
            img_path = "basic.jpg"

        try:
            self.mystery_img = pg.image.load(img_path)
            self.mystery_img = pg.transform.scale(self.mystery_img, (SIZE, SIZE))
        except:
            # Final fallback if even basic.png is missing
            self.mystery_img = pg.Surface((SIZE, SIZE))
            self.mystery_img.fill((200, 200, 200))

    def get_color_map(self, guess):
        res = []
        for i, char in enumerate(guess):
            if char == self.target_word[i]: res.append(2)
            elif char in self.target_word: res.append(1)
            else: res.append(0)
        return res

    def draw(self):
        self.screen.fill(C_BG)

        # Header
        elapsed = datetime.now() - self.start_time
        time_str = f"{int(elapsed.total_seconds()//60):02}:{int(elapsed.total_seconds()%60):02}"
        self.screen.blit(self.font_ui.render(f"Score: {self.score}", True, "black"), (50, 25))
        self.screen.blit(self.font_ui.render(time_str, True, "black"), (SIZE//2-35, 25))
        self.screen.blit(self.font_ui.render(f"ID: {self.session_id}", True, "black"), (SIZE-160, 25))

        # Grid Logic
        word_len = len(self.target_word)
        start_x = (SIZE - (word_len * (GRID_SIZE + MARGIN))) // 2

        for row in range(10):
            for col in range(word_len):
                rect = pg.Rect(start_x + col * (GRID_SIZE + MARGIN), 100 + row * (GRID_SIZE + MARGIN), GRID_SIZE, GRID_SIZE)

                char = ""
                bg_color = (40, 40, 40) # Default dark
                show_img = False

                if row < len(self.guesses):
                    word, colors = self.guesses[row]
                    char = word[col]
                    if colors[col] == 2: # CORRECT (GREEN)
                        show_img = True
                    elif colors[col] == 1: bg_color = C_ORANGE
                    else: bg_color = C_RED
                elif row == len(self.guesses) and col < len(self.current_str):
                    char = self.current_str[col]
                    bg_color = (0, 0, 0)

                # Draw the Tile
                if show_img:
                    # Reveal the specific part of the person's photo
                    self.screen.blit(self.mystery_img, rect, rect)
                    pg.draw.rect(self.screen, (255, 255, 255), rect, 2) # White border for image tiles
                else:
                    pg.draw.rect(self.screen, bg_color, rect)

                if char:
                    txt = self.font_grid.render(char, True, "white")
                    self.screen.blit(txt, txt.get_rect(center=rect.center))

        if self.game_over:
            prompt = "WINNER! SPACE TO NEXT" if self.won else f"LOST! WORD: {self.target_word}. SPACE TO RESET"
            txt = self.font_ui.render(prompt, True, "black")
            self.screen.blit(txt, (SIZE//2 - txt.get_width()//2, SIZE - 60))

        pg.display.flip()

    def run(self):
        while True:
            self.draw()
            for event in pg.event.get():
                if event.type == pg.QUIT: return
                if event.type == pg.KEYDOWN:
                    if self.game_over:
                        if event.key == pg.K_SPACE:
                            if self.won: self.current_lvl_idx += 1
                            else: self.score = 120 # Reset score on loss
                            self.load_level()
                    else:
                        if event.key == pg.K_BACKSPACE:
                            self.current_str = self.current_str[:-1]
                        elif event.key == pg.K_RETURN and len(self.current_str) == len(self.target_word):
                            colors = self.get_color_map(self.current_str)
                            self.guesses.append((self.current_str, colors))

                            if self.current_str == self.target_word:
                                self.won = True
                                self.game_over = True
                            elif len(self.guesses) >= 10:
                                self.game_over = True
                            else:
                                if not self.won: self.score -= 20 # Incorrect penalty
                            self.current_str = ""
                        elif len(self.current_str) < len(self.target_word):
                            if event.unicode.isalpha():
                                self.current_str += event.unicode.upper()

            self.clock.tick(FPS)

if __name__ == "__main__":
    app = CompetitionApp()
    app.run()
