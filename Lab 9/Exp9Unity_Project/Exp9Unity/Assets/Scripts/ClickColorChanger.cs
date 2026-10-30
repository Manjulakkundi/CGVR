using UnityEngine;

// Attach to ANY object (e.g. an empty "GameManager").
// Left-click on any 3D object with a Collider -> it gets a random color.
public class ClickColorChanger : MonoBehaviour
{
    void Update()
    {
        if (Input.GetMouseButtonDown(0))
        {
            Ray ray = Camera.main.ScreenPointToRay(Input.mousePosition);

            if (Physics.Raycast(ray, out RaycastHit hit))
            {
                Renderer rend = hit.collider.GetComponent<Renderer>();
                if (rend != null)
                {
                    rend.material.color = new Color(Random.value, Random.value, Random.value);
                }
            }
        }
    }
}
