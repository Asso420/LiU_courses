using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AmmoBox : MonoBehaviour
{
    public Transform boneCap; // Assign the "Bone_cap" child object in the Inspector
    public float rotationSpeed = 50f; // Speed of rotation
    private bool playerInRange = false; // Track if the player is close
    [SerializeField] private int ammoCount = 30; // Amount of ammo in the box
    private bool ammoGiven = false; // To track if ammo has already been given

    private Quaternion targetRotation; // Store the target rotation

    void Start()
    {
        // Initialize the target rotation to the current rotation of boneCap
        targetRotation = boneCap.localRotation;
    }

    void Update()
    {
        // If the player is within range and the ammo hasn't been given yet, rotate the cap
        if (playerInRange && !ammoGiven)
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
        if (Quaternion.Angle(boneCap.localRotation, targetRotation) < 0.1f && !ammoGiven)
        {
            GiveAmmoToPlayer();
        }
    }

    void GiveAmmoToPlayer()
    {
        // Find the player's SwitchWeapon script and add ammo if it's not given yet
        GameObject player = GameObject.FindWithTag("Player");
        if (player != null)
        {
            SwitchWeapon switchWeapon = player.GetComponent<SwitchWeapon>();
            if (switchWeapon != null)
            {
                switchWeapon.AddAmmo(ammoCount);
                ammoGiven = true; // Ensure ammo is given only once
                Debug.Log("Ammo given to player: " + ammoCount);
            }
        }
    }

    // Detect when the player enters the trigger zone
    private void OnTriggerEnter(Collider other)
    {
        // Only set playerInRange if ammo hasn't been given yet
        if (other.CompareTag("Player") && !ammoGiven)
        {
            playerInRange = true;
            Debug.Log("Player is in range");
        }
    }
    public bool IsEmpty()
    {
        return ammoGiven;
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
