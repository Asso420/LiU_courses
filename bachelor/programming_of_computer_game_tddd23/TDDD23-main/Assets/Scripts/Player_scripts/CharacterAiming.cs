using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Animations.Rigging;
using UnityEngine.Rendering;

public class CharacterAiming : MonoBehaviour
{
    private PlayerController playerController;

    private Rig RigLayer_GunPoseBody;  // Rig for not aiming
    private Rig RigLayer_GunPoseAiming;  // Rig for aiming
    private Rig RigLayer_BodyAim;  // Rig for aiming
    [SerializeField] LayerMask aimColliderLayerMask;
    [SerializeField] Transform aimtarget;
    [SerializeField] Transform secondaryTarget;
    public Canvas aimingCanvas;
    public bool hasGun;

    bool isAiming;
    bool isShooting;
    private void Awake()
    {
        Transform character = transform.Find("Boss");  

        if (character != null)
        {
            // Find the rig layers on the character model
            RigLayer_GunPoseBody = character.Find("RigLayer_GunPoseBody").GetComponent<Rig>();
            RigLayer_GunPoseAiming = character.Find("RigLayer_GunPoseAiming").GetComponent<Rig>();
            RigLayer_BodyAim = character.Find("RigLayer_BodyAim").GetComponent<Rig>();
        }
        else
        {
            Debug.LogError("Character model or rig layers not found!");
        }
    }
    void Start()
    {
        playerController = GetComponent<PlayerController>();
    }

   
    void Update()
    {
        isAiming = playerController.GetAimingState();
        isShooting = playerController.GetShootingState();
        
        UpdateRigAndAnimatorWeights();
        ShowAimingCanvas(isAiming);
        HandleAiming();
       
    }
    void ShowAimingCanvas(bool show)
    {
        if (hasGun && isAiming)
        {
            // Set the CrossHair child to active
            aimingCanvas.transform.Find("CrossHair").gameObject.SetActive(true);
        }
        else
        {
            // Set the CrossHair child to inactive
            aimingCanvas.transform.Find("CrossHair").gameObject.SetActive(false);
        }
    }
    private void HandleAiming()
    {
        if (!isAiming) return;

        Aiming();
        secondaryTarget.position = aimtarget.position;
    }

    private void Aiming()
    {
        Vector2 screenCenterPoint = new Vector2(Screen.width / 2, Screen.height / 2);
        Ray ray = Camera.main.ScreenPointToRay(screenCenterPoint);
        if (Physics.Raycast(ray, out RaycastHit raycastHit, 999f, aimColliderLayerMask))
        {
            aimtarget.position = raycastHit.point;
            Vector3 hitPoint = raycastHit.point;
            Vector3 direction = hitPoint - transform.position;
            direction.y = 0;
            playerController.RotateTowards(direction);
        }
    }
    private void UpdateRigAndAnimatorWeights()
    {
        if (hasGun)
        {
            float targetWeight = isAiming ? 1f : 0f;
            RigLayer_GunPoseBody.weight = Mathf.Lerp(RigLayer_GunPoseBody.weight, 1f - targetWeight, Time.deltaTime * 10f);
            RigLayer_GunPoseAiming.weight = Mathf.Lerp(RigLayer_GunPoseAiming.weight, targetWeight, Time.deltaTime * 10f);
            RigLayer_BodyAim.weight = Mathf.Lerp(RigLayer_BodyAim.weight, targetWeight, Time.deltaTime * 20f);


        }


      
    }
    public void SetHasGun(bool state)
    {
        hasGun = state;
    }
}
