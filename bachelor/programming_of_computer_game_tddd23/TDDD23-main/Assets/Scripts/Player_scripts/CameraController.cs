//using System.Collections;
//using System.Collections.Generic;
//using Unity.VisualScripting;
//using UnityEngine;
//using Cinemachine;

//public class CameraController : MonoBehaviour
//{
//    [SerializeField] private CinemachineFreeLook freeLookCamera;  // Assign your FreeLook camera here
//    [SerializeField] private CinemachineVirtualCamera aimCamera;  // Assign your aim camera here
//    [SerializeField] Transform followTarget;
//    [SerializeField] Transform player;
//    [SerializeField] float baserotationSpeed = 2f;
//    [SerializeField] float distance = 5;
//    [SerializeField] float minVerticalAngle = -45;
//    [SerializeField] float maxVerticalAngle = 45;
//    [SerializeField] Vector2 framingOffset;
//    [SerializeField] bool invertX;
//    [SerializeField] bool invertY;


//    //[Header("Ground Check Settings")]
//    public float sensitivityX = 10f;
//    public float sensitivityY = 10f;
//    public float defaultSensitivityX = 10f;  // Sensitivity for default (non-aiming) mode
//    public float defaultSensitivityY = 10f;  // Sensitivity for default (non-aiming) mode
//    public float rotationSpeedMultiplier = 0.5f;  // Slows down the overall speed

//    private bool isMoving;

//    private float yaw = 0f;
//    private float pitch = 0f;

//    float rotationX;
//    float rotationY;
//    float invertYVal;
//    float invertXVal;
//    private bool isAiming;
//    private PlayerController playerController;


//    [Header("Camera setting base on starter asset")]
//    public GameObject CinemachineCameraTarget;
//    private float _cinemachineTargetYaw;
//    private float _cinemachineTargetPitch;
//    [SerializeField] public float TopClamp = 70.0f;
//    [SerializeField] public float BottomClamp = -30.0f;
//    [SerializeField] public float CameraAngleOverride = 0.0f;
//    private void Start()
//    {
//        _cinemachineTargetYaw = CinemachineCameraTarget.transform.rotation.eulerAngles.y;
//        playerController = player.GetComponent<PlayerController>();

//        Cursor.visible = false;
//        Cursor.lockState = CursorLockMode.Locked;
//    }

//    private void Update()
//    {
//        invertXVal = (invertX) ? -1 : 1;
//        invertYVal = (invertY) ? -1 : 1;
//        bool wasAiming = isAiming;
//        if (wasAiming == isAiming)
//        {
//            _cinemachineTargetYaw = CinemachineCameraTarget.transform.rotation.eulerAngles.y;
//            _cinemachineTargetPitch = CinemachineCameraTarget.transform.rotation.eulerAngles.x;
//        }
//        isAiming = Input.GetMouseButton(1);   // Right mouse button
//        SwitchCameras(isAiming);
//        isMoving = playerController.GetStateMoving();
//        if (isAiming)
//        {
//            baserotationSpeed = 0.75f;
//        }
//        else
//        {
//            baserotationSpeed = 2f;
//        }
//        if (isAiming && !isMoving)
//        {
//            RotateAimCamera();
//        }

//        // Update rotationX and clamp to prevent over-rotation
//        rotationX += Input.GetAxis("Mouse Y") * invertYVal * baserotationSpeed;
//        rotationX = Mathf.Clamp(rotationX, minVerticalAngle, maxVerticalAngle);

//        // Update rotationY based on mouse X-axis movement
//        rotationY -= Input.GetAxis("Mouse X") * invertXVal * baserotationSpeed;

//        // Apply the camera's target rotation
//        var targetRotation = Quaternion.Euler(rotationX, rotationY, 0);
//        var focusPosition = followTarget.position + new Vector3(framingOffset.x, framingOffset.y);

//    }

//    public Quaternion PlanarRotation => Quaternion.Euler(0, rotationY, 0);
//    // Method to switch between FreeLook and Aim cameras
//    private static float ClampAngle(float lfAngle, float lfMin, float lfMax)
//    {
//        if (lfAngle < -360f) lfAngle += 360f;
//        if (lfAngle > 360f) lfAngle -= 360f;
//        return Mathf.Clamp(lfAngle, lfMin, lfMax);
//    }
//    void SwitchCameras(bool isAiming)
//    {
//        if (isAiming)
//        {
//            aimCamera.Priority = 10;  // Higher priority
//            freeLookCamera.Priority = 5;  // Lower priority

//        }
//        else
//        {
//            aimCamera.Priority = 5;  // Lower priority
//            freeLookCamera.Priority = 10;  // Higher priority

//        }
//    }

//    void RotateAimCamera()
//    {
//        float horizontalInput = Input.GetAxis("Mouse X"); // or Input.GetAxis("Horizontal") for controller
//        float verticalInput = Input.GetAxis("Mouse Y");   // or Input.GetAxis("Vertical") for controller
//        if (horizontalInput != 0 || verticalInput != 0)
//        {
//            _cinemachineTargetYaw += horizontalInput * baserotationSpeed;
//            _cinemachineTargetPitch -= verticalInput * baserotationSpeed;

