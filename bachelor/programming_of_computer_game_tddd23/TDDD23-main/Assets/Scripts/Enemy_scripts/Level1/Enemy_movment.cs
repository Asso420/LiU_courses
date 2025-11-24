using System.Collections;
using UnityEngine;
using UnityEngine.AI;
using UnityEngine.UI;

public class EnemyMovement : MonoBehaviour
{
    public Transform target;  // Target player
    NavMeshAgent agent;
    private Animator enemy;
    //public int Zombie1_life_Init = 10;
    //private int Zombie1_life;

    private PlayerHealth playerHealth;
    public int playerDamageAmount = 10;

    private float timeBetweenAttacks = 5.0f;
    private float lastAttackTime = 0.0f;
    public float attackRange = 2f;
    public int zombieDamageAmount = 2;

    // Spawning variables
    public GameObject zombiePrefab;       // Reference to the prefab (self) for cloning
   // public Transform spawnPoint;          // Reference to a specific spawn point
   
   

    //Healthbar 
    public int zombieMaxHP =10;
    public int zombieCurrentHP;
    public Slider healthBar;

    void Start()
    {
        GameObject targetObject = GameObject.FindWithTag("Player");
        if (targetObject != null)
        {
            target = targetObject.transform;
            playerHealth = target.GetComponent<PlayerHealth>();
        }

        agent = GetComponent<NavMeshAgent>();
        enemy = GetComponent<Animator>();
        // Zombie1_life = Zombie1_life_Init;
        zombieCurrentHP = zombieMaxHP;

        // Start spawning zombies if enabled
        //if (enableZombieSpawning)
        //{
        //    StartCoroutine(SpawnZombieWithInterval());
        //}
    }

    void Update()
    {
        //zombieCurrentHP = zombieMaxHP;
        UpdateHealthUI();

        if (target == null) return; // Return if the player is not found

        float distance = Vector3.Distance(target.position, transform.position);

        if (distance <= attackRange)
        {
            agent.isStopped = true;
            enemy.SetBool("isInRange", true);

            if (Time.time >= lastAttackTime + timeBetweenAttacks)
            {
                damageToPlayer();
                lastAttackTime = Time.time;
            }
        }
        else
        {
            agent.isStopped = false;
            agent.SetDestination(target.position);
            enemy.SetBool("isInRange", false);
        }
    }

    public void damageToPlayer()
    {
        if (playerHealth != null)
        {
            playerHealth.TakeDamagePlayer(playerDamageAmount);
        }
    }

    public void TakeDamage(int zombieDamageAmount)
    {
        zombieCurrentHP -= zombieDamageAmount;

        Debug.Log("Enemy took damage! Remaining life: " + zombieCurrentHP);

        if (zombieCurrentHP <= 0)
        {
            Zombie1_IsDying();
        }
    }

    private void Zombie1_IsDying()
    {
        Debug.Log("Enemy died");
        Destroy(gameObject);
    }

    // Coroutine for spawning zombies
    //IEnumerator SpawnZombieWithInterval()
    //{
    //    yield return new WaitForSeconds(5f);  // Optional initial delay

    //    while (true)
    //    {
    //        // Use the specified spawn point's position and rotation
    //        if (spawnPoint != null)
    //        {
    //            GameObject newZombie = Instantiate(zombiePrefab, spawnPoint.position, spawnPoint.rotation);
    //            EnemyMovement newZombieMovement = newZombie.GetComponent<EnemyMovement>();

    //            if (newZombieMovement != null)
    //            {
    //                newZombieMovement.zombieCurrentHP = zombieMaxHP; // Reset health for the new zombie
    //            }
    //        }
    //        else
    //        {
    //            Debug.LogWarning("Spawn point is not set!");
    //        }

    //        yield return new WaitForSeconds(spawnInterval);
    //    }
    //}

    private void OnDrawGizmosSelected()
    {
        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(transform.position, attackRange);
    }

    private void UpdateHealthUI()
    {
        if (healthBar != null)
        {
            healthBar.value = zombieCurrentHP;
        }
    }
}
