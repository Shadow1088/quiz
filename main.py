import quiz
import pygame as pg

quiz = quiz.Quiz("guesss", 11)


# constrains
SIZE = 720
LIMIT_ROWS = 10
LIMIT_CHARS = 13


pg.init()
screen = pg.display.set_mode((SIZE, SIZE))
clock = pg.time.Clock()
running = True

while running:
    for event in pg.event.get():
        match event.type:
            case pg.QUIT:
                running = False
                continue

    screen.fill("aquamarine3")

    for i in range(quiz.length):
        pg.draw.rect(screen, "black", (0,(i)*(45+22.5), SIZE, 45), 1)
        if not i:
            # divide into thirds, each third contains a text
            # 1st third contains a score (9 digits)
            # 2nd third contains session duration
            # 3rd third contains an ID (3 byte hex code)
        for j in range(len(quiz.guess)):
            if len(quiz.guess)%2:
                pg.draw.rect(screen, "black", (((j)*45)+SIZE//4+22.5 , i*(45+22.5), 45, 45), 1)
            else:
                pg.draw.rect(screen, "black", (((j)*45)+SIZE//4+45 , i*(45+22.5), 45, 45), 1)

    pg.display.flip()
