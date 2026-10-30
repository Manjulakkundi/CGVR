#if UNITY_EDITOR
using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;

// Runs once each time the project is opened:
//  - first time: builds the Experiment 9 scene automatically
//  - later:      just opens the saved scene
// So you only need to open the project and press Play.
[InitializeOnLoad]
public static class AutoOpenExp9
{
    const string ScenePath = "Assets/Scenes/Exp9Scene.unity";

    static AutoOpenExp9()
    {
        if (SessionState.GetBool("Exp9AutoDone", false)) return;
        SessionState.SetBool("Exp9AutoDone", true);
        EditorApplication.delayCall += Run;
    }

    static void Run()
    {
        if (EditorApplication.isPlayingOrWillChangePlaymode) return;

        if (File.Exists(ScenePath))
            EditorSceneManager.OpenScene(ScenePath);
        else
            SceneBuilder.Build();
    }
}
#endif
