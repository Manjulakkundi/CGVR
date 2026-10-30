#if UNITY_EDITOR
using UnityEngine;
using UnityEditor;
using UnityEditor.SceneManagement;

// Put this file in:  Assets/Editor/SceneBuilder.cs
// Then in Unity click the top menu:  Lab > Build Experiment 9 Scene
// It creates the ground, player, pickups, camera, light and attaches all scripts automatically.
public static class SceneBuilder
{
    [MenuItem("Lab/Build Experiment 9 Scene")]
    public static void Build()
    {
        EnsureTag("Ground");
        EnsureTag("Pickup");
        EnsureFolder("Assets/Materials");
        EnsureFolder("Assets/Scenes");

        // Fresh scene that already has a Main Camera and a Directional Light
        var scene = EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects, NewSceneMode.Single);

        // ---------------- Ground ----------------
        GameObject ground = GameObject.CreatePrimitive(PrimitiveType.Plane);
        ground.name = "Ground";
        ground.tag = "Ground";
        ground.transform.localScale = new Vector3(2f, 1f, 2f);          // 20 x 20 units
        Paint(ground, "GroundMat", new Color(0.35f, 0.65f, 0.35f));

        // ---------------- Player ----------------
        GameObject player = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        player.name = "Player";
        player.transform.position = new Vector3(0f, 1f, 0f);
        player.AddComponent<Rigidbody>();
        player.AddComponent<PlayerController>();
        Paint(player, "PlayerMat", new Color(0.15f, 0.35f, 0.95f));

        // ---------------- Pickups (ring of 8 spinning cubes) ----------------
        GameObject pickupParent = new GameObject("Pickups");
        int count = 8;
        float radius = 6f;
        for (int i = 0; i < count; i++)
        {
            float angle = i * Mathf.PI * 2f / count;
            GameObject pickup = GameObject.CreatePrimitive(PrimitiveType.Cube);
            pickup.name = "Pickup_" + (i + 1);
            pickup.tag = "Pickup";
            pickup.transform.SetParent(pickupParent.transform);
            pickup.transform.position = new Vector3(Mathf.Cos(angle) * radius, 0.8f, Mathf.Sin(angle) * radius);
            pickup.transform.localScale = new Vector3(0.7f, 0.7f, 0.7f);
            pickup.GetComponent<BoxCollider>().isTrigger = true;
            pickup.AddComponent<Rotator>();
            Paint(pickup, "PickupMat", new Color(1f, 0.85f, 0.1f));
        }

        // ---------------- Camera ----------------
        Camera cam = Camera.main;
        if (cam != null)
        {
            cam.transform.position = new Vector3(0f, 7f, -8f);
            CameraFollow follow = cam.gameObject.AddComponent<CameraFollow>();
            follow.target = player.transform;
        }

        // ---------------- Click-to-recolor manager ----------------
        GameObject manager = new GameObject("GameManager");
        manager.AddComponent<ClickColorChanger>();

        // ---------------- Save the scene ----------------
        string path = "Assets/Scenes/Exp9Scene.unity";
        EditorSceneManager.SaveScene(scene, path);
        AssetDatabase.SaveAssets();

        Debug.Log("Experiment 9 scene built and saved at " + path + ". Press Play!");
    }

    // ---------- helpers ----------

    static void Paint(GameObject go, string matName, Color color)
    {
        Renderer r = go.GetComponent<Renderer>();
        // Copy the default material so it works in Built-in, URP and HDRP projects
        Material mat = new Material(r.sharedMaterial);
        mat.color = color;
        string matPath = "Assets/Materials/" + matName + ".mat";
        AssetDatabase.DeleteAsset(matPath);                 // overwrite if it already exists
        AssetDatabase.CreateAsset(mat, matPath);
        r.sharedMaterial = mat;
    }

    static void EnsureFolder(string path)
    {
        if (!AssetDatabase.IsValidFolder(path))
        {
            string parent = System.IO.Path.GetDirectoryName(path).Replace("\\", "/");
            string name = System.IO.Path.GetFileName(path);
            AssetDatabase.CreateFolder(parent, name);
        }
    }

    static void EnsureTag(string tag)
    {
        SerializedObject tagManager = new SerializedObject(
            AssetDatabase.LoadAllAssetsAtPath("ProjectSettings/TagManager.asset")[0]);
        SerializedProperty tags = tagManager.FindProperty("tags");

        for (int i = 0; i < tags.arraySize; i++)
            if (tags.GetArrayElementAtIndex(i).stringValue == tag) return;

        tags.InsertArrayElementAtIndex(tags.arraySize);
        tags.GetArrayElementAtIndex(tags.arraySize - 1).stringValue = tag;
        tagManager.ApplyModifiedProperties();
    }
}
#endif
