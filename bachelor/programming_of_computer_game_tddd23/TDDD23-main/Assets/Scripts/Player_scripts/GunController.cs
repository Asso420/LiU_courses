using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GunController : MonoBehaviour
{
    [Header("Gun Settings")]
    public GameObject pfBulletProjectile;
    [SerializeField] Transform bulletSpawnPoint;
    public Transform aimtarget;
    [SerializeField] ParticleSystem muzzleFlash;
    [SerializeField] ParticleSystem hitEffectMetall;
    [SerializeField] ParticleSystem hitEffectBlood;
    [SerializeField] AudioSource shootSound;

    public int maxAmmo = 30; // Max ammo capacity
    private int currentAmmo;
    void Start()
    {
        currentAmmo = maxAmmo;
    }

    public void Shoot()
    {
        if (currentAmmo <= 0)
        {
            Debug.Log("Out of ammo!");
            return;
        }

        if (shootSound != null)
            {
                shootSound.Play();
            }
            Vector3 aimDir = (aimtarget.position - bulletSpawnPoint.position).normalized;
            GameObject bullet = Instantiate(pfBulletProjectile, bulletSpawnPoint.position, Quaternion.LookRotation(aimDir));
            BulletProjectile bulletScript = bullet.GetComponent<BulletProjectile>();
            if (bulletScript != null)
            {
                bulletScript.gunController = this;
            }
            muzzleFlash.Emit(1);
            // hitEffect.transform.position = aimtarget.position; // Move the hit effect to the target point
            // hitEffect.Emit(1); // Emit the hit effect particle system
            currentAmmo--; // Reduce ammo in magazine
            Debug.Log("ammo left: " + currentAmmo);

    }
    public void HitEffectMetall()
    {
        hitEffectMetall.transform.position = aimtarget.position;
        hitEffectMetall.Emit(1);
    }
    public void HitEffectBlood()
    {
        hitEffectBlood.transform.position = aimtarget.position;
        hitEffectBlood.Emit(1);
    }
    public void Reload(int ammoAmount)
    {
        currentAmmo += ammoAmount; // Add ammo to the magazine
        if (currentAmmo > maxAmmo)
        {
            currentAmmo = maxAmmo; // Clamp to max ammo capacity
        }
    }
    public void SetAmmo(int ammo)
    {
        currentAmmo = ammo;
    }
    public int GetAmmo()
    {
        return currentAmmo;
    }


}
