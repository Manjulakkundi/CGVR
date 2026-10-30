#if UNITY_EDITOR
using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

// Menu:  Lab > Build Experiment 8 Scene
public static class Exp8SceneBuilder
{
    public const string ScenePath = "Assets/Scenes/Exp8Scene.unity";

    [MenuItem("Lab/Build Experiment 8 Scene")]
    public static void Build()
    {
        EnsureFolder("Assets/Materials");
        EnsureFolder("Assets/Scenes");

        Shader shader = Shader.Find("Lab/Exp8_VertexFragment");
        if (shader == null)
        {
            Debug.LogError("Shader 'Lab/Exp8_VertexFragment' not found. Check the Console for shader compile errors, then use Lab > Build Experiment 8 Scene again.");
            return;
        }

        var scene = EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects, NewSceneMode.Single);

        Material mat = new Material(shader);
        string matPath = "Assets/Materials/Exp8Mat.mat";
        AssetDatabase.DeleteAsset(matPath);
        AssetDatabase.CreateAsset(mat, matPath);

        GameObject tri = new GameObject("Triangle");
        tri.AddComponent<MeshFilter>();
        MeshRenderer mr = tri.AddComponent<MeshRenderer>();
        mr.sharedMaterial = mat;
        tri.AddComponent<TriangleMesh>();
        tri.AddComponent<ShaderController>();

        Camera cam = Camera.main;
        if (cam != null)
        {
            cam.transform.position = new Vector3(0f, 0f, -3f);
            cam.transform.rotation = Quaternion.identity;
            cam.clearFlags = CameraClearFlags.SolidColor;
            cam.backgroundColor = new Color(0.1f, 0.1f, 0.15f);
        }

        EditorSceneManager.SaveScene(scene, ScenePath);
        AssetDatabase.SaveAssets();
        Debug.Log("Experiment 8 scene built. Press Play!");
    }

    static void EnsureFolder(string path)
    {
        if (!AssetDatabase.IsValidFolder(path))
            AssetDatabase.CreateFolder(Path.GetDirectoryName(path).Replace("\\", "/"), Path.GetFileName(path));
    }
}

// Builds (first time) or opens (later) the scene automatically when the project is opened.
[InitializeOnLoad]
public static class AutoOpenExp8
{
    static AutoOpenExp8()
    {
        if (SessionState.GetBool("Exp8AutoDone", false)) return;
        SessionState.SetBool("Exp8AutoDone", true);
        EditorApplication.delayCall += Run;
    }

    static void Run()
    {
        if (EditorApplication.isPlayingOrWillChangePlaymode) return;
        if (File.Exists(Exp8SceneBuilder.ScenePath))
            EditorSceneManager.OpenScene(Exp8SceneBuilder.ScenePath);
        else
            Exp8SceneBuilder.Build();
    }
}
#endif
