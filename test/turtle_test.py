import turtle
import math

# --- Setup ---
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("4D Tesseract – Kamera + POV + Zoom")
screen.tracer(0)

t = turtle.Turtle()
t.hideturtle()
t.speed(0)
t.width(2)
t.color("cyan")

# --- 4D Hypercube Points ---
points_4d = []
for x in (-1, 1):
    for y in (-1, 1):
        for z in (-1, 1):
            for w in (-1, 1):
                points_4d.append([x, y, z, w])

# --- Edges ---
edges = []
for i in range(len(points_4d)):
    for j in range(i + 1, len(points_4d)):
        if sum(a != b for a, b in zip(points_4d[i], points_4d[j])) == 1:
            edges.append((i, j))

# --- 4D Rotation ---
ax = 0.01
ay = 0.01
az = 0.01

# --- Kamera Rotation ---
cam_x = 0.0
cam_y = 0.0
cam_z = 0.0

# --- Kamera Zoom ---
zoom = 150

# --- 4D Rotation ---
def rotate_plane(p, i1, i2, angle):
    c = math.cos(angle)
    s = math.sin(angle)
    x = p[i1]
    y = p[i2]
    p[i1] = x * c - y * s
    p[i2] = x * s + y * c

def rotate_4d(p):
    p = p[:]
    rotate_plane(p, 0, 3, ax)
    rotate_plane(p, 1, 3, ay)
    rotate_plane(p, 2, 3, az)
    return p

# --- Kamera Rotation in 3D ---
def rotate_camera(p):
    x, y, z = p

    # Y-Achse
    cy = math.cos(cam_y)
    sy = math.sin(cam_y)
    x, z = x * cy - z * sy, x * sy + z * cy

    # X-Achse
    cx = math.cos(cam_x)
    sx = math.sin(cam_x)
    y, z = y * cx - z * sx, y * sx + z * cx

    # Z-Achse (Roll)
    cz = math.cos(cam_z)
    sz = math.sin(cam_z)
    x, y = x * cz - y * sz, x * sz + y * cz

    return [x, y, z]

# --- Projektion ---
def project_4d_to_3d(p):
    x, y, z, w = p
    w = max(-1.2, min(1.2, w))
    f = 2.2 / (2.2 - w)
    return [x * f, y * f, z * f]

def project_3d_to_2d(p):
    x, y, z = p
    z = max(-2.8, min(2.8, z))
    f = 3.5 / (3.5 - z)
    return [x * f * zoom, y * f * zoom]

# --- Steuerung 4D ---
def inc_xw():  # D
    global ax
    ax += 0.01

def dec_xw():  # A
    global ax
    ax -= 0.01

def inc_yw():  # W
    global ay
    ay += 0.01

def dec_yw():  # S
    global ay
    ay -= 0.01

def inc_zw():  # E
    global az
    az += 0.01

def dec_zw():  # Q
    global az
    az -= 0.01

# --- Kamera Steuerung ---
def cam_up():    # I
    global cam_x
    cam_x += 0.05

def cam_down():  # K
    global cam_x
    cam_x -= 0.05

def cam_left():  # J
    global cam_y
    cam_y += 0.05

def cam_right(): # L
    global cam_y
    cam_y -= 0.05

def cam_roll_left():  # U
    global cam_z
    cam_z += 0.05

def cam_roll_right(): # O
    global cam_z
    cam_z -= 0.05

# --- Zoom ---
def zoom_in():
    global zoom
    zoom += 10

def zoom_out():
    global zoom
    zoom = max(10, zoom - 10)

# --- Tastatur aktivieren ---
screen.listen()

# 4D Rotation
screen.onkeypress(inc_yw, "w")
screen.onkeypress(dec_yw, "s")
screen.onkeypress(inc_xw, "d")
screen.onkeypress(dec_xw, "a")
screen.onkeypress(inc_zw, "e")
screen.onkeypress(dec_zw, "q")

# Kamera
screen.onkeypress(cam_up, "i")
screen.onkeypress(cam_down, "k")
screen.onkeypress(cam_left, "j")
screen.onkeypress(cam_right, "l")
screen.onkeypress(cam_roll_left, "u")
screen.onkeypress(cam_roll_right, "o")

# Zoom
screen.onkeypress(zoom_in, "plus")
screen.onkeypress(zoom_out, "minus")


while True:
    t.clear()
    proj = []

    for p in points_4d:
        p4 = rotate_4d(p)
        p3 = project_4d_to_3d(p4)
        p3 = rotate_camera(p3)
        p2 = project_3d_to_2d(p3)
        proj.append(p2)

    for a, b in edges:
        x1, y1 = proj[a]
        x2, y2 = proj[b]
        t.penup()
        t.goto(x1, y1)
        t.pendown()
        t.goto(x2, y2)

    screen.update()
