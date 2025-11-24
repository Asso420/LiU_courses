using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI; // For health bar UI (if any)

public class PlayerHealth : MonoBehaviour
{
    public int maxHealth = 10; // Maximum health of the player
    private int currentHealth;  // Current health of the player
    public static bool isDead = false;

    public Slider healthBar; // Optional: Link to a health bar UI in the Inspector

    // Start is called before the first frame update
    void Start()
    {
        currentHealth = maxHealth; // Initialize player's health
        UpdateHealth();
        UpdateHealthUI(); // Update UI at the start if a health bar is used
    }
    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.K))
        {
            TakeDamagePlayer(10); // Simulate taking damage when pressing Space
        }
    }
    
    private void UpdateHealth()
    {
        if (currentHealth >= 0) return;
        Die();
    }
    // This method adds health to the player, called by the HealthBox script
    public void AddHealth(int healthAmount)
    {
        currentHealth += healthAmount; // Add health
        if (currentHealth > maxHealth)
        {
            currentHealth = maxHealth; // Ensure health doesn't exceed max health
        }

        UpdateHealthUI(); // Update the health bar (if applicable)
        Debug.Log("Player health increased. Current health: " + currentHealth);
    }

    // This method can be called to reduce health (e.g., from enemy attacks)
    public void TakeDamagePlayer(int damageAmount)
    {
        
        currentHealth -= damageAmount; // Subtract damage from health
        Debug.Log("Plyer current life is: " + currentHealth);
        Debug.Log("Player bitten");

        if (currentHealth <= 0)
        {
            currentHealth = 0;
            Die(); // Call the Die function if health reaches 0
        }

        UpdateHealthUI(); // Update the health bar (if applicable)
        Debug.Log("Player took damage. Current health: " + currentHealth);
    }
    public void SetHealth()
    {
        currentHealth = maxHealth;
        isDead = false;
        UpdateHealthUI();
    }
    // Handle player death (to be expanded based on your game's needs)
    private void Die()
    {
        Debug.Log("Player has died!");

        isDead = true;
        
        // Handle death logic (e.g., respawn, game over screen)
    }

    // Update health bar UI (if linked in Inspector)
    private void UpdateHealthUI()
    {
        if (healthBar != null)
        {
            healthBar.value = currentHealth;
        }
    }
}
