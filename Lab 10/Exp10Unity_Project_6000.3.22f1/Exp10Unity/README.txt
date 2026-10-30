EXPERIMENT 10 - 3D viewing pipeline, projection and viewport mapping (Unity)

1. Extract the zip fully.
2. Unity Hub > Projects > Add > Add project from disk > select the Exp10Unity folder (the one that contains Assets).
3. Use editor 6000.3.22f1 (or any Unity 6 editor you have installed).
4. Open the project. The scene builds automatically (if not: top menu Lab > Build Experiment 10 Scene).
5. Press Play, then click inside the Game view.

WHAT YOU SEE
- Full Game view: Unity's own camera rendering the blue cube.
- Top-right panel: the SAME cube projected by our hand-written matrices (Model, View, Projection, divide by w, Viewport) and drawn with Bresenham lines.
- Top-left panel: the matrices and vertex table. Press T to change page.

CONTROLS
Arrows orbit camera | Z/X zoom | P perspective/orthographic | F/G field of view
1/2 near plane | 3/4 far plane | V viewport size | R spin cube | T next page

If the Console shows an Input error:
Edit > Project Settings > Player > Other Settings > Active Input Handling = Both, restart Unity.

VIVA POINTS
- Pipeline: local -> (Model) world -> (View) eye -> (Projection) clip -> (divide by w) NDC [-1,1] -> (Viewport) screen pixels.
- Model matrix = translate/rotate/scale of the object. View matrix = look-at; moves the world so the camera is at the origin.
- Perspective: w_clip = z_eye, so dividing by w shrinks far objects. Orthographic: w = 1, no shrinking.
- Viewport mapping: sx = (x_ndc+1)/2 * Width, sy = (y_ndc+1)/2 * Height.
- near/far planes decide what is clipped; vertices with w <= 0 are behind the camera and are skipped.
- Unity is left-handed (camera looks down +Z in eye space), so signs differ from the OpenGL right-handed Python version.
