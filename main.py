import pygame as pg
import json
import random
from quiz import Quiz

# Configuration
SIZE = 720
GRID_SIZE = 50
MARGIN = 10
FPS = 60

# Colors
COLOR_BG = pg.Color("aquamarine3")
COLOR_CORRECT = (76, 175, 80)    # Green
COLOR_MISPLACED = (255, 152, 0)  # Orange
COLOR_WRONG = (244, 67, 54)     # Red

def load_new_word():
    try:
        with open("names.json", "r") as f:
            data = json.load(f)
        return random.choice(data["surnames"])
    except FileNotFoundError:
        return "PYTHON" # Fallback

pg.init()
screen = pg.display.set_mode((SIZE, SIZE))
font_main = pg.font.SysFont("monospace", 30, bold=True)
font_ui = pg.font.SysFont("monospace", 20)
font_small = pg.font.SysFont("monospace", 16, bold=True)
clock = pg.time.Clock()

# Initialize Game State
target = load_new_word()
game = Quiz(target, 10)
total_score = 0

running = True
while running:
    screen.fill(COLOR_BG)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.KEYDOWN:
            # Logic for Resetting when Game is Over
            if game.game_over:
                if event.key == pg.K_SPACE:
                    target = load_new_word()
                    game = Quiz(target, 10)
                    total_score = 0 # Reset score on loss and manual reset

            # Normal Gameplay Logic
            elif not game.game_over:
                if event.key == pg.K_BACKSPACE:
                    game.current_guess = game.current_guess[:-1]
                elif event.key == pg.K_RETURN:
                    if len(game.current_guess) == len(game.target_word):
                        game.submit_guess()
                        if game.won:
                            total_score += 1
                            # Load next level without resetting ID/Timer/Total Score
                            target = load_new_word()
                            old_id = game.session_id
                            old_start = game.start_time
                            game = Quiz(target, 10)
                            game.session_id = old_id
                            game.start_time = old_start
                elif len(game.current_guess) < len(game.target_word):
                    if event.unicode.isalpha():
                        game.current_guess += event.unicode.upper()

    # --- RENDER HEADER ---
    header_y = 20
    # 1. Score Format: "Score: 51"
    score_txt = font_ui.render(f"Score: {total_score}", True, "black")
    screen.blit(score_txt, (SIZE//6 - score_txt.get_width()//2, header_y))

    # 2. Duration
    time_txt = font_ui.render(game.get_duration(), True, "black")
    screen.blit(time_txt, (SIZE//2 - time_txt.get_width()//2, header_y))

    # 3. Session ID
    id_txt = font_ui.render(f"ID: {game.session_id}", True, "black")
    screen.blit(id_txt, (5*SIZE//6 - id_txt.get_width()//2, header_y))

    # --- RENDER GRID ---
    start_y = 80
    word_len = len(game.target_word)
    total_grid_width = word_len * (GRID_SIZE + MARGIN)
    start_x = (SIZE - total_grid_width) // 2

    for row in range(game.max_attempts):
        for col in range(word_len):
            rect = pg.Rect(start_x + col * (GRID_SIZE + MARGIN),
                           start_y + row * (GRID_SIZE + MARGIN),
                           GRID_SIZE, GRID_SIZE)

            color = "black"
            fill = 1
            char = ""

            if row < len(game.guesses):
                guess_str = game.guesses[row]
                char = guess_str[col]
                res = game.get_color_map(guess_str)[col]
                fill = 0
                if res == 2: color = COLOR_CORRECT
                elif res == 1: color = COLOR_MISPLACED
                else: color = COLOR_WRONG
            elif row == len(game.guesses) and col < len(game.current_guess):
                char = game.current_guess[col]

            pg.draw.rect(screen, color, rect, fill)
            if char:
                text = font_main.render(char, True, "white" if fill == 0 else "black")
                screen.blit(text, text.get_rect(center=rect.center))

    # --- GAME OVER PROMPTS ---
    if game.game_over and not game.won:
        # Show solution
        msg = f"GAME OVER! THE NAME WAS: {game.target_word}"
        lost_txt = font_small.render(msg, True, "black")
        screen.blit(lost_txt, (SIZE//2 - lost_txt.get_width()//2, SIZE - 80))

        # Reset Prompt
        prompt_txt = font_main.render("PRESS SPACE TO RESTART", True, "black")
        screen.blit(prompt_txt, (SIZE//2 - prompt_txt.get_width()//2, SIZE - 45))

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
