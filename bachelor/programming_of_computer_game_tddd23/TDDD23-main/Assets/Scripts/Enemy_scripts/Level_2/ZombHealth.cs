using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.AI;
using UnityEngine.UI;

public class ZombHealth : MonoBehaviour
{
    public float maxHealth = 12f;
    private Animator enemy;
    [HideInInspector]

    private Ragdoll ragdoll;  // Reference to the ragdoll system
    public float zombieCurrentHP;
    public Slider healthBar;
    public ZombieManager zombieManager;
    NavMeshAgent agent;

    void Start()
    {
        zombieCurrentHP = maxHealth;
        ragdoll = GetComponent<Ragdoll>();

        // Ensure the ragdoll script is attached
        if (ragdoll == null)
        {
            Debug.LogError("Ragdoll script is missing on the zombie!");
        }
        agent = GetComponent<NavMeshAgent>();
    }

    private void Awake()
    {
        enemy = transform.GetComponent<Animator>();
        if (enemy == null)
        {
            Debug.Log("enemy is not findebhcfjs:");
        }
    }
    private void Update()
    {
        UpdateHealthUI();
    }

    public void TakeDamage(float damageAmount)
    {
        zombieCurrentHP -= damageAmount;
        
        Debug.Log("Zombie took {damageAmount} damage, current health: {zombieCurrentHP}");
        if (zombieCurrentHP <= 0)
        {
            zombieCurrentHP = 0;
            agent.speed = 0;
            agent.isStopped = true;
            enemy.SetBool("zombieDying", true);
            Die();
        }
    }

    public void Die()
    {
        Debug.Log("Zombie died!");

        if (ragdoll != null)
        {
            ragdoll.ActivateRagdoll();  // Activate the ragdoll on death
        }
        else
        {
            Debug.LogWarning("Ragdoll component is missing on the zombie.");
        }
        if(zombieManager != null)
        { 
            zombieManager.RemoveZombie(this);
       }    
        Destroy(gameObject, 2f);

    }

    private void UpdateHealthUI()
    {
        if (healthBar != null)
        {
            healthBar.value = zombieCurrentHP;
        }
    }
}
