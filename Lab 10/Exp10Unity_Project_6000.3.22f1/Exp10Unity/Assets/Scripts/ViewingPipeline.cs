using System.Text;
using UnityEngine;

// EXPERIMENT 10 - 3D viewing pipeline with projection and viewport mapping.
//
//   local --(Model M)--> world --(View V)--> eye --(Projection P)--> clip
//   --(divide by w)--> NDC [-1,1] --(Viewport)--> 2D screen pixels
//
// Every matrix is built by hand here (no Camera.projectionMatrix etc.).
// Unity is LEFT-handed: in eye space the camera looks down +Z.
// The projected cube is drawn into a small 2D panel with Bresenham lines (Experiment 1).
// Unity's own camera is driven by the same parameters so you can compare both pictures.
public class ViewingPipeline : MonoBehaviour
{
    public Transform cube;
    public Camera cam;

    // ---- virtual camera parameters ----
    public Vector3 target = Vector3.zero;
    public float yaw = 35f, pitch = 25f, distance = 8f;
    public bool perspective = true;
    public float fov = 60f;
    public float orthoHalfHeight = 3f;
    public float nearPlane = 1f, farPlane = 20f;
    public bool spin = true;

    // ---- viewport sizes (press V to cycle) ----
    static readonly int[,] viewports = { { 320, 240 }, { 400, 400 }, { 200, 150 } };
    int vpIndex = 0;
    int W = 320, H = 240;

    // ---- cube geometry (unit cube centred on the origin) ----
    Vector3[] localVerts = new Vector3[8];
    static readonly int[,] edges =
    {
        {0,1},{2,3},{4,5},{6,7},   // edges along X
        {0,2},{1,3},{4,6},{5,7},   // edges along Y
        {0,4},{1,5},{2,6},{3,7}    // edges along Z
    };

    // ---- results of the pipeline ----
    Matrix4x4 M, V, P, PVM;
    Vector3[] world = new Vector3[8];
    Vector4[] clip = new Vector4[8];
    Vector3[] ndc = new Vector3[8];
    Vector2[] screen = new Vector2[8];
    bool[] visible = new bool[8];

    Texture2D tex;
    Color32[] pixels;
    int page = 0;
    GUIStyle mono, boxStyle;

    void Awake()
    {
        for (int i = 0; i < 8; i++)
            localVerts[i] = new Vector3(
                (i & 1) != 0 ? 0.5f : -0.5f,
                (i & 2) != 0 ? 0.5f : -0.5f,
                (i & 4) != 0 ? 0.5f : -0.5f);
        if (cam == null) cam = Camera.main;
        MakeTexture();
    }

    void MakeTexture()
    {
        W = viewports[vpIndex, 0];
        H = viewports[vpIndex, 1];
        tex = new Texture2D(W, H, TextureFormat.RGBA32, false);
        tex.filterMode = FilterMode.Point;
        pixels = new Color32[W * H];
    }

    // ===================== MATRICES (built by hand) =====================

    // View matrix: moves the world so the camera sits at the origin looking down +Z.
    static Matrix4x4 LookAtLH(Vector3 eye, Vector3 tgt, Vector3 up)
    {
        Vector3 z = (tgt - eye).normalized;           // forward
        Vector3 x = Vector3.Cross(up, z).normalized;  // right
        Vector3 y = Vector3.Cross(z, x);              // true up
        Matrix4x4 m = Matrix4x4.identity;
        m.SetRow(0, new Vector4(x.x, x.y, x.z, -Vector3.Dot(x, eye)));
        m.SetRow(1, new Vector4(y.x, y.y, y.z, -Vector3.Dot(y, eye)));
        m.SetRow(2, new Vector4(z.x, z.y, z.z, -Vector3.Dot(z, eye)));
        m.SetRow(3, new Vector4(0, 0, 0, 1));
        return m;
    }

    // Perspective projection: w_clip = z_eye, so dividing by w gives perspective foreshortening.
    static Matrix4x4 PerspectiveLH(float fovDeg, float aspect, float n, float f)
    {
        float t = 1f / Mathf.Tan(fovDeg * Mathf.Deg2Rad * 0.5f);
        Matrix4x4 m = Matrix4x4.zero;
        m[0, 0] = t / aspect;
        m[1, 1] = t;
        m[2, 2] = (f + n) / (f - n);
        m[2, 3] = -2f * f * n / (f - n);
        m[3, 2] = 1f;
        return m;
    }

    // Orthographic (parallel) projection: w stays 1, so no foreshortening.
    static Matrix4x4 OrthographicLH(float halfW, float halfH, float n, float f)
    {
        Matrix4x4 m = Matrix4x4.zero;
        m[0, 0] = 1f / halfW;
        m[1, 1] = 1f / halfH;
        m[2, 2] = 2f / (f - n);
        m[2, 3] = -(f + n) / (f - n);
        m[3, 3] = 1f;
        return m;
    }

    // ===================== UPDATE =====================

