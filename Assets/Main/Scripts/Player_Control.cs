using System;
using System.Collections;
using System.Net.Sockets;
using System.Text;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Player_Control : MonoBehaviour
{

    private TcpClient client;
    private NetworkStream stream;
    private Animator animatorComponent;

    private const string SHOOT_RIGHT_NAME = "Shooting_right";
    private const string SHOOT_LEFT_NAME = "Shooting_left";

    // Start is called before the first frame update
    void Start()
    {
        client = new TcpClient("localhost", 12345);
        stream = client.GetStream();
        animatorComponent = GetComponent<Animator>();

        StartCoroutine(ReadMessages());
    }
    IEnumerator ReadMessages()
    {
        byte[] data = new byte[1024];

        while (true)
        {
            if (stream.DataAvailable)
            {
                int bytesRead = stream.Read(data, 0, data.Length);
                string message = Encoding.UTF8.GetString(data, 0, bytesRead);

                string[] val = message.Split(',');
                foreach (var number in val)
                {
                    int dir = try_int(number);
                    // if(dir == 0)
                    // {
                    //     Debug.Log("No Value");
                    // }
                    if(dir == 1)
                    {
                        Debug.Log("Left");
                        animatorComponent.Play(SHOOT_LEFT_NAME);
                    }
                    if(dir == 2)
                    {
                        Debug.Log("Right");
                        animatorComponent.Play(SHOOT_RIGHT_NAME);
                    }
                }

                
            }

            yield return null;
        }
    }

    private int try_int(string v)
    {
        try
        {
            return int.Parse(v, System.Globalization.CultureInfo.InvariantCulture);
        } 
        catch
        {
            return 0;
        }
        
    }
        

    void OnApplicationQuit()
    {
        client.Close();
    }

}

