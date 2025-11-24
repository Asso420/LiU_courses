using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AmmoBoxManager : MonoBehaviour
{
    public GameObject ammoBoxPrefab; // Assign the AmmoBox prefab in the Inspector
    public float respawnTime = 10f; // Respawn time in seconds (3 minutes)

    private List<AmmoBox> ammoBoxes; // List to store all ammo boxes

    void Start()
    {
        // Initialize the list and find all AmmoBox components in the children
        ammoBoxes = new List<AmmoBox>(GetComponentsInChildren<AmmoBox>());

        // Start the respawn coroutine
        StartCoroutine(CheckAndRespawnAmmoBoxes());
    }

    // Coroutine that runs every few seconds to check and respawn empty ammo boxes
    IEnumerator CheckAndRespawnAmmoBoxes()
    {
        while (true)
        {
            yield return new WaitForSeconds(respawnTime);

            // Iterate through each AmmoBox and check if it has given ammo
            List<AmmoBox> emptyBoxes = new List<AmmoBox>();

            foreach (AmmoBox ammoBox in ammoBoxes)
            {
                if (ammoBox == null || ammoBox.IsEmpty()) // Check if ammo box is empty or destroyed
                {
                    emptyBoxes.Add(ammoBox); // Add to empty boxes list
                }
            }

            // Randomly pick an empty box and respawn
            if (emptyBoxes.Count > 0)
            {
                int randomIndex = Random.Range(0, emptyBoxes.Count);
                AmmoBox emptyHealthBox = emptyBoxes[randomIndex];
                ammoBoxes.Remove(emptyHealthBox); // Remove the empty box from the list
                RespawnAmmoBox(emptyBoxes[randomIndex]);
            }
        }
    }

    // Function to respawn a new ammo box at the position of the empty one
    void RespawnAmmoBox(AmmoBox emptyAmmoBox)
    {
        if (emptyAmmoBox != null)
        {
            Vector3 spawnPosition = emptyAmmoBox.transform.position;
            Quaternion spawnRotation = emptyAmmoBox.transform.rotation;

            // Destroy the old ammo box
            Destroy(emptyAmmoBox.gameObject);

            // Instantiate a new ammo box at the same position
            GameObject newAmmoBox = Instantiate(ammoBoxPrefab, spawnPosition, spawnRotation);
            newAmmoBox.transform.parent = this.transform; // Set it as a child of ammoBoxes
            ammoBoxes.Add(newAmmoBox.GetComponent<AmmoBox>()); // Add the new ammo box to the list
        }
    }
}
