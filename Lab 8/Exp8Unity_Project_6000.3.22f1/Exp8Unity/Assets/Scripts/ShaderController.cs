using UnityEngine;

// Sends values from C# (CPU) to the shader (GPU) every frame.
// Q / E : rotate        Arrow keys : translate        Z / X : scale        Space : animation on/off
public class ShaderController : MonoBehaviour
{
    public float angle = 0f;
    public float scale = 1f;
    public Vector2 translate = Vector2.zero;
    public bool animate = true;

    Material mat;

    void Start()
    {
        mat = GetComponent<MeshRenderer>().material;
    }

    void Update()
    {
        float dt = Time.deltaTime;

        if (Input.GetKey(KeyCode.Q)) angle += 90f * dt;
        if (Input.GetKey(KeyCode.E)) angle -= 90f * dt;
        if (Input.GetKey(KeyCode.Z)) scale += 0.8f * dt;
        if (Input.GetKey(KeyCode.X)) scale -= 0.8f * dt;
        scale = Mathf.Clamp(scale, 0.2f, 3f);

        if (Input.GetKey(KeyCode.RightArrow)) translate.x += 1.0f * dt;
        if (Input.GetKey(KeyCode.LeftArrow))  translate.x -= 1.0f * dt;
        if (Input.GetKey(KeyCode.UpArrow))    translate.y += 1.0f * dt;
        if (Input.GetKey(KeyCode.DownArrow))  translate.y -= 1.0f * dt;

        if (Input.GetKeyDown(KeyCode.Space)) animate = !animate;

        mat.SetFloat("_Angle", angle);
        mat.SetFloat("_Scale", scale);
        mat.SetVector("_Translate", new Vector4(translate.x, translate.y, 0f, 0f));
        mat.SetFloat("_Animate", animate ? 1f : 0f);
    }

    void OnGUI()
    {
        GUIStyle style = new GUIStyle(GUI.skin.label) { fontSize = 18 };
        style.normal.textColor = Color.white;
        GUI.Label(new Rect(15, 10, 900, 30), "Q/E rotate | Arrows translate | Z/X scale | Space animate on/off", style);
        GUI.Label(new Rect(15, 40, 900, 30),
            "angle = " + angle.ToString("F0") + "   scale = " + scale.ToString("F2") +
            "   translate = (" + translate.x.ToString("F2") + ", " + translate.y.ToString("F2") + ")", style);
    }
}
