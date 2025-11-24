using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NewBehaviourScript : MonoBehaviour
{
    public GameObject Destroyed;
    [SerializeField] private float health = 4f;
    public bool containsKey = false;
    private bool isDestroyed = false;  // New flag to prevent multiple destruction

    // Reference to the BarrelManager
    public BarrelManager barrelManager;

    // Method to apply damage to the barrel
    public void TakeDamage()
    {
        if (isDestroyed) return;  // Prevent taking damage after being destroyed

        health--;
        Debug.Log("Barrel health: " + health);
        if (health <= 0)
        {
            DestroyBarrel();
        }
    }

    // Method to destroy the barrel
    public void DestroyBarrel()
    {
        if (isDestroyed) return;  // Prevent multiple instantiations
        isDestroyed = true;  // Set the flag to prevent future destruction

        // Instantiate the destroyed barrel object
        Instantiate(Destroyed, transform.position, transform.rotation);
        Debug.Log("Barrel is destroyed");

        // Check if this barrel contains the key
        if (containsKey)
        {
            Debug.Log("The key is found");
            // Additional logic to handle the key can be added here
        }

        // Notify the BarrelManager to remove this barrel from the list
        if (barrelManager != null)
        {
            barrelManager.RemoveBarrel(this);
        }

        // Finally, destroy the barrel game object
        Destroy(gameObject);
    }
}