    void Update()
    {
        float dt = Time.deltaTime;

        // ---- input ----
        if (Input.GetKey(KeyCode.LeftArrow))  yaw -= 60f * dt;
        if (Input.GetKey(KeyCode.RightArrow)) yaw += 60f * dt;
        if (Input.GetKey(KeyCode.UpArrow))    pitch += 40f * dt;
        if (Input.GetKey(KeyCode.DownArrow))  pitch -= 40f * dt;
        if (Input.GetKey(KeyCode.Z)) distance -= 4f * dt;
        if (Input.GetKey(KeyCode.X)) distance += 4f * dt;
        if (Input.GetKey(KeyCode.F)) fov -= 30f * dt;
        if (Input.GetKey(KeyCode.G)) fov += 30f * dt;
        if (Input.GetKey(KeyCode.Alpha1)) nearPlane -= 3f * dt;
        if (Input.GetKey(KeyCode.Alpha2)) nearPlane += 3f * dt;
        if (Input.GetKey(KeyCode.Alpha3)) farPlane -= 6f * dt;
        if (Input.GetKey(KeyCode.Alpha4)) farPlane += 6f * dt;
        if (Input.GetKeyDown(KeyCode.P)) perspective = !perspective;
        if (Input.GetKeyDown(KeyCode.R)) spin = !spin;
        if (Input.GetKeyDown(KeyCode.T)) page = (page + 1) % 3;
        if (Input.GetKeyDown(KeyCode.V))
        {
            vpIndex = (vpIndex + 1) % (viewports.GetLength(0));
            MakeTexture();
        }

        pitch = Mathf.Clamp(pitch, -80f, 80f);
        distance = Mathf.Clamp(distance, 3f, 20f);
        fov = Mathf.Clamp(fov, 20f, 120f);
        nearPlane = Mathf.Clamp(nearPlane, 0.1f, 15f);
        farPlane = Mathf.Max(farPlane, nearPlane + 1f);

        if (spin && cube != null) cube.Rotate(15f * dt, 30f * dt, 0f);

        // ---- virtual camera position ----
        float yr = yaw * Mathf.Deg2Rad, pr = pitch * Mathf.Deg2Rad;
        Vector3 eye = target + distance * new Vector3(
            Mathf.Cos(pr) * Mathf.Sin(yr),
            Mathf.Sin(pr),
            -Mathf.Cos(pr) * Mathf.Cos(yr));

        // ---- drive Unity's real camera with the same parameters (for comparison) ----
        if (cam != null)
        {
            cam.transform.position = eye;
            cam.transform.rotation = Quaternion.LookRotation(target - eye, Vector3.up);
            cam.orthographic = !perspective;
            cam.fieldOfView = fov;
            cam.orthographicSize = orthoHalfHeight;
            cam.nearClipPlane = nearPlane;
            cam.farClipPlane = farPlane;
        }

        // ---- THE PIPELINE ----
        Vector3 pos = cube != null ? cube.position : Vector3.zero;
        Quaternion rot = cube != null ? cube.rotation : Quaternion.identity;
        Vector3 scl = cube != null ? cube.localScale : Vector3.one * 2f;

        M = Matrix4x4.TRS(pos, rot, scl);                        // 1. Model
        V = LookAtLH(eye, target, Vector3.up);                   // 2. View
        float aspect = (float)W / H;
        P = perspective
            ? PerspectiveLH(fov, aspect, nearPlane, farPlane)    // 3. Projection
            : OrthographicLH(orthoHalfHeight * aspect, orthoHalfHeight, nearPlane, farPlane);
        PVM = P * V * M;

        for (int i = 0; i < 8; i++)
        {
            Vector4 local = new Vector4(localVerts[i].x, localVerts[i].y, localVerts[i].z, 1f);
            Vector4 w4 = M * local;                              // local -> world
            Vector4 e4 = V * w4;                                 // world -> eye
            Vector4 c4 = P * e4;                                 // eye   -> clip
            world[i] = new Vector3(w4.x, w4.y, w4.z);
            clip[i] = c4;

            visible[i] = c4.w > 0.0001f;
            if (visible[i])
            {
                ndc[i] = new Vector3(c4.x / c4.w, c4.y / c4.w, c4.z / c4.w);          // 4. divide by w
                screen[i] = new Vector2((ndc[i].x + 1f) * 0.5f * W,                  // 5. viewport
                                        (ndc[i].y + 1f) * 0.5f * H);
            }
        }

        DrawScreen();
    }

    // ===================== DRAW THE 2D RESULT =====================

