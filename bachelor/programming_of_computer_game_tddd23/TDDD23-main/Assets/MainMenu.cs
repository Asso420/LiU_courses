using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class MainMenu : MonoBehaviour
{
    private void Awake()
    {
        GameTimer.instance.ResetTimer(); // Reset the timer when the main menu is loaded
        GameTimer.instance.SetPaused(true); // Pause the timer when the main menu is loaded
    }
    // Start is called before the first frame update
    public void PlayGame()
    { 
        GameTimer.instance.SetPaused(false); // Resume the timer
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex + 1);
    }

    public void QuitGame()
    {
        Debug.Log("Quit");
        Application.Quit();
    }
}
