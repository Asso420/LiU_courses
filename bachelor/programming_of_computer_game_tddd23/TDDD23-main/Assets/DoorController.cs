using UnityEngine;
using TMPro;
using UnityEngine.SceneManagement;

public class DoorController : MonoBehaviour
{
    public float rotationAngle = 45f;  // The angle to rotate the door when opening
    public float rotationSpeed = 2f;   // The speed at which the door rotates
    public Transform doorTransform;    // The door's transform
    public TextMeshProUGUI messageText; // UI Text to display messages
    public string keyTag = "Key";      // Tag for the key object

    public static bool isPlayerNearby = false; // To track if the player is near the door
    public static bool isDoorOpen = false;     // To track if the door has already been opened
    private float initialRotation;             // Store the initial door rotation
    public ZombieManager zombieManager;

    private void Start()
    {
        // Save the door's initial rotation
        initialRotation = doorTransform.localEulerAngles.y;
    }

    private void OnTriggerEnter(Collider other)
    {
        int buildIndex = SceneManager.GetActiveScene().buildIndex;
        if (other.CompareTag("Player"))
        {
            isPlayerNearby = true;
            if (buildIndex == 1)
            {
                if (PlayerController.hasKey)
                {
                    //messageText.gameObject.SetActive(false);
                    OpenDoor();
                }
                else
                {
                    // Show message to the player to find the key
                    messageText.gameObject.SetActive(true);
                }
            }
            else if (buildIndex == 2)
            {
                if (zombieManager.GetZombieCount() <= 0)   // Check if the player has killed all the zombies
                {
                    //messageText.gameObject.SetActive(false);
                    OpenDoor();
                }
                else
                {
                    // Show message to the player to find the key
                    messageText.gameObject.SetActive(true);
                }
            }
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            isPlayerNearby = false;
            messageText.gameObject.SetActive(false);  // Hide message when player leaves

            // Close the door if the player leaves the area
            if (isDoorOpen)
            {
                CloseDoor();
            }
        }
    }

    private void OpenDoor()
    {
        if (!isDoorOpen)
        {
            StartCoroutine(RotateDoor(rotationAngle));  // Open door by the specified angle
            messageText.gameObject.SetActive(false);    // Hide the message
            isDoorOpen = true;
        }
    }

    private void CloseDoor()
    {
        if (isDoorOpen)
        {
            StartCoroutine(RotateDoor(initialRotation - doorTransform.localEulerAngles.y));  // Rotate back to the initial position
            isDoorOpen = false;
        }
    }

    private System.Collections.IEnumerator RotateDoor(float angle)
    {
        float targetRotation = doorTransform.localEulerAngles.y + angle;
        float currentRotation = doorTransform.localEulerAngles.y;

        while (Mathf.Abs(targetRotation - currentRotation) > 0.01f)
        {
            currentRotation = Mathf.Lerp(currentRotation, targetRotation, Time.deltaTime * rotationSpeed);
            doorTransform.localEulerAngles = new Vector3(doorTransform.localEulerAngles.x, currentRotation, doorTransform.localEulerAngles.z);
            yield return null;
        }
    }
}
