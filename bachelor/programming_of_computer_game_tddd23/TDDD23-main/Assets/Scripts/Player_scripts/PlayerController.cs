using Cinemachine;
using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.Animations.Rigging;
using UnityEngine.UI;

public class PlayerController : MonoBehaviour
{
    [Header("Movement Settings")]
    [SerializeField] float baseSpeed = 5f;
    [SerializeField] float sprintMultiplier = 1.5f;
    [SerializeField] float jumpSpeed = 5f;
    [SerializeField] float gravityMultiplier = 2f; // Increased gravity control
    [SerializeField] float rotationSpeed = 500f;
    [Header("Ground Check Settings")]
    [SerializeField] Vector3 groundCheckOffset;
    [SerializeField] public static bool hasKey = true;
  
    private float ySpeed;
    private bool isGrounded;
    private bool isJumping;
    private bool isMoving;
    private bool walkingBackwards;
    private bool isAiming;
    private bool isShooting;
    private bool isReloading;
    private bool isRunning;
    private Quaternion targetRotation;
    private CameraController cameraController;
    private Animator animator;
    private CharacterController characterController;
    [SerializeField] AudioSource walkSound;
    public static bool playerWon = false;  





    private void Awake()
    {
   
        cameraController = Camera.main.GetComponent<CameraController>();
        animator = transform.Find("Boss").GetComponent<Animator>();
        characterController = GetComponent<CharacterController>();
        
    }

    private void Update()
    {
        if (PlayerHealth.isDead)
        {
            // Stop all movement and actions if the player is dead
            animator.SetFloat("moveAmount", 0f);
            animator.SetBool("isDead", true);
            StopAllSounds();
            return; // Exit the Update method to prevent any further movement or rotation
        }
        if (playerWon)
        {
            // Stop all movement and actions if the player has won
            animator.SetFloat("moveAmount", 0f);
            animator.SetBool("Victory", true);
            StopAllSounds();
            return; // Exit the Update method to prevent any further movement or rotation

        }
        else
        {
            animator.SetBool("Victory", false);
        }
        isShooting = Input.GetMouseButtonDown(0);
        //isShooting = Input.GetKeyDown(KeyCode.E);
        isAiming = Input.GetMouseButton(1);
        HandleMovement();
        HandleRotation();
        HandleAimingAnimation();
        
    }
   
    public bool GetAimingState()
     {
        return isAiming;
     }
    public bool GetShootingState()
    {
        return isShooting;
    }
    public void SetShootingStat(bool stat)
    {
        isShooting = stat;
    }
    public bool GetStateMoving()
    {
        return isMoving;
    }
    public bool GetRunningState() // New method to get running state
    {
        return isRunning;
    }
    public void SetReloadingState(bool state)
    {
        isReloading = state;
    }
    public void RotateTowards(Vector3 direction)
    {
        if (direction.magnitude > 0.1f)
        {
            Quaternion targetRotation = Quaternion.LookRotation(direction);
            transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, rotationSpeed * Time.deltaTime);
        }
    }

