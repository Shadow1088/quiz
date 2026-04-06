import pygame as pg
import json, secrets, os
from datetime import datetime
from quiz import Quiz

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

        self.score = 120
        self.session_id = secrets.token_hex(3).upper()
        self.start_time = datetime.now()

        self.levels = self.load_json_data()
        self.current_lvl_idx = 0
        self.load_level()

    def load_json_data(self):
        # Ensure this path matches your folder structure
        path = os.path.join("data", "competition.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
        print("Warning: JSON not found, using internal defaults.")
        return [{"answer": "EINSTEIN", "image": "einstein.png"}]

    def load_level(self):
        if self.current_lvl_idx < len(self.levels):
            lvl = self.levels[self.current_lvl_idx]
            # Initialize the Quiz logic for this specific word
            self.game = Quiz(lvl["answer"], 10)

            # Image handling with basic.png fallback
            img_name = lvl.get("image", "none.png")
            img_path = os.path.join("assets", img_name)
            if not os.path.exists(img_path):
                img_path = os.path.join("assets", "basic.png")

            try:
                self.mystery_img = pg.image.load(img_path)
                self.mystery_img = pg.transform.scale(self.mystery_img, (SIZE, SIZE))
            except:
                self.mystery_img = pg.Surface((SIZE, SIZE))
                self.mystery_img.fill((200, 200, 200))

            self.won_this_round = False
        else:
            # End of competition
            self.game = None

    def draw(self):
        self.screen.fill(C_BG)
        self.draw_header()

        if not self.game:
            txt = self.font_ui.render("COMPETITION FINISHED!", True, "black")
            self.screen.blit(txt, (SIZE//2 - txt.get_width()//2, SIZE//2))
            return

        # Grid Logic
        word_len = len(self.game.guess)
        start_x = (SIZE - (word_len * (GRID_SIZE + MARGIN))) // 2

        for row in range(10):
            for col in range(word_len):
                rect = pg.Rect(start_x + col * (GRID_SIZE + MARGIN), 100 + row * (GRID_SIZE + MARGIN), GRID_SIZE, GRID_SIZE)

                char = ""
                bg_color = (40, 40, 40)
                show_img = False

                # Past Guesses
                if row < len(self.game.past_guesses):
                    word = self.game.past_guesses[row]
                    colors = self.game.past_colors[row]
                    char = word[col]
                    if colors[col] == 2: show_img = True
                    elif colors[col] == 1: bg_color = C_ORANGE
                    else: bg_color = C_RED

                # Current Input
                elif row == len(self.game.past_guesses) and col < len(self.game.current_input):
                    char = self.game.current_input[col]
                    bg_color = (0, 0, 0)

                if show_img:
                    self.screen.blit(self.mystery_img, rect, rect)
                    pg.draw.rect(self.screen, (255, 255, 255), rect, 2)
                else:
                    pg.draw.rect(self.screen, bg_color, rect)

                if char:
                    txt = self.font_grid.render(char, True, "white")
                    self.screen.blit(txt, txt.get_rect(center=rect.center))

        pg.display.flip()

    def draw_header(self):
        elapsed = datetime.now() - self.start_time
        time_str = f"{int(elapsed.total_seconds()//60):02}:{int(elapsed.total_seconds()%60):02}"
        self.screen.blit(self.font_ui.render(f"Score: {self.score}", True, "black"), (50, 25))
        self.screen.blit(self.font_ui.render(time_str, True, "black"), (SIZE//2-35, 25))
        self.screen.blit(self.font_ui.render(f"ID: {self.session_id}", True, "black"), (SIZE-160, 25))

    def run(self):
        while True:
            self.draw()
            for event in pg.event.get():
                if event.type == pg.QUIT: return
                if event.type == pg.KEYDOWN and self.game:
                    if event.key == pg.K_BACKSPACE:
                        self.game.current_input = self.game.current_input[:-1]
                    elif event.key == pg.K_RETURN:
                        if len(self.game.current_input) == len(self.game.guess):
                            correct = self.game.submit_guess()
                            if correct:
                                self.current_lvl_idx += 1
                                self.load_level()
                            else:
                                self.score -= 20
                    else:
                        if len(self.game.current_input) < len(self.game.guess):
                            if event.unicode.isalpha():
                                self.game.current_input += event.unicode.upper()
            self.clock.tick(60)
