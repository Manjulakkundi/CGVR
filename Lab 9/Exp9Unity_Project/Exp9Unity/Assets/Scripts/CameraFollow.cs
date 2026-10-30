using UnityEngine;

// Attach to Main Camera. Drag the Player into the "Target" slot in the Inspector.
public class CameraFollow : MonoBehaviour
{
    public Transform target;                              // the player
    public Vector3 offset = new Vector3(0f, 6f, -8f);     // camera position relative to player
    public float smoothSpeed = 5f;

    void LateUpdate()
    {
        if (target == null) return;

        Vector3 desiredPosition = target.position + offset;
        transform.position = Vector3.Lerp(transform.position, desiredPosition, smoothSpeed * Time.deltaTime);
        transform.LookAt(target);
    }
}
