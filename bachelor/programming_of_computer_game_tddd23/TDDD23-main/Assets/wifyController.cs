using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro; // For TextMeshPro

public class WifyController : MonoBehaviour
{
    // Animator for the wife
    private Animator animator;
    

    // Reference to the UI Text component (TextMeshPro or regular Text)
    public TextMeshProUGUI wifeDialogueText; // The text showing what the wife says

    public float gameOverDelay = 6f;

    // Wife's dialogue messages
    public string bestTimeDialogue = "You're amazing! You got here so fast!";
    public string regularTimeDialogue = "You finally made it, but you're late!";

    void Awake()
    {
        animator = transform.Find("Wife").GetComponent<Animator>();
        // Initially hide the dialogue text
        wifeDialogueText.gameObject.SetActive(false);
    }

    // This method is called when something enters the trigger collider
    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player"))
        {
           
            // Stop the timer when the player reaches the wife
            GameTimer.instance.SaveCurrentTime();
            GameTimer.instance.StopTimer();
            

            // Check if the player achieved a new best time
            if (GameTimer.instance.IsNewBestTime())
            {
                wifeDialogueText.text = bestTimeDialogue; // Wife says best time message
                animator.SetBool("BossWon", true);
            }
            else
            {
                wifeDialogueText.text = regularTimeDialogue; // Wife says regular time message
                animator.SetBool("BossLate", true);
            }

            // Show the text and play the animation when the player is close
            wifeDialogueText.gameObject.SetActive(true);

            PlayerController.playerWon = true;
        }
    }
}
