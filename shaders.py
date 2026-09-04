import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np


# ==============================
# VERTEX SHADER
# ==============================

vertex_shader_source = """
#version 330 core

layout (location = 0) in vec3 aPos;

void main()
{
    gl_Position = vec4(aPos, 1.0);
}
"""


# ==============================
# FRAGMENT SHADER
# ==============================

fragment_shader_source = """
#version 330 core

out vec4 FragColor;

uniform vec3 color;

void main()
{
    FragColor = vec4(color, 1.0);
}
"""


# ==============================
# USER INPUT
# ==============================

print("======================================")
print(" OPENGL VERTEX AND FRAGMENT SHADERS")
print("======================================")

print("\nEnter triangle coordinates")
print("Use values between -1 and 1")

x1 = float(input("Enter x1: "))
y1 = float(input("Enter y1: "))

x2 = float(input("Enter x2: "))
y2 = float(input("Enter y2: "))

x3 = float(input("Enter x3: "))
y3 = float(input("Enter y3: "))


print("\nEnter RGB color values")
print("Values should be between 0 and 255")

r = int(input("Red   : "))
g = int(input("Green : "))
b = int(input("Blue  : "))


# Convert RGB to OpenGL range
r = r / 255.0
g = g / 255.0
b = b / 255.0


# ==============================
# VERTEX DATA
# ==============================

vertices = np.array([
    x1, y1, 0.0,
    x2, y2, 0.0,
    x3, y3, 0.0
], dtype=np.float32)


# ==============================
# INITIALIZE GLFW
# ==============================

if not glfw.init():
    raise Exception("GLFW initialization failed")


# Request OpenGL 3.3
glfw.window_hint(
    glfw.CONTEXT_VERSION_MAJOR, 3
)

glfw.window_hint(
    glfw.CONTEXT_VERSION_MINOR, 3
)

glfw.window_hint(
    glfw.OPENGL_PROFILE,
    glfw.OPENGL_CORE_PROFILE
)


# ==============================
# CREATE WINDOW
# ==============================

window = glfw.create_window(
    800,
    600,
    "Experiment 8 - Shaders",
    None,
    None
)

if window is None:
    glfw.terminate()
    raise Exception("Could not create GLFW window")


glfw.make_context_current(window)


# ==============================
# PRINT OPENGL VERSION
# ==============================

print("\nOpenGL Version:")
print(glGetString(GL_VERSION).decode())


# ==============================
# COMPILE SHADERS
# ==============================

try:

    vertex_shader = compileShader(
        vertex_shader_source,
        GL_VERTEX_SHADER
    )

    fragment_shader = compileShader(
        fragment_shader_source,
        GL_FRAGMENT_SHADER
    )

    shader_program = compileProgram(
        vertex_shader,
        fragment_shader
    )

except Exception as e:

    glfw.terminate()

    print("\nShader compilation error:")
    print(e)

    exit()


# ==============================
# CREATE VAO
# ==============================

VAO = glGenVertexArrays(1)

glBindVertexArray(VAO)


# ==============================
# CREATE VBO
# ==============================

VBO = glGenBuffers(1)

glBindBuffer(
    GL_ARRAY_BUFFER,
    VBO
)


glBufferData(
    GL_ARRAY_BUFFER,
    vertices.nbytes,
    vertices,
    GL_STATIC_DRAW
)


# ==============================
# VERTEX ATTRIBUTE
# ==============================

glVertexAttribPointer(
    0,
    3,
    GL_FLOAT,
    GL_FALSE,
    3 * vertices.itemsize,
    ctypes.c_void_p(0)
)

glEnableVertexAttribArray(0)


# Unbind
glBindBuffer(GL_ARRAY_BUFFER, 0)

glBindVertexArray(0)


# ==============================
# SHADER UNIFORM
# ==============================

glUseProgram(shader_program)

color_location = glGetUniformLocation(
    shader_program,
    "color"
)


# ==============================
# OPENGL SETTINGS
# ==============================

glClearColor(
    0.1,
    0.1,
    0.1,
    1.0
)


# ==============================
# MAIN LOOP
# ==============================

while not glfw.window_should_close(window):

    # Clear screen
    glClear(GL_COLOR_BUFFER_BIT)


    # Use shader
    glUseProgram(shader_program)


    # Set triangle color
    glUniform3f(
        color_location,
        r,
        g,
        b
    )


    # Bind VAO
    glBindVertexArray(VAO)


    # Draw triangle
    glDrawArrays(
        GL_TRIANGLES,
        0,
        3
    )


    # Unbind
    glBindVertexArray(0)


    # Display
    glfw.swap_buffers(window)

    glfw.poll_events()


# ==============================
# CLEANUP
# ==============================

glDeleteVertexArrays(
    1,
    [VAO]
)

glDeleteBuffers(
    1,
    [VBO]
)

glDeleteProgram(
    shader_program
)

glfw.terminate()