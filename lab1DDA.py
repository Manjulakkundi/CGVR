import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import time


def dda(x1, y1, x2, y2):

    dx = x2 - x1
    dy = y2 - y1

    steps = max(abs(dx), abs(dy))

    x_inc = dx / steps
    y_inc = dy / steps

    x = x1
    y = y1

    pixels = []

    for i in range(steps + 1):
        pixels.append((round(x), round(y)))

        x += x_inc
        y += y_inc

    return pixels


# ---------------- USER INPUT ----------------

x1 = int(input("Enter x1: "))
y1 = int(input("Enter y1: "))

x2 = int(input("Enter x2: "))
y2 = int(input("Enter y2: "))


# Generate pixels
pixels = dda(x1, y1, x2, y2)

print("\nPixels generated using DDA:")

for pixel in pixels:
    print(pixel)


# ---------------- GLFW ----------------

if not glfw.init():
    raise Exception("GLFW initialization failed")


window = glfw.create_window(
    800,
    600,
    "DDA Line Drawing Algorithm",
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

    # White pixels
    glColor3f(1.0, 1.0, 1.0)

    glBegin(GL_POINTS)

    for x, y in pixels:
        glVertex2i(x, y)

    glEnd()

    glfw.swap_buffers(window)

    glfw.poll_events()


glfw.terminate()