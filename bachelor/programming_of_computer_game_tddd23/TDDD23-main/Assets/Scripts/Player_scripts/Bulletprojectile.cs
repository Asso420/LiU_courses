using UnityEditor.Experimental.GraphView;
using UnityEngine;
using UnityEngine.AI;
using UnityEngine.SceneManagement;

public class BulletProjectile : MonoBehaviour
{
    public float bulletSpeed = 50f;
    public int zombieDamageAmount = 2;
    private Rigidbody rb;
    public GameObject tracerPrefab;
    private GameObject tracerInstance;
    public GunController gunController;

    // [SerializeField] GameObject hitVFX;

    private void Awake()
    {
        rb = GetComponent<Rigidbody>();
    }

    private void Start()
    {
        rb.velocity = transform.forward * bulletSpeed;

        tracerInstance = Instantiate(tracerPrefab, transform.position, Quaternion.identity);
        tracerInstance.transform.SetParent(transform);
        

    }

    private void OnTriggerEnter(Collider other)
    {
       
        int buildIndex = SceneManager.GetActiveScene().buildIndex;

        Debug.Log($"Bullet hit something: {other.name}");

        switch (buildIndex)
        {
            case 1:
                HandleLevel1Collision(other);
                break;
            case 2:
                HandleLevel2Collision(other);
                break;
            default:
                Debug.LogWarning("Unhandled build index: " + buildIndex);
                break;
        }

        Destroy(gameObject); // Destroy the bullet on impact
    }

    private void HandleLevel1Collision(Collider other)
    {
        if (other.CompareTag("Zombielvl1"))
        {
            ApplyDamageToZombie(other);
            gunController.HitEffectBlood();
        }
        else if (other.CompareTag("Barrels"))
        {
            HandleBarrelHit(other);
            gunController.HitEffectMetall();
        }
        else
        {
            gunController.HitEffectMetall(); // Handle other metal objects
        }
    }

    private void HandleLevel2Collision(Collider other)
    {
        Debug.Log("We are shooting on level 2");

        if (other.CompareTag("zombieHead") || other.CompareTag("zombieLeg") || other.CompareTag("zombieBody"))
        {
            ApplyDamageToZombieWithSpecificTags(other);
            gunController.HitEffectBlood();
        }
        else if (other.CompareTag("Barrels"))
        {
            HandleBarrelHit(other);
            gunController.HitEffectMetall();
        }
        else if (other.CompareTag("Zombielvl1"))
        {
            ApplyDamageToZombie(other);
            gunController.HitEffectBlood();
        }
        else
        {
            gunController.HitEffectMetall(); // Handle other metal objects
        }
    }

    private void ApplyDamageToZombie(Collider other)
    {
        EnemyMovement zombHealth = other.GetComponent<EnemyMovement>();
        if (zombHealth != null)
        {
            Debug.Log("Zombie got shot.");
            zombHealth.TakeDamage(zombieDamageAmount);
        }
        else
        {
            Debug.LogError("EnemyMovement component not found on zombie.");
        }
    }

    private void HandleBarrelHit(Collider other)
    {
        NewBehaviourScript barrelScript = other.GetComponent<NewBehaviourScript>();
        if (barrelScript != null)
        {
            Debug.Log("Barrel got hit");
            barrelScript.TakeDamage(); // Destroy the barrel
        }
        else
        {
            Debug.LogError("NewBehaviourScript component not found on barrel.");
        }
    }

    private void ApplyDamageToZombieWithSpecificTags(Collider other)
    {
        ZombHealth zombHealth = other.GetComponentInParent<ZombHealth>();
        if (zombHealth == null)
        {
            Debug.LogError("ZombHealth component not found on parent.");
            return;
        }

        switch (other.tag)
        {
            case "zombieHead":
                float headDamage = 4f;
                Debug.Log("Head hit! Extra damage applied.");
                zombHealth.TakeDamage(headDamage);
                break;
            case "zombieBody":
                float bodyDamage = 1f;
                Debug.Log("Body hit! Extra damage applied.");
                zombHealth.TakeDamage(bodyDamage);
                break;
            case "zombieLeg":
                HandleZombieLegHit(other);
                break;
        }
    }

    private void HandleZombieLegHit(Collider other)
    {
        
        EnemyMovementL2 zombiIdle = other.GetComponentInParent<EnemyMovementL2>();
        if (zombiIdle != null)
        {
            zombiIdle.zombieIsIdle();

        }
        else
        {
            Debug.LogError("NavMeshAgent component not found on zombie.");
        }
    }

    private void DestroyBullet()
    {
        if (tracerInstance != null)
        {
            Destroy(tracerInstance);
        }

        Destroy(gameObject);  // Destroy the bullet object
    }



}




