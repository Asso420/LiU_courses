using System.Collections;
using UnityEngine;
using UnityEngine.AI;  // Make sure to include this if you're using NavMesh

public class ZombieSpawner : MonoBehaviour
{
    public GameObject WhiteclownPrefab; // This should be a prefab with all scripts, NavMesh, etc., attached
    public float spawnInterval = 10f;    // Time interval between spawns

    // Start is called before the first frame update
    void Start()
    {
        // Start spawning the Whiteclown instances with a delay
        StartCoroutine(SpawnWhiteclownWithInterval());
    }

    // Coroutine for spawning zombies at regular intervals
    IEnumerator SpawnWhiteclownWithInterval()
    {
        // Optionally, add an initial delay if required
        yield return new WaitForSeconds(1f);

        // Spawn zombies at regular intervals
        while (true)
        {
            yield return new WaitForSeconds(spawnInterval);

            // Instantiate the Whiteclown prefab with all its components (NavMesh, scripts, etc.)
            // Ensure the newWhiteclown is not a child of the spawner
            GameObject newWhiteclown = Instantiate(WhiteclownPrefab, transform.position, transform.rotation);

            // Optional: Perform additional runtime configuration for the zombie if necessary
            NavMeshAgent navMeshAgent = newWhiteclown.GetComponent<NavMeshAgent>();
            if (navMeshAgent != null)
            {
                // Set up the NavMesh agent if needed
                navMeshAgent.enabled = true;  // Just an example, depends on your logic
            }
        }
    }
}
