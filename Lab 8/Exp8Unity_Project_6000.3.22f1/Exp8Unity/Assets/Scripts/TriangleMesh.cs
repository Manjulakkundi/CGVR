using UnityEngine;

// Builds a single triangle (like the OpenGL triangle in the Python version)
// with a different color at each vertex: red, green, blue.
[ExecuteAlways]
[RequireComponent(typeof(MeshFilter), typeof(MeshRenderer))]
public class TriangleMesh : MonoBehaviour
{
    void OnEnable()
    {
        MeshFilter mf = GetComponent<MeshFilter>();
        if (mf.sharedMesh != null) return;

        Mesh mesh = new Mesh();
        mesh.name = "Triangle";
        mesh.vertices = new Vector3[]
        {
            new Vector3(-0.5f, -0.5f, 0f),   // bottom left
            new Vector3( 0.5f, -0.5f, 0f),   // bottom right
            new Vector3( 0.0f,  0.5f, 0f)    // top
        };
        mesh.colors = new Color[] { Color.red, Color.green, Color.blue };
        mesh.triangles = new int[] { 0, 1, 2 };
        mesh.RecalculateBounds();
        mf.sharedMesh = mesh;
    }
}
