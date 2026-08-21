import glfw
from OpenGL.GL import *
from OpenGL.GLU import *


def bresenham(x1, y1, x2, y2):

    pixels = []

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    error = dx - dy

    while True:

        pixels.append((x1, y1))

        if x1 == x2 and y1 == y2:
            break

        e2 = 2 * error

        if e2 > -dy:
            error -= dy
            x1 += sx

        if e2 < dx:
            error += dx
            y1 += sy

    return pixels


# ---------------- USER INPUT ----------------

x1 = int(input("Enter x1: "))
y1 = int(input("Enter y1: "))

x2 = int(input("Enter x2: "))
y2 = int(input("Enter y2: "))


# Generate pixels
pixels = bresenham(x1, y1, x2, y2)

print("\nPixels generated using Bresenham:")

for pixel in pixels:
    print(pixel)


# ---------------- GLFW ----------------

if not glfw.init():
    raise Exception("GLFW initialization failed")


window = glfw.create_window(
    800,
    600,
    "Bresenham Line Drawing Algorithm",
    None,
    None
)

if not window:
    glfw.terminate()
    raise Exception("GLFW window creation failed")


glfw.make_context_current(window)


# ---------------- OPENGL SETUP ----------------

glClearColor(0.0, 0.0, 0.0, 1.0)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()

gluOrtho2D(0, 800, 0, 600)

glMatrixMode(GL_MODELVIEW)
glLoadIdentity()


# ---------------- DRAW ----------------

while not glfw.window_should_close(window):

    glClear(GL_COLOR_BUFFER_BIT)

    # Pixel size
    glPointSize(6)

    # Green pixels
    glColor3f(0.0, 1.0, 0.0)

    glBegin(GL_POINTS)

    for x, y in pixels:
        glVertex2i(x, y)

    glEnd()

    glfw.swap_buffers(window)

    glfw.poll_events()


glfw.terminate()