//        }

//        _cinemachineTargetYaw = ClampAngle(_cinemachineTargetYaw, float.MinValue, float.MaxValue);
//        _cinemachineTargetPitch = ClampAngle(_cinemachineTargetPitch, BottomClamp, TopClamp);
//        // Get input


//        CinemachineCameraTarget.transform.rotation = Quaternion.Euler(_cinemachineTargetPitch + CameraAngleOverride,
//               _cinemachineTargetYaw, 0.0f);
//     }
//}


using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;

public class CameraController : MonoBehaviour
{
    [SerializeField] Transform followTarget;
    [SerializeField] float aimSensitivityMultiplier = 0.5f;
    [SerializeField] float rotationSpeed = 2f;
    [SerializeField] float minVerticalAngle = -45f;
    [SerializeField] float maxVerticalAngle = 45f;
    public Vector3 framingOffset; // Offset for third-person view
    public Vector3 aimOffset; // Offset for aiming view
    public float transitionSpeed = 5f; // Speed of the transition
    public Vector3 aimCameraPosition;
    public Vector3 thirdPersonCameraPosition;
    [SerializeField] bool invertX;
    [SerializeField] bool invertY;
    private float rotationX;
    private float rotationY;
    private float invertYVal;
    private float invertXVal;
    private bool isAiming = false;
    private Vector3 currentCameraPosition;
    private Vector3 targetCameraPosition;
    private Quaternion currentRotation;
    private Quaternion targetRotation;
    [SerializeField] float cameraCollisionRadius = 0.2f; // Radius for collision detection
    [SerializeField] LayerMask collisionMask; // Layers that should block the camera
    [SerializeField] float minDistanceFromTarget = 0.5f; // Minimum distance the camera should maintain from the follow target
   

    private void Start()
    {
        //Cursor.visible = false;s
        //Cursor.lockState = CursorLockMode.Locked;
        currentCameraPosition = thirdPersonCameraPosition;
        currentRotation = Quaternion.identity;
        aimCameraPosition.x = -1f;
        aimCameraPosition.z = 3f;
        thirdPersonCameraPosition.z = 7f;
    }

    private void Update()
    {
        invertXVal = (invertX) ? -1 : 1;
        invertYVal = (invertY) ? -1 : 1;

        float currentRotationSpeed = rotationSpeed;

        if (Input.GetMouseButton(1)) // Right mouse button for aiming
        {
            isAiming = true;
            targetCameraPosition = aimCameraPosition;
            currentCameraPosition = Vector3.Lerp(currentCameraPosition, targetCameraPosition, transitionSpeed * Time.deltaTime);
            currentRotationSpeed *= aimSensitivityMultiplier; // Reduce sensitivity when aiming
        }
        else
        {
            isAiming = false;
            targetCameraPosition = thirdPersonCameraPosition;
            currentCameraPosition = Vector3.Lerp(currentCameraPosition, targetCameraPosition, transitionSpeed * Time.deltaTime);
        }

        rotationX += Input.GetAxis("Mouse Y") * invertYVal * currentRotationSpeed;
        rotationX = Mathf.Clamp(rotationX, minVerticalAngle, maxVerticalAngle);
        rotationY += Input.GetAxis("Mouse X") * invertXVal * currentRotationSpeed;

        targetRotation = Quaternion.Euler(rotationX, rotationY, 0);

        // Smooth rotation using Slerp for transitions
        currentRotation = Quaternion.Slerp(currentRotation, targetRotation, transitionSpeed * Time.deltaTime);

        // Apply the position and rotation
        Vector3 focusPosition = followTarget.position + (isAiming ? aimOffset : framingOffset);
        Vector3 desiredCameraPosition = focusPosition - currentRotation * currentCameraPosition;

        // Raycast to detect objects between camera and target
        RaycastHit hit;
        if (Physics.SphereCast(focusPosition, cameraCollisionRadius, desiredCameraPosition - focusPosition, out hit, currentCameraPosition.magnitude, collisionMask))
        {
            // If there's a collision, stop the camera at the hit point
            
            float hitDistance = Vector3.Distance(focusPosition, hit.point);

            // Ensure the camera doesn't get closer than the minimum distance
            if (hitDistance > minDistanceFromTarget)
            {
                transform.position = hit.point + hit.normal * cameraCollisionRadius;
            }
            else
            {
                // If too close, maintain the minimum distance from the target
                transform.position = focusPosition - currentRotation * Vector3.forward * minDistanceFromTarget;
            }
        }
        else
        {
            // No collision, apply the desired position
            transform.position = desiredCameraPosition;
        }

        transform.rotation = currentRotation;

    }

    public Quaternion PlanarRotation => Quaternion.Euler(0, rotationY, 0);
}

