using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WeaponPickup : MonoBehaviour
{
    public GunController gunPrefab;
    public float rotationSpeed = 50f; // Speed of the rotation
    public float bounceForce = 2f;    // Force for the bouncing effect
    public Transform gun;
    // Start is called before the first frame update
    void Start()
    {
       
    }
    void Update()
    {
        // Rotate the weapon slowly around the Y-axis
        gun.transform.Rotate(Vector3.up, rotationSpeed * Time.deltaTime);
    }
    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            Debug.Log("Player has picked up a weapon");
            SwitchWeapon activeWeapon = other.GetComponent<SwitchWeapon>();
            if (activeWeapon)
            {
                GunController newWeapon = Instantiate(gunPrefab);
                activeWeapon.Equip(newWeapon);
                Destroy(gameObject);

            }

        }
        
    }
}
