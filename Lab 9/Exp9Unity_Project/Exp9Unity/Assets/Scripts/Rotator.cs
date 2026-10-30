using UnityEngine;

// Attach to Pickup objects (cubes). Makes them spin continuously.
public class Rotator : MonoBehaviour
{
    public Vector3 rotationSpeed = new Vector3(15f, 30f, 45f);   // degrees per second

    void Update()
    {
        transform.Rotate(rotationSpeed * Time.deltaTime);
    }
}
