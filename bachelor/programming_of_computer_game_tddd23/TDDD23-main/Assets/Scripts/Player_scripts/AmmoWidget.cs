using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AmmoWidget : MonoBehaviour
{
    public TMPro.TextMeshProUGUI ammoText;
    // Start is called before the first frame update
    public void SetAmmoText(int currentAmmo, int totalAmmo)
    {
        ammoText.text = $"{currentAmmo}/{totalAmmo}";
    }
}
