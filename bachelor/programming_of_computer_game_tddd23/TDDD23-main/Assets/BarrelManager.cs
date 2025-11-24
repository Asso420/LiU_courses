using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.Rendering;

public class BarrelManager : MonoBehaviour
{
    public GameObject keyPrefab;// Reference to the key GameObject
    private List<NewBehaviourScript> barrels; // List to store all the barrels (boxes)
    public float keyYOffset = 0.5f;
    private GameObject keyInstance;
    public TextMeshProUGUI barrelCountText;

    // Start is called before the first frame update
    void Start()
    {
        // Initialize the list and get all the barrels (child objects with NewBehaviourScript attached)
        barrels = new List<NewBehaviourScript>();
        foreach (Transform child in transform)
        {
            NewBehaviourScript barrelScript = child.GetComponent<NewBehaviourScript>();
            if (barrelScript != null)
            {
                barrels.Add(barrelScript);
                barrelScript.barrelManager = this; // Assign the reference to each barrel
            }
        }

        // Randomly pick one barrel to contain the key
        AssignKeyToRandomBarrel();
        UpdateBarrelCountUI();
    }

    // Function to assign the key to a random barrel
    void AssignKeyToRandomBarrel()
    {
        if (barrels.Count > 0)
        {
            int randomIndex = Random.Range(0, barrels.Count);
            barrels[randomIndex].containsKey = true; // Set the selected barrel to contain the key
            keyInstance = Instantiate(keyPrefab);
            Vector3 barrelPosition = barrels[randomIndex].transform.position;
            keyInstance.transform.position = new Vector3(barrelPosition.x, barrelPosition.y + keyYOffset, barrelPosition.z);
            // Adjust the key's position with a Y-axis offset

            Debug.Log("Key placed in barrel: " + barrels[randomIndex].gameObject.name);
        }
        else
        {
            Debug.LogWarning("No barrels found to place the key!");
        }
    }
    void UpdateBarrelCountUI()
    {
        barrelCountText.text = "Boxes Remaining: " + barrels.Count;
    }
    public void RemoveBarrel(NewBehaviourScript barrel)
    {
        if (barrels.Contains(barrel))
        {
            barrels.Remove(barrel);
            Debug.Log("Barrel removed: " + barrel.gameObject.name);

            // Display the updated number of barrels left
            Debug.Log("Barrels remaining: " + barrels.Count);
            barrelCountText.text = "Barrels Remaining: " + barrels.Count;
        }
    }

}

