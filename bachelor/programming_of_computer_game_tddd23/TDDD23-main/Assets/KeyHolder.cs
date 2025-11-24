using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class KeyHolder : MonoBehaviour
{
    public Transform key; // Reference to the key GameObject
    public float rotationSpeed = 45f; // Speed of rotation (degrees per second)

    // Update is called once per frame
    void Update()
    {
        // Rotate the key around its local Y-axis (you can change the axis if needed)
        key.Rotate(Vector3.up * rotationSpeed * Time.deltaTime);
    }

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            Debug.Log("Player has picked up the key!");
            PlayerController.hasKey = true; // Set the hasKey flag to true
            Destroy(gameObject); // Destroy the key object
        }
    }
}


