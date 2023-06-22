using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Zombie_Controller : MonoBehaviour
{
    private Renderer rendererComponent;
    private Animator animatorComponent;

    private float spawnInterval;

    // Start is called before the first frame update
    void Start()
    {
        rendererComponent = GetComponent<Renderer>();
        animatorComponent = GetComponent<Animator>();
    }

    // Update is called once per frame
    void Update()
    {
        if(rendererComponent.enabled == false)
        {
            spawnInterval = Random.Range(1f,3f);
            Invoke("Zombie_Spawn",spawnInterval);
        }
    }

    public void Zombie_Spawn()
    {
        rendererComponent.enabled = true;
    }

    public void Zombie_Death()
    {
        rendererComponent.enabled = false;
    }
}
