import pygame
import turtle
import time
import random
import math

# ----------------- CONFIG -----------------
TILE_SIZE = 30
DELAY = 0.01
BASE_SPEED = 0.08  # Grundgeschwindigkeit (Skalierung für Stick)
DEADZONE = 0.15    # Deadzone für Analogstick

# Level: X = Wand, . = Punkt, ' ' = leer
LEVEL = [
    "XXXXXXXXXXXXXXXX",
    "X..............X",
    "X.XXXX.XXXXXX..X",
    "X.X  X.X    X..X",
    "X.X  X.X XX X..X",
    "X.XXXX.X XX X..X",
    "X......X    X..X",
    "XXXXXX.XXXXXX..X",
    "X..............X",
    "XXXXXXXXXXXXXXXX",
]

# ----------------- TURTLE SETUP -----------------
screen = turtle.Screen()
screen.setup(800, 600)
screen.bgcolor("black")
screen.title("Controller Pac-Man Light")
screen.tracer(0)

drawer = turtle.Turtle()
drawer.hideturtle()
drawer.penup()
drawer.speed(0)
drawer.color("blue")

player = turtle.Turtle()
player.shape("circle")
player.color("yellow")
player.penup()
player.speed(0)

score_t = turtle.Turtle()
score_t.hideturtle()
score_t.penup()
score_t.color("white")
score_t.goto(-380, 260)

walls = []
dots = []
score = 0

# ----------------- HELFER -----------------
def grid_to_xy(col, row):
    x = -len(LEVEL[0]) * TILE_SIZE / 2 + col * TILE_SIZE + TILE_SIZE / 2
    y = len(LEVEL) * TILE_SIZE / 2 - row * TILE_SIZE - TILE_SIZE / 2
    return x, y

def update_score():
    score_t.clear()
    score_t.write(f"Score: {score}", font=("Arial", 16, "bold"))

def can_move_to(x, y):
    for wx, wy in walls:
        if abs(x - wx) < TILE_SIZE * 0.5 and abs(y - wy) < TILE_SIZE * 0.5:
            return False
    return True

# ----------------- LEVEL ZEICHNEN -----------------
player_start = None

for row_idx, row in enumerate(LEVEL):
    for col_idx, ch in enumerate(row):
        x, y = grid_to_xy(col_idx, row_idx)
        if ch == "X":
            drawer.goto(x - TILE_SIZE / 2, y - TILE_SIZE / 2)
            drawer.begin_fill()
            for _ in range(4):
                drawer.forward(TILE_SIZE)
                drawer.left(90)
            drawer.end_fill()
            walls.append((x, y))
        elif ch == ".":
            dot = turtle.Turtle()
            dot.shape("circle")
            dot.color("white")
            dot.shapesize(0.2)
            dot.penup()
            dot.goto(x, y)
            dots.append(dot)
        elif ch == " ":
            pass

# Startposition: irgendwo frei
if player_start is None:
    player_start = grid_to_xy(1, 1)

player.goto(player_start)
update_score()

# ----------------- PYGAME SETUP -----------------
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("Kein Controller gefunden.")
    pygame.quit()
    raise SystemExit

controller = pygame.joystick.Joystick(0)
controller.init()

axe = [0.0] * 6
btn = [False] * 20

# ----------------- MAIN LOOP -----------------
running = True
while running:
    # --- Pygame Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.JOYBUTTONDOWN:
            if event.button < len(btn):
                btn[event.button] = True

        elif event.type == pygame.JOYBUTTONUP:
            if event.button < len(btn):
                btn[event.button] = False

        elif event.type == pygame.JOYAXISMOTION:
            if event.axis < len(axe):
                axe[event.axis] = round(event.value, 3)

    # --- Steuerung: linker Stick als Velocity ---
    raw_vx = axe[0]
    raw_vy = -axe[1]

    # Deadzone
    vx = raw_vx if abs(raw_vx) > DEADZONE else 0.0
    vy = raw_vy if abs(raw_vy) > DEADZONE else 0.0

    # Speed-Boost auf Button 0
    speed = BASE_SPEED * (2.0 if btn[0] else 1.0)

    # Nächste Position berechnen
    px, py = player.position()
    new_x = px + vx * speed * TILE_SIZE
    new_y = py + vy * speed * TILE_SIZE

    # Physik: nur bewegen, wenn Ziel nicht Wand ist
    if can_move_to(new_x, new_y):
        player.goto(new_x, new_y)
    else:
        # Versuche getrennt X und Y (sliding an Wänden)
        if can_move_to(new_x, py):
            player.goto(new_x, py)
        elif can_move_to(px, new_y):
            player.goto(px, new_y)
        # sonst komplett blockiert

    # Dots einsammeln
    for dot in dots[:]:
        if player.distance(dot) < 10:
            dot.hideturtle()
            dots.remove(dot)
            score += 10
            update_score()

    # Optional: Button 1 = Reset Position
    if btn[1]:
        player.goto(player_start)

    # Win-Condition
    if not dots:
        msg = turtle.Turtle()
        msg.hideturtle()
        msg.color("green")
        msg.write("YOU WIN!", align="center", font=("Arial", 32, "bold"))
        running = False

    screen.update()
    time.sleep(DELAY)

pygame.quit()
