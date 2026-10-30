#if UNITY_EDITOR
using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

// Menu:  Lab > Build Experiment 10 Scene
public static class Exp10SceneBuilder
{
    public const string ScenePath = "Assets/Scenes/Exp10Scene.unity";

    [MenuItem("Lab/Build Experiment 10 Scene")]
    public static void Build()
    {
        EnsureFolder("Assets/Materials");
        EnsureFolder("Assets/Scenes");

        var scene = EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects, NewSceneMode.Single);

        // the 3D object (unit cube scaled to 2)
        GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
        cube.name = "Cube";
        cube.transform.position = Vector3.zero;
        cube.transform.localScale = new Vector3(2f, 2f, 2f);
        Renderer r = cube.GetComponent<Renderer>();
        Material mat = new Material(r.sharedMaterial);
        mat.color = new Color(0.25f, 0.55f, 0.95f);
        string matPath = "Assets/Materials/Exp10CubeMat.mat";
        AssetDatabase.DeleteAsset(matPath);
        AssetDatabase.CreateAsset(mat, matPath);
        r.sharedMaterial = mat;

        Camera cam = Camera.main;
        if (cam != null)
        {
            cam.clearFlags = CameraClearFlags.SolidColor;
            cam.backgroundColor = new Color(0.12f, 0.12f, 0.18f);
        }

        GameObject pipeline = new GameObject("ViewingPipeline");
        ViewingPipeline vp = pipeline.AddComponent<ViewingPipeline>();
        vp.cube = cube.transform;
        vp.cam = cam;

        EditorSceneManager.SaveScene(scene, ScenePath);
        AssetDatabase.SaveAssets();
        Debug.Log("Experiment 10 scene built. Press Play!");
    }

    static void EnsureFolder(string path)
    {
        if (!AssetDatabase.IsValidFolder(path))
            AssetDatabase.CreateFolder(Path.GetDirectoryName(path).Replace("\\", "/"), Path.GetFileName(path));
    }
}

// Builds (first time) or opens (later) the scene automatically when the project is opened.
[InitializeOnLoad]
public static class AutoOpenExp10
{
    static AutoOpenExp10()
    {
        if (SessionState.GetBool("Exp10AutoDone", false)) return;
        SessionState.SetBool("Exp10AutoDone", true);
        EditorApplication.delayCall += Run;
    }

    static void Run()
    {
        if (EditorApplication.isPlayingOrWillChangePlaymode) return;
        if (File.Exists(Exp10SceneBuilder.ScenePath))
            EditorSceneManager.OpenScene(Exp10SceneBuilder.ScenePath);
        else
            Exp10SceneBuilder.Build();
    }
}
#endif
