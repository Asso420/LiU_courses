using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SwitchWeapon : MonoBehaviour
{
    private CharacterAiming characterAiming;
    private GunController gunController;
    private PlayerController playerController;
    public UnityEngine.Animations.Rigging.Rig HandK;
    public Transform WeaponParent;
    private Animator animator;

    public Transform aimtarget;
    private bool isAiming;
    private bool isShooting;
    private bool hasGun;
    private bool isReloading;
    public int totalAmmo = 40; // Total amount of ammo the player has
    public AmmoWidget ammoWidget;
    public CountDown countDown;
    public float reloadTime = 2f;
    //public Canvas Canvas;


    void Awake()
    {
        GunController existgunController = GetComponentInChildren<GunController>();
        if (existgunController)
        {
            Equip(existgunController);

        }
        playerController = GetComponent<PlayerController>();
        characterAiming = GetComponent<CharacterAiming>();
        animator = transform.Find("Boss").GetComponent<Animator>();

    }

    void Update()
    {
        UpdatePlayerState();
        UpdateHandPose();
        HandleShoot();
        HandleReload();
        UpdateAmmoWidget();
    }
    private void UpdateAmmoWidget()
    {
        if (hasGun)
        {
            ammoWidget.gameObject.SetActive(true);

            if (ammoWidget != null)
            {
                ammoWidget.SetAmmoText(gunController.GetAmmo(), totalAmmo);
            }
        }
        else
        {
            ammoWidget.gameObject.SetActive(false);

        }
    }
    private void UpdateHandPose()
    {
        HandK.weight = hasGun ? 1f : 0f;
    }
    private void UpdatePlayerState()
    {
        isAiming = playerController.GetAimingState();
        isShooting = playerController.GetShootingState();
        hasGun = gunController != null;
        characterAiming.SetHasGun(hasGun);
    }
   
    private void HandleShoot()
    { 
        if (isShooting && isAiming)
        {
            
            gunController.Shoot();
            playerController.SetShootingStat(false);


        }
    }
    private void HandleReload()
    {
        // Reload when the player presses 'R' or the gun is empty
        if (!isReloading && hasGun && gunController.GetAmmo() < gunController.maxAmmo && totalAmmo > 0 && Input.GetKeyDown(KeyCode.R) && !playerController.GetRunningState())
        {
            StartCoroutine(ReloadWeapon()); // Start the reload coroutine
        }

        // Auto reload if the gun is empty and total ammo is available
        if (!isReloading && hasGun && gunController.GetAmmo() <= 0 && totalAmmo > 0 && !playerController.GetRunningState())
        {
            StartCoroutine(ReloadWeapon()); // Start the reload coroutine
        }
    }
    private IEnumerator ReloadWeapon()
    {
        isReloading = true; // Mark as reloading
        playerController.SetReloadingState(isReloading); // Update the player controller
        float timeRemaining = reloadTime;
        countDown.gameObject.SetActive(true);
        animator.SetBool("isReloading", true);

        // Update the countdown UI during reload
        while (timeRemaining > 0)
        {
            timeRemaining -= Time.deltaTime;
            yield return null; // Wait for the next frame
        }

        // Perform the actual reload
        int ammoNeeded = gunController.maxAmmo - gunController.GetAmmo(); // How much ammo is needed to fully reload
        int ammoToReload = Mathf.Min(ammoNeeded, totalAmmo); // Determine how much ammo can be reloaded based on total ammo

        gunController.Reload(ammoToReload); // Reload the gun
        totalAmmo -= ammoToReload; // Deduct the reloaded ammo from the total ammo pool
        animator.SetBool("isReloading", false);
        isReloading = false; // Mark as not reloading
        playerController.SetReloadingState(isReloading); // Update the player controller
        countDown.gameObject.SetActive(false);
        Debug.Log("Reloading complete... Ammo reloaded: " + ammoToReload + " | Total Ammo Left: " + totalAmmo);

   

    }
    public void AddAmmo(int ammoAmount)
    {
        totalAmmo += ammoAmount;
        Debug.Log("Ammo added: " + ammoAmount + " | Total Ammo: " + totalAmmo);
    }
        public void Equip(GunController weapon)
    {
        if (gunController)
        {
            Destroy(gunController.gameObject);
        }
        gunController = weapon;
        gunController.aimtarget = aimtarget;
        gunController.transform.SetParent(WeaponParent);
        gunController.transform.localPosition = Vector3.zero;
        gunController.transform.localRotation = Quaternion.identity;


    }
  

}
