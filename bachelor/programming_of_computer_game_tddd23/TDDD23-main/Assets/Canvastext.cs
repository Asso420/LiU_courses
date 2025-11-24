using UnityEngine;

public class Billboard : MonoBehaviour
{
    private Camera mainCamera;

    void Start()
    {
        mainCamera = Camera.main;
    }

    void LateUpdate()
    {
        // Make the UI text always face the camera
        transform.LookAt(transform.position + mainCamera.transform.forward);
    }
}

