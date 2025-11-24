using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HealthBox : MonoBehaviour
{
    public Transform boneCap; // Assign the "Bone_cap" child object in the Inspector
    public float rotationSpeed = 50f; // Speed of rotation
    private bool playerInRange = false; // Track if the player is close
    [SerializeField] private int healthAmount = 30; // Amount of ammo in the box
    private bool healthGiven = false; // To track if ammo has already been given

    private Quaternion targetRotation; // Store the target rotation

    void Start()
    {
        // Initialize the target rotation to the current rotation of boneCap
        targetRotation = boneCap.localRotation;
    }

    void Update()
    {
        // If the player is within range and the ammo hasn't been given yet, rotate the cap
        if (playerInRange && !healthGiven)
        {
            RotateCap();
        }
    }

    void RotateCap()
    {
        // Rotate the cap by 45 degrees in the Z-axis
        targetRotation = Quaternion.Euler(boneCap.localEulerAngles.x, boneCap.localEulerAngles.y, -45f);

        // Smoothly rotate towards the target rotation
        boneCap.localRotation = Quaternion.RotateTowards(boneCap.localRotation, targetRotation, rotationSpeed * Time.deltaTime);

        // Check if the cap is fully open (i.e., reached the target rotation)
        if (Quaternion.Angle(boneCap.localRotation, targetRotation) < 0.1f && !healthGiven)
        {
            GiveHealthToPlayer();
        }
    }

    void GiveHealthToPlayer()
    {
        // Find the player's Health script and add health if it's not given yet

        GameObject player = GameObject.FindWithTag("Player");
        if (player != null)
        {
            PlayerHealth playerHealth = player.GetComponent<PlayerHealth>();
            if (playerHealth != null)
            {
                playerHealth.AddHealth(healthAmount);
                healthGiven = true; // Ensure ammo is given only once
                Debug.Log("Given given to player: " + healthAmount);
            }
        }
    }

    // Detect when the player enters the trigger zone
    private void OnTriggerEnter(Collider other)
    {
        // Only set playerInRange if ammo hasn't been given yet
        if (other.CompareTag("Player") && !healthGiven)
        {
            playerInRange = true;
            Debug.Log("Player is in range");
        }
    }

    public bool IsEmpty()
    {
        return healthGiven;
    }
    // Detect when the player leaves the trigger zone
    private void OnTriggerExit(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            playerInRange = false;
        }
    }
}
