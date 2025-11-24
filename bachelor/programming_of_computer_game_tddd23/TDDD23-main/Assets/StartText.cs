using UnityEngine;
using TMPro; // For TextMeshPro, remove this if using standard UI Text
using UnityEngine.UI; // If using standard UI Text

public class RemoveText : MonoBehaviour
{
    public TextMeshProUGUI displayText; // For TextMeshPro, change to `Text` if using standard UI Text
    public float displayDuration = 3.0f; // Duration to display the text before removing it

    void Start()
    {
        displayText = GetComponent<TextMeshProUGUI>(); // For TextMeshPro, use `Text` if you're using regular UI Text
        Invoke("RemoveTextObject", displayDuration); // Call RemoveTextObject after displayDuration seconds
    }

    void RemoveTextObject()
    {
        gameObject.SetActive(false); // Disable the text object
    }
}
