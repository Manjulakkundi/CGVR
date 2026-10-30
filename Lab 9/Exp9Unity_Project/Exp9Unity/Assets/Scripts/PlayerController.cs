using UnityEngine;

// Attach to the Player (Sphere). Needs a Rigidbody + Collider on the same object.
// Move: W A S D / Arrow keys     Jump: Space
[RequireComponent(typeof(Rigidbody))]
public class PlayerController : MonoBehaviour
{
    public float moveForce = 12f;      // how strongly the ball is pushed
    public float jumpForce = 6f;       // upward impulse when jumping

    private Rigidbody rb;
    private bool isGrounded;
    private int score = 0;

    void Start()
    {
        rb = GetComponent<Rigidbody>();
    }

    void Update()
    {
        // Jump (only when touching the ground)
        if (Input.GetKeyDown(KeyCode.Space) && isGrounded)
        {
            rb.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);
        }
    }

    void FixedUpdate()
    {
        float h = Input.GetAxis("Horizontal");   // A / D
        float v = Input.GetAxis("Vertical");     // W / S

        Vector3 movement = new Vector3(h, 0f, v);
        rb.AddForce(movement * moveForce);
    }

    // ---- Ground check ----
    void OnCollisionStay(Collision collision)
    {
        if (collision.gameObject.CompareTag("Ground"))
            isGrounded = true;
    }

    void OnCollisionExit(Collision collision)
    {
        if (collision.gameObject.CompareTag("Ground"))
            isGrounded = false;
    }

    // ---- Collect pickups (objects tagged "Pickup" with "Is Trigger" ticked) ----
    void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Pickup"))
        {
            other.gameObject.SetActive(false);   // make the pickup disappear
            score++;
        }
    }

    // Simple on-screen score (no UI setup needed)
    void OnGUI()
    {
        GUIStyle style = new GUIStyle(GUI.skin.label);
        style.fontSize = 28;
        style.normal.textColor = Color.white;
        GUI.Label(new Rect(20, 20, 400, 50), "Score: " + score, style);
    }
}
