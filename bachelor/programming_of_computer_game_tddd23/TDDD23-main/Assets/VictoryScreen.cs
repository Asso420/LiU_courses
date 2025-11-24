using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UI;  // For handling UI elements

public class VictoryScreen : MonoBehaviour
{
    public GameObject background;
    public GameObject victoryMenu;
    public float delayBeforeVictoryScreen = 6f;  // Delay before showing the victory screen
    public CanvasGroup victoryCanvasGroup;  // To handle fade effect on victory menu

    public TextMeshProUGUI victoryMessageText;
    public TextMeshProUGUI bestTimeText;
    public TextMeshProUGUI currentTimeText;
    private bool victoryTriggered = false;
    private GameObject gun;

    private void Start()
    {
        Cursor.visible = false;
        Cursor.lockState = CursorLockMode.Locked;

        // Ensure the victory screen starts hidden
        victoryCanvasGroup.alpha = 0f;
        victoryMenu.SetActive(false);
        background.SetActive(false);
    }

    void Update()
    {
        if (Input.GetKey(KeyCode.O) && Input.GetKey(KeyCode.P))
        {
            ResetBestTime();  // Trigger reset
        }
        if (PlayerController.playerWon && !victoryTriggered)
        {
            victoryTriggered = true;
            gun = GameObject.FindWithTag("Gun");
            if (gun != null)
            {
                Destroy(gun);
            }
            StartCoroutine(ShowVictoryScreenWithDelay());
        }
    }

    // Coroutine to show the victory screen after a delay
    private IEnumerator ShowVictoryScreenWithDelay()
    {
        yield return new WaitForSeconds(delayBeforeVictoryScreen);  // Wait for the delay

        // Activate background and victory menu before starting fade
        background.SetActive(true);
        victoryMenu.SetActive(true);
        float bestTime = PlayerPrefs.GetFloat("BestTime", float.MaxValue);
        float currentTime = GameTimer.instance.GetCurrentTime(); // Assuming you have a method to get current time
        if (GameTimer.instance.IsNewBestTime())
        {
            victoryMessageText.text = "You set a new best time!";
        }
        else
        {
            victoryMessageText.text = "But seriously... what took you so long?";
        }
        bestTimeText.text = "Best Time: " + FormatTime(bestTime);
        currentTimeText.text = "Your Time: " + FormatTime(currentTime);
        StartCoroutine(FadeInVictoryScreen());  // Start fading in the victory menu
    }
    private string FormatTime(float time)
    {
        int minutes = Mathf.FloorToInt(time / 60);
        int seconds = Mathf.FloorToInt(time % 60);
        return string.Format("{0:D2}:{1:D2}", minutes, seconds);
    }

    // Coroutine to fade in the victory screen gradually
    private IEnumerator FadeInVictoryScreen()
    {
        float fadeDuration = 2f;  // Time it takes to fully fade in the screen
        float currentTime = 0f;

        while (currentTime < fadeDuration)
        {
            currentTime += Time.unscaledDeltaTime;  // Use unscaled time because time is paused
            victoryCanvasGroup.alpha = Mathf.Lerp(0f, 1f, currentTime / fadeDuration);
            yield return null;  // Wait for the next frame
        }

        Time.timeScale = 0.05f;  // Pauses the game after the fade is complete
        Cursor.visible = true;
        Cursor.lockState = CursorLockMode.None;
    }

    public void LoadMenu()
    {
        Time.timeScale = 1f;  // Resume time before loading menu
        background.SetActive(false);
        victoryMenu.SetActive(false);
        PlayerController.playerWon = false;
        SceneManager.LoadScene(0);  // Load the main menu (assuming it's scene index 0)
    }

    public void QuitButton()
    {
        Debug.Log("Quit");
        Application.Quit();
    }
    public void ResetBestTime()
    {
        PlayerPrefs.DeleteKey("BestTime");
        bestTimeText.text = "Best Time: --:--";
        Debug.Log("Best time reset!");
    }
}
