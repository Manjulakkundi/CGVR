"""
EXPERIMENT 8
Develop a basic OpenGL program using Vertex and Fragment Shaders.

Pipeline:
    Vertex Data (CPU) -> Vertex Shader (GPU) -> Rasterization -> Fragment Shader (GPU) -> Pixels on screen
"""

import ctypes
import glfw
from OpenGL.GL import *
import numpy as np

# ==========================================================
# 1. INITIALIZE GLFW AND CREATE A WINDOW
# ==========================================================
if not glfw.init():
    raise Exception("GLFW could not be initialized")

# Request an OpenGL 3.3 CORE profile -> required for programmable shaders
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

window = glfw.create_window(800, 600, "Experiment 8 - Vertex & Fragment Shaders", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window could not be created")

glfw.make_context_current(window)

print("OpenGL version:", glGetString(GL_VERSION).decode())


# ==========================================================
# 2. DEFINE VERTEX DATA (a triangle)
# ==========================================================
# Each vertex: (x, y, z) in Normalized Device Coordinates (-1 to 1)
vertices = np.array([
    -0.5, -0.5, 0.0,   # bottom left
     0.5, -0.5, 0.0,   # bottom right
     0.0,  0.5, 0.0    # top
], dtype=np.float32)


# ==========================================================
# 3. VERTEX SHADER SOURCE
# ==========================================================
# Runs once per vertex. Its job: decide the FINAL POSITION of each vertex.
# 'aPos' receives the vertex data we send from Python (location = 0).
# gl_Position is a built-in output every vertex shader must set.
vertex_shader_src = """
#version 330 core
layout(location = 0) in vec3 aPos;

void main()
{
    gl_Position = vec4(aPos, 1.0);
}
"""


# ==========================================================
# 4. FRAGMENT SHADER SOURCE
# ==========================================================
# Runs once per pixel (fragment) covered by the shape.
# Its job: decide the FINAL COLOR of each pixel.
# 'FragColor' is our own output variable -> the pixel color.
fragment_shader_src = """
#version 330 core
out vec4 FragColor;

void main()
{
    FragColor = vec4(1.0, 0.5, 0.2, 1.0);   // orange color (R, G, B, Alpha)
}
"""


# ==========================================================
# 5. COMPILE A SHADER (helper function)
# ==========================================================
def compile_shader(source, shader_type):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    # Check for compile errors
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        raise RuntimeError(f"Shader compilation failed:\n{error}")

    return shader


vertex_shader = compile_shader(vertex_shader_src, GL_VERTEX_SHADER)
fragment_shader = compile_shader(fragment_shader_src, GL_FRAGMENT_SHADER)


# ==========================================================
# 6. LINK SHADERS INTO A SHADER PROGRAM
# ==========================================================
# The shader program is what actually runs on the GPU during rendering.
shader_program = glCreateProgram()
glAttachShader(shader_program, vertex_shader)
glAttachShader(shader_program, fragment_shader)
glLinkProgram(shader_program)

# Check for linking errors
if not glGetProgramiv(shader_program, GL_LINK_STATUS):
    error = glGetProgramInfoLog(shader_program).decode()
    raise RuntimeError(f"Shader program linking failed:\n{error}")

# Shaders are now inside the program; the standalone objects can be deleted
glDeleteShader(vertex_shader)
glDeleteShader(fragment_shader)


# ==========================================================
# 7. SET UP VERTEX ARRAY OBJECT (VAO) AND VERTEX BUFFER OBJECT (VBO)
# ==========================================================
# VBO: uploads our vertex data to GPU memory.
# VAO: remembers HOW to read that data (layout, stride, offset) so we
#      don't need to reconfigure it every frame.
VAO = glGenVertexArrays(1)
VBO = glGenBuffers(1)

glBindVertexArray(VAO)

glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# Tell OpenGL how to interpret the vertex data at location = 0 (aPos)
# 3 floats per vertex, not normalized, tightly packed (stride = 3 * float size)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * vertices.itemsize, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)

# Unbind (good practice, prevents accidental modification)
glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)


# ==========================================================
# 8. RENDER LOOP
# ==========================================================
glClearColor(0.1, 0.1, 0.15, 1.0)  # dark background

while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(shader_program)   # activate our shader program
    glBindVertexArray(VAO)         # bind the vertex data + layout
    glDrawArrays(GL_TRIANGLES, 0, 3)   # draw 3 vertices as 1 triangle

    glfw.swap_buffers(window)


# ==========================================================
# 9. CLEANUP
# ==========================================================
glDeleteVertexArrays(1, [VAO])
glDeleteBuffers(1, [VBO])
glDeleteProgram(shader_program)
glfw.terminate()
