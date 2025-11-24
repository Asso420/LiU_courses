
using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.AI;
using static UnityEditor.ShaderGraph.Internal.KeywordDependentCollection;

public class EnemyMovementL2 : MonoBehaviour
{
    public float lookRadius = 20f;
    public float attackRange = 2f;
    private float timeBetweenAttacks = 5.0f;
    private float lastAttackTime = 0.0f;

    public int playerDamageAmount = 2;

    public Transform target;
    NavMeshAgent agent;
    private Animator enemy;
    private int Zombie1_life_Init = 4;
    private int Zombie1_life;
    public float zombieSpeed = 3f;
    private bool zombieHit = false;

    private PlayerHealth playerHealth;



    void Start()
    {
        GameObject targetObject = GameObject.FindWithTag("Player");
        if (targetObject != null)
        {
            target = targetObject.transform;
            playerHealth = target.GetComponent<PlayerHealth>();
        }

        agent = GetComponent<NavMeshAgent>();
        // enemy = GetComponent<Animator>();
        Zombie1_life = Zombie1_life_Init;
    }

    private void Awake()
    {
        enemy = transform.GetComponent<Animator>();
        if (enemy == null)
        {
            Debug.Log("enemy is not findebhcfjs:");
        }
    }

    void Update()
    {
        float distance = Vector3.Distance(target.position, transform.position);
        Zombie1_IsChasing(distance);
        Zombie1_IsAttacking(distance);

        

    }

    public void zombieIsIdle()
    {
        if (enemy != null) {
            enemy.SetBool("zombieStay", true);
            agent.speed = 0f;
        }
        zombieHit = true;
        StartCoroutine(ResetZombieStayAfterDelay(5f));
    }

    private IEnumerator ResetZombieStayAfterDelay(float delay)
    {
        yield return new WaitForSeconds(delay); // Wait for the specified delay (10 seconds)
        enemy.SetBool("zombieStay", false); // Reset the bool back to false
        zombieHit = false;
        agent.speed = zombieSpeed;
    }
    private void Zombie1_IsChasing(float distance)
    {
        if (distance <= lookRadius)
        {
            agent.SetDestination(target.position);
            enemy.SetBool("PlayerDetected", true);
            if(zombieHit)
            {
                agent.speed = 0f;
            }
            else
                agent.speed = zombieSpeed;

        }

        else
        {
            enemy.SetBool("PlayerDetected", false);
            agent.speed = 0f;
        }

    }
  

    private void Zombie1_IsAttacking(float distance)
    {
        if (distance <= attackRange)
        {
            agent.SetDestination(target.position);
            enemy.SetBool("Attacking", true);
            if (Time.time >= lastAttackTime + timeBetweenAttacks)
            {
                damageToPlayer();
                lastAttackTime = Time.time;
            }

        }
        else enemy.SetBool("Attacking", false);
    }

    public void damageToPlayer()
    {
        if (playerHealth != null)
        {
            playerHealth.TakeDamagePlayer(playerDamageAmount);
        }
    }
    private void OnDrawGizmosSelected()
    {
        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(transform.position, lookRadius);
        Gizmos.color = Color.black;
        Gizmos.DrawWireSphere(transform.position, attackRange);

    }

  

  
}