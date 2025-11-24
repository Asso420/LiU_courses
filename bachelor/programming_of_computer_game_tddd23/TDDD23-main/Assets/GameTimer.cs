using UnityEngine;
using TMPro;

public class GameTimer : MonoBehaviour
{
    public static GameTimer instance; // Singleton instance
    public TextMeshProUGUI timerText; // Reference to the UI Text component
    private float timeElapsed;
    private bool timerActive = true;
    private bool isPaused = false;  // New flag to check if game is paused
    private float savedTime;
    

    // Best time tracking
    private float bestTime;
    private bool isNewBestTime;

    void Awake()
    {
        // Ensure the timer persists between scenes
        if (instance == null)
        {
            instance = this;
            DontDestroyOnLoad(gameObject); // Keep this object across scenes
        }
        else
        {
            Destroy(gameObject);
        }

        LoadBestTime(); // Load the best time when the game starts
    }

    void Update()
    {
        if (timerActive && !isPaused) // Only count time if not paused
        {
            timeElapsed += Time.deltaTime;
            UpdateTimerDisplay();
        }
    }

    // Function to update the timer UI
    void UpdateTimerDisplay()
    {
        int minutes = Mathf.FloorToInt(timeElapsed / 60F);
        int seconds = Mathf.FloorToInt(timeElapsed % 60F);
        int milliseconds = Mathf.FloorToInt((timeElapsed * 100F) % 100F);

        timerText.text = $"{minutes:00}:{seconds:00}";
    }

    // Public function to stop the timer when the player wins
    public void StopTimer()
    {
        timerActive = false;

        // Check if this is a new best time
        if (timeElapsed < bestTime || bestTime == 0)
        {
            bestTime = timeElapsed;
            isNewBestTime = true;
            SaveBestTime(); // Save the best time to PlayerPrefs
        }
        else
        {
            isNewBestTime = false;
        }
    }

    // Public function to reset the timer
    public void ResetTimer()
    {
        timeElapsed = 0;
        timerActive = true;
        isPaused = false; // Reset the pause state as well
    }

    // Pause or resume the timer
    public void SetPaused(bool paused)
    {
        isPaused = paused;
    }

    // Save the best time using PlayerPrefs
    void SaveBestTime()
    {
        PlayerPrefs.SetFloat("BestTime", bestTime);
        PlayerPrefs.Save(); // Save PlayerPrefs data to disk
    }

    // Load the best time from PlayerPrefs
    void LoadBestTime()
    {
        bestTime = PlayerPrefs.GetFloat("BestTime", 0); // Load best time or 0 if no record exists
    }
    public void SaveCurrentTime()
    {
        savedTime = timeElapsed;
    }
    public float GetCurrentTime()
    {
        return savedTime;
    }

    public void RestoreSavedTime()
    {
        timeElapsed = savedTime;
        timerActive = true; // Ensure the timer resumes
        UpdateTimerDisplay(); // Update the UI with the restored time
    }

    // Public getter methods for current and best times
  
    public float GetBestTime()
    {
        return bestTime;
    }

    public bool IsNewBestTime()
    {
        return isNewBestTime;
    }
}
