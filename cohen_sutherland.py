import glfw
from OpenGL.GL import *
from OpenGL.GLU import *


# -------------------------------------------------
# Region codes
# -------------------------------------------------

INSIDE = 0
LEFT = 1
RIGHT = 2
BOTTOM = 4
TOP = 8


# -------------------------------------------------
# Calculate region code
# -------------------------------------------------

def compute_code(x, y, xmin, ymin, xmax, ymax):

    code = INSIDE

    if x < xmin:
        code |= LEFT

    elif x > xmax:
        code |= RIGHT

    if y < ymin:
        code |= BOTTOM

    elif y > ymax:
        code |= TOP

    return code


# -------------------------------------------------
# Cohen-Sutherland Line Clipping
# -------------------------------------------------

def cohen_sutherland(x1, y1, x2, y2,
                     xmin, ymin, xmax, ymax):

    code1 = compute_code(x1, y1, xmin, ymin, xmax, ymax)
    code2 = compute_code(x2, y2, xmin, ymin, xmax, ymax)

    while True:

        # Case 1: Both points are inside
        if code1 == 0 and code2 == 0:
            return True, x1, y1, x2, y2

        # Case 2: Both points are outside
        if code1 & code2:
            return False, None, None, None, None

        # Select point outside the clipping window
        if code1 != 0:
            code_out = code1
        else:
            code_out = code2

        # Find intersection
        if code_out & TOP:

            x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
            y = ymax

        elif code_out & BOTTOM:

            x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
            y = ymin

        elif code_out & RIGHT:

            y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
            x = xmax

        elif code_out & LEFT:

            y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
            x = xmin

        # Replace the outside point
        if code_out == code1:

            x1 = x
            y1 = y
            code1 = compute_code(
                x1, y1,
                xmin, ymin,
                xmax, ymax
            )

        else:

            x2 = x
            y2 = y
            code2 = compute_code(
                x2, y2,
                xmin, ymin,
                xmax, ymax
            )


# -------------------------------------------------
# USER INPUT
# -------------------------------------------------

print("COHEN-SUTHERLAND LINE CLIPPING")
print("--------------------------------")

print("\nEnter clipping window coordinates:")

xmin = float(input("Enter xmin: "))
ymin = float(input("Enter ymin: "))
xmax = float(input("Enter xmax: "))
ymax = float(input("Enter ymax: "))

print("\nEnter line coordinates:")

x1 = float(input("Enter x1: "))
y1 = float(input("Enter y1: "))
x2 = float(input("Enter x2: "))
y2 = float(input("Enter y2: "))


# -------------------------------------------------
# Perform clipping
# -------------------------------------------------

accepted, cx1, cy1, cx2, cy2 = cohen_sutherland(
    x1, y1, x2, y2,
    xmin, ymin, xmax, ymax
)


# -------------------------------------------------
# DISPLAY RESULT
# -------------------------------------------------

print("\n--------------------------------")
print("RESULT")
print("--------------------------------")

if accepted:

    print("Line is ACCEPTED / CLIPPED")

    print(
        f"Clipped Line: "
        f"({cx1:.2f}, {cy1:.2f}) -> "
        f"({cx2:.2f}, {cy2:.2f})"
    )

else:

    print("Line is REJECTED")
    print("Line lies completely outside the clipping window.")


# -------------------------------------------------
# GLFW INITIALIZATION
# -------------------------------------------------

if not glfw.init():
    raise Exception("GLFW initialization failed")


window = glfw.create_window(
    800,
    600,
    "Cohen-Sutherland Line Clipping",
    None,
    None
)

if not window:
    glfw.terminate()
    raise Exception("GLFW window creation failed")


glfw.make_context_current(window)


# -------------------------------------------------
# OPENGL SETUP
# -------------------------------------------------

glClearColor(0.0, 0.0, 0.0, 1.0)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()

gluOrtho2D(0, 800, 0, 600)

glMatrixMode(GL_MODELVIEW)
glLoadIdentity()


# -------------------------------------------------
# DRAW
# -------------------------------------------------

while not glfw.window_should_close(window):

    glClear(GL_COLOR_BUFFER_BIT)

    # ---------------------------------------------
    # Draw clipping window
    # ---------------------------------------------

    glColor3f(1.0, 1.0, 1.0)

    glLineWidth(2)

    glBegin(GL_LINE_LOOP)

    glVertex2f(xmin, ymin)
    glVertex2f(xmax, ymin)
    glVertex2f(xmax, ymax)
    glVertex2f(xmin, ymax)

    glEnd()


    # ---------------------------------------------
    # Draw original line
    # ---------------------------------------------

    glColor3f(1.0, 0.0, 0.0)

    glLineWidth(2)

    glBegin(GL_LINES)

    glVertex2f(x1, y1)
    glVertex2f(x2, y2)

    glEnd()


    # ---------------------------------------------
    # Draw clipped line
    # ---------------------------------------------

    if accepted:

        glColor3f(0.0, 1.0, 0.0)

        glLineWidth(4)

        glBegin(GL_LINES)

        glVertex2f(cx1, cy1)
        glVertex2f(cx2, cy2)

        glEnd()


    glfw.swap_buffers(window)

    glfw.poll_events()


# -------------------------------------------------
# CLOSE
# -------------------------------------------------

glfw.terminate()