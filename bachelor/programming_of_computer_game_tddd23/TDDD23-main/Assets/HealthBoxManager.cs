using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HealthBoxManager : MonoBehaviour
{
    public GameObject healthBoxPrefab; // Assign the HealthBox prefab in the Inspector
    public float respawnTime = 10f; // Respawn time in seconds

    private List<HealthBox> healthBoxes; // List to store all health boxes

    void Start()
    {
        // Initialize the list and find all HealthBox components in the children
        healthBoxes = new List<HealthBox>(GetComponentsInChildren<HealthBox>());

        // Start the respawn coroutine
        StartCoroutine(CheckAndRespawnHealthBoxes());
    }

    // Coroutine that runs every few seconds to check and respawn empty health boxes
    IEnumerator CheckAndRespawnHealthBoxes()
    {
        while (true)
        {
            yield return new WaitForSeconds(respawnTime);

            // Create a list to track empty health boxes
            List<HealthBox> emptyBoxes = new List<HealthBox>();

            // Iterate through each HealthBox and check if it has been used (is empty)
            foreach (HealthBox healthBox in healthBoxes)
            {
                if (healthBox == null || healthBox.IsEmpty()) // Check if the health box is empty or destroyed
                {
                    emptyBoxes.Add(healthBox); // Add to the empty boxes list
                }
            }

            // Randomly pick an empty box and respawn
            if (emptyBoxes.Count > 0)
            {
                int randomIndex = Random.Range(0, emptyBoxes.Count);
                HealthBox emptyHealthBox = emptyBoxes[randomIndex];
                Debug.Log("Respawning health box at: " + emptyBoxes[randomIndex]);

                // Remove the empty box from the list
                healthBoxes.Remove(emptyHealthBox);
                RespawnHealthBox(emptyHealthBox); // Use the emptyHealthBox variable instead
            }
        }
    }

    // Function to respawn a new health box at the position of the empty one
    void RespawnHealthBox(HealthBox emptyHealthBox)
    {
        if (emptyHealthBox != null)
        {
            Vector3 spawnPosition = emptyHealthBox.transform.position;
            Quaternion spawnRotation = emptyHealthBox.transform.rotation;

            // Destroy the old health box
            Destroy(emptyHealthBox.gameObject);

            // Instantiate a new health box at the same position
            GameObject newHealthBox = Instantiate(healthBoxPrefab, spawnPosition, spawnRotation);
            newHealthBox.transform.parent = this.transform; // Set it as a child of the HealthBoxManager

            // Add the new health box to the list
            healthBoxes.Add(newHealthBox.GetComponent<HealthBox>());
        }
    }
}
