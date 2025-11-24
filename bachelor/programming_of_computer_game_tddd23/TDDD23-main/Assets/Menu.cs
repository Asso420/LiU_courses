using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class PauseMenu : MonoBehaviour
{
    public static bool GameIsPaused = false;


    public GameObject pauseMenuUI;
    public GameObject background;
    public GameObject GameOverMenu;
    private PlayerHealth playerHealth;
    private Transform player;    

    private void Start()
    {
        Cursor.visible = false;
        Cursor.lockState = CursorLockMode.Locked;
        playerHealth = GameObject.Find("Player").GetComponent<PlayerHealth>();
    }
    private void Update()
    {


        if (Input.GetKeyDown(KeyCode.Escape) && !PlayerHealth.isDead && !PlayerController.playerWon)
        {
            if (GameIsPaused)
            {
                ResumeButton();
            }
            else
            {
                Pause();
            }
        }
        if (PlayerHealth.isDead)
        {
            GameOver();
        }

    }
   
    void Pause()
    {
        background.SetActive(true);
        pauseMenuUI.SetActive(true);
        Time.timeScale = 0f;
        GameIsPaused = true;
        Cursor.visible = true;
        Cursor.lockState = CursorLockMode.None;
    }
    void GameOver()
    {
        background.SetActive(true);
        GameOverMenu.SetActive(true);
        Time.timeScale = 0.2f;
        Cursor.visible = true;
        Cursor.lockState = CursorLockMode.None;
    }
    public void ResumeButton()
    {
        background.SetActive(false);
        pauseMenuUI.SetActive(false);
        Time.timeScale = 1f;
        GameIsPaused = false;
        Cursor.visible = false;
        Cursor.lockState = CursorLockMode.Locked;
    }
    public void LoadMenu()
    {
        Time.timeScale = 1f;
        GameIsPaused = false;
        background.SetActive(false);
        pauseMenuUI.SetActive(false);
        PlayerHealth.isDead = false;
        GameTimer.instance.ResetTimer();
        GameTimer.instance.SetPaused(true);
        SceneManager.LoadScene(0);

    }
    public void RestartButton()
    {
        Time.timeScale = 1f;
        GameIsPaused = false;
        background.SetActive(false);
        pauseMenuUI.SetActive(false);
        GameOverMenu.SetActive(false);
        if(SceneManager.GetActiveScene().buildIndex == 2)
        {
            GameTimer.instance.RestoreSavedTime();

        }
        else
        {
            GameTimer.instance.ResetTimer();

        }
        
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
        playerHealth.SetHealth();
    }
    public void QuitButton()
    {
        Debug.Log("Quit");
        Application.Quit();
    }

}



