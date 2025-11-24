using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class LevelLoader : MonoBehaviour
{
    public Animator transition;
    public float transitionTime = 1f;

    // Update is called once per frame
    private void Update()
    {
        if (DoorController.isDoorOpen && DoorController.isPlayerNearby && PlayerController.hasKey)
        {
            LoadNextLevel();

        }
    }
    public void LoadNextLevel()
    {
        transition.SetTrigger("NewLevel");
        PlayerController.hasKey = false;
        PlayerHealth.isDead = false;
        PlayerController.playerWon = false;
        StartCoroutine(LoadLevel(SceneManager.GetActiveScene().buildIndex + 1));
    }
    IEnumerator LoadLevel(int levelIndex)
    {

        yield return new WaitForSeconds(transitionTime);
        GameTimer.instance.SaveCurrentTime();
        SceneManager.LoadScene(levelIndex);
    }
}
