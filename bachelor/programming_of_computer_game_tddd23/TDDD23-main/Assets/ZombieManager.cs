using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;

public class ZombieManager : MonoBehaviour
{
    // Start is called before the first frame update
    private List<ZombHealth> healthList;
    public TextMeshProUGUI zombieCountText;
    void Start()
    {
        healthList = new List<ZombHealth>();
        foreach (Transform child in transform)
        {
            ZombHealth healthScript = child.GetComponent<ZombHealth>();
            if (healthScript != null)
            {
                healthList.Add(healthScript);
                healthScript.zombieManager = this;
            }
        }
        UpdateZombieCountUI();

    }

    // Update is called once per frame
    void Update()
    {
        
    }
    void UpdateZombieCountUI()
    {
        zombieCountText.text = "Zombies Remaining: " + healthList.Count;
    }
    public void RemoveZombie(ZombHealth health)
    {
        if (healthList.Contains(health))
        {
            healthList.Remove(health);
            UpdateZombieCountUI();
        }
    }
    public int GetZombieCount()
    {
        return healthList.Count;
    }
}
