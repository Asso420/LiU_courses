using System.Collections;
using UnityEngine;

public class KillZombieText : MonoBehaviour
{
    public CanvasGroup canvasGroup; // Reference to the CanvasGroup component
    public float fadeDuration = 2.0f; // Duration of the fade in seconds
    public float delayBeforeFade = 1.0f; // Delay before starting the fade

    void Start()
    {
        StartCoroutine(FadeOutTextAndImage());
    }

    IEnumerator FadeOutTextAndImage()
    {
        // Wait before starting the fade
        yield return new WaitForSeconds(delayBeforeFade);

        float elapsedTime = 0f;

        // Gradually fade out
        while (elapsedTime < fadeDuration)
        {
            elapsedTime += Time.deltaTime;
            canvasGroup.alpha = Mathf.Lerp(1f, 0f, elapsedTime / fadeDuration);
            yield return null;
        }

        // Ensure the alpha is fully set to 0
        canvasGroup.alpha = 0f;
        gameObject.SetActive(false);
    }
}
