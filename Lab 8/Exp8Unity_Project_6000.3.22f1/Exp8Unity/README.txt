EXPERIMENT 8 - Basic vertex and fragment shaders (Unity)

1. Extract the zip fully.
2. Unity Hub > Projects > Add > Add project from disk > select the Exp8Unity folder (the one that contains Assets).
3. Use editor 6000.3.22f1 (or any Unity 6 editor you have installed).
4. Open the project. The scene builds automatically (if not: top menu Lab > Build Experiment 8 Scene).
5. Press Play. A red/green/blue triangle spins.
   Q/E rotate, arrow keys translate, Z/X scale, Space = animation on/off.

Shader file: Assets/Shaders/Exp8_VertexFragment.shader
Pink triangle = shader compile error: open the Console and send the message.
Input error: Edit > Project Settings > Player > Other Settings > Active Input Handling = Both.

VIVA POINTS
- Vertex shader: runs once per vertex, outputs the final position (here: M = T*R*S applied in homogeneous coordinates).
- Fragment shader: runs once per pixel, outputs the color (here: interpolated vertex color * tint).
- The rasterizer between them interpolates vertex colors across the triangle (the gradient).
- C# sends values to the shader with Material.SetFloat / SetVector (uniforms).
- Unity uses ShaderLab/HLSL; OpenGL uses GLSL. The pipeline stages are the same.