    void DrawScreen()
    {
        Color32 bg = new Color32(20, 20, 30, 255);
        for (int i = 0; i < pixels.Length; i++) pixels[i] = bg;

        Color32 border = new Color32(255, 255, 255, 255);
        for (int x = 0; x < W; x++) { Plot(x, 0, border); Plot(x, H - 1, border); }
        for (int y = 0; y < H; y++) { Plot(0, y, border); Plot(W - 1, y, border); }

        for (int e = 0; e < 12; e++)
        {
            int a = edges[e, 0], b = edges[e, 1];
            if (!visible[a] || !visible[b]) continue;     // vertex behind the camera
            Color32 col = e < 4 ? new Color32(255, 90, 90, 255)
                        : e < 8 ? new Color32(90, 255, 90, 255)
                                : new Color32(100, 150, 255, 255);
            Line(Mathf.RoundToInt(screen[a].x), Mathf.RoundToInt(screen[a].y),
                 Mathf.RoundToInt(screen[b].x), Mathf.RoundToInt(screen[b].y), col);
        }

        tex.SetPixels32(pixels);
        tex.Apply();
    }

    void Plot(int x, int y, Color32 c)
    {
        if (x < 0 || y < 0 || x >= W || y >= H) return;
        pixels[y * W + x] = c;
    }

    // Bresenham line (same algorithm as Experiment 1b)
    void Line(int x0, int y0, int x1, int y1, Color32 c)
    {
        x0 = Mathf.Clamp(x0, -2000, 2000); y0 = Mathf.Clamp(y0, -2000, 2000);
        x1 = Mathf.Clamp(x1, -2000, 2000); y1 = Mathf.Clamp(y1, -2000, 2000);
        int dx = Mathf.Abs(x1 - x0), dy = Mathf.Abs(y1 - y0);
        int sx = x0 < x1 ? 1 : -1, sy = y0 < y1 ? 1 : -1;
        int err = dx - dy, guard = 0;
        while (true)
        {
            Plot(x0, y0, c);
            if (x0 == x1 && y0 == y1) break;
            int e2 = 2 * err;
            if (e2 > -dy) { err -= dy; x0 += sx; }
            if (e2 < dx)  { err += dx; y0 += sy; }
            if (++guard > 6000) break;
        }
    }

    // ===================== ON-SCREEN TEXT =====================

    static string Mat(Matrix4x4 m)
    {
        StringBuilder sb = new StringBuilder();
        for (int r = 0; r < 4; r++)
        {
            for (int c = 0; c < 4; c++) sb.Append(m[r, c].ToString("0.00").PadLeft(8));
            sb.Append('\n');
        }
        return sb.ToString();
    }

    void OnGUI()
    {
        if (mono == null)
        {
            mono = new GUIStyle(GUI.skin.label);
            mono.font = Font.CreateDynamicFontFromOSFont(new[] { "Consolas", "Courier New" }, 13);
            mono.fontSize = 13;
            mono.normal.textColor = Color.white;
            mono.wordWrap = false;
            boxStyle = new GUIStyle(GUI.skin.box);
        }

        // ---- the computed 2D screen (viewport) ----
        float px = Screen.width - W - 20f;
        GUI.Box(new Rect(px - 6, 14, W + 12, H + 34), "", boxStyle);
        GUI.Label(new Rect(px, 16, W + 40, 22),
            "Computed 2D screen (viewport " + W + " x " + H + ")", mono);
        GUI.DrawTexture(new Rect(px, 38, W, H), tex);

        // ---- info panel ----
        StringBuilder sb = new StringBuilder();
        sb.Append(perspective ? "Projection: PERSPECTIVE  fov=" + fov.ToString("0") : "Projection: ORTHOGRAPHIC");
        sb.Append("   near=" + nearPlane.ToString("0.0") + " far=" + farPlane.ToString("0.0") + "\n");

        if (page == 0)
        {
            sb.Append("\nModel matrix M (cube TRS):\n" + Mat(M));
            sb.Append("\nView matrix V (look-at):\n" + Mat(V));
        }
        else if (page == 1)
        {
            sb.Append("\nProjection matrix P:\n" + Mat(P));
            sb.Append("\nCombined  P x V x M:\n" + Mat(PVM));
        }
        else
        {
            sb.Append("\nVtx  World              NDC               Screen px\n");
            for (int i = 0; i < 8; i++)
            {
                if (!visible[i]) { sb.Append("V" + (i + 1) + "   behind camera\n"); continue; }
                sb.Append("V" + (i + 1) + "  (" + F(world[i].x) + "," + F(world[i].y) + "," + F(world[i].z) + ")  ("
                          + F(ndc[i].x) + "," + F(ndc[i].y) + "," + F(ndc[i].z) + ")  ("
                          + screen[i].x.ToString("0").PadLeft(4) + "," + screen[i].y.ToString("0").PadLeft(4) + ")\n");
            }
        }

        float panelH = page == 2 ? 215f : 255f;
        GUI.Box(new Rect(10, 10, 520, panelH), "", boxStyle);
        GUI.Label(new Rect(18, 14, 510, panelH), sb.ToString(), mono);

        GUI.Label(new Rect(10, Screen.height - 46, Screen.width - 20, 44),
            "Arrows: orbit camera | Z/X: zoom | P: perspective/ortho | F/G: field of view | 1/2: near | 3/4: far | V: viewport size | R: spin cube | T: next page",
            mono);
    }

    static string F(float v) { return v.ToString("0.0").PadLeft(5); }
}