private void HandleAimingAnimation()
    {
        if (!isAiming) return;

        Vector3 moveInput = new Vector3(Input.GetAxis("Horizontal"), 0, Input.GetAxis("Vertical")).normalized;
        bool isMoving = moveInput.magnitude > 0;

        // Update movement-related animation only if the player is moving
        if (isMoving)
        {
            UpdateMovementAnimation(moveInput);
        }
        else
        {
            // Set moveAmount to 0 when not moving
            animator.SetFloat("moveAmount", 0f, 0.05f, Time.deltaTime);
        }
    }

    private void UpdateMovementAnimation(Vector3 moveInput)
    {
        float moveSpeed = Input.GetKey(KeyCode.LeftShift) ? baseSpeed * sprintMultiplier : baseSpeed;
        float inputMagnitude = Mathf.Clamp01(moveInput.magnitude);
        float moveAmount = inputMagnitude * (Input.GetKey(KeyCode.LeftShift) ? 1f : 0.5f);

        // Set animator parameters
        animator.SetFloat("moveAmount", moveAmount, 0.05f, Time.deltaTime);

        // Check and set if walking backwards
        bool isWalkingBackwards = Input.GetKey(KeyCode.S);
        animator.SetBool("BackWard", isWalkingBackwards);
    }

    
   
    
    private void HandleMovement()
    {
        // Get input
        float horizontalInput = Input.GetAxis("Horizontal");
        float verticalInput = Input.GetAxis("Vertical");

        Vector3 moveInput = new Vector3(horizontalInput, 0, verticalInput).normalized;
        float inputMagnitude = Mathf.Clamp01(moveInput.magnitude);


        float moveSpeed = (!isAiming && Input.GetKey(KeyCode.LeftShift) && !isReloading) ? baseSpeed * sprintMultiplier : baseSpeed;
        float moveAmount = inputMagnitude * (Input.GetKey(KeyCode.LeftShift) && !isAiming && !isReloading ? 1f : 0.5f);
        animator.SetFloat("moveAmount", moveAmount, 0.05f, Time.deltaTime);
        isRunning = (!isAiming && Input.GetKey(KeyCode.LeftShift) && inputMagnitude > 0 && !isReloading); // Update running state
        //PlayMovementSound(inputMagnitude);
        // Movement direction based on camera
        Vector3 moveDirection = cameraController.PlanarRotation * moveInput;
        isGrounded = characterController.isGrounded;
        if (isGrounded)
        {
            animator.SetBool("isGrounded", true);
            animator.SetBool("isJumping", false);
            animator.SetBool("isFalling", false);
            ySpeed = -1f; // Small downward force to keep grounded
            isJumping = false;
            isGrounded = true;

            if (Input.GetButtonDown("Jump") && !isJumping && !isAiming && !isReloading)
            {
                animator.SetBool("isJumping", true);
                animator.SetBool("isGrounded", false);
                animator.SetBool("isFalling", false);
                ySpeed = jumpSpeed;
                isJumping = true;
                isGrounded = false;

            }

        }
        else
        {
            // Apply gravity when not grounded
            ySpeed += Physics.gravity.y * gravityMultiplier * Time.deltaTime;
            if (ySpeed < 0 && !isJumping)
            {
                animator.SetBool("isFalling", true);
                animator.SetBool("isGrounded", false);
                animator.SetBool("isJumping", false);
                isGrounded = false;
            }

            // Reset jump after peak of jump (player starts falling)
            if (ySpeed < 0 && isJumping)
            {
                isJumping = false;
                isGrounded = false;
                animator.SetBool("isJumping", false);
                animator.SetBool("isFalling", true);

            }
        }



        // Calculate final movement vector
        Vector3 velocity = moveDirection * moveSpeed;
        velocity.y = ySpeed;


        // Move character
        characterController.Move(velocity * Time.deltaTime);

        if (characterController.isGrounded)
        {
            ySpeed = -0.5f;
            isJumping = false;
            isGrounded = true;
            animator.SetBool("isGrounded", true);
            animator.SetBool("isJumping", false);
            animator.SetBool("isFalling", false);
        }
    }

 

    private void HandleRotation()
    {
        // Get input
        float horizontalInput = Input.GetAxis("Horizontal");
        float verticalInput = Input.GetAxis("Vertical");


        // Rotate the character based on the movement direction relative to the camera
        if (horizontalInput != 0 || verticalInput != 0)
        {
            isMoving = true;
           animator.SetBool("isMoving", true);
            Vector3 moveDirection = cameraController.PlanarRotation * new Vector3(horizontalInput, 0, verticalInput).normalized;

            // Only apply rotation if moveDirection is not zero
            if (moveDirection != Vector3.zero && !isAiming)
            {
                targetRotation = Quaternion.LookRotation(moveDirection);
                transform.rotation = Quaternion.RotateTowards(transform.rotation, targetRotation, rotationSpeed * Time.deltaTime);
            }
        }

        else
        {
            isMoving = false;
            animator.SetBool("isMoving", false);
        }
    }
    private void PlayMovementSound(float inputMagnitude)
    {
           if (inputMagnitude > 0 && isGrounded && !isJumping)
        {
            if (!walkSound.isPlaying)
            {
                walkSound.Play();
            }
        }
        else
        {
            StopAllSounds(); // Stop sounds when not moving
        }
    }

    private void StopAllSounds()
    {
        walkSound.Stop();
    }
}
   
   






