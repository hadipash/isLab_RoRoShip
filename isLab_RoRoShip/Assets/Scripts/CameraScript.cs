using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraScript : MonoBehaviour {

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		//transform.rotation = Quaternion.LookRotation(new Vector3(30.0f, 0.0f, 30.0f));
		if (Input.GetKey(KeyCode.Alpha1)) {
			transform.position = new Vector3(0.0f, 50.0f, 0.0f);
			//transform.rotation = Quaternion.LookRotation(new Vector3(35.0f, -35.0f, 0.0f));
			transform.rotation = Quaternion.LookRotation(new Vector3(0.0f, -1.0f, 0.0f));
		}
		if (Input.GetKey(KeyCode.Alpha2)) {
            transform.position = new Vector3(60.0f, 30.0f, -60.0f);
			//transform.rotation = Quaternion.LookRotation(new Vector3(35.0f, -35.0f, 0.0f));
			transform.rotation = Quaternion.LookRotation(new Vector3(-60.0f, -30.0f, 60.0f));
		}
        if (Input.GetKey(KeyCode.Alpha3)) {
            transform.position = new Vector3(60.0f, 30.0f, 60.0f);
			transform.rotation = Quaternion.LookRotation(new Vector3(-60.0f, -30.0f, -60.0f));
		}
        /*if (Input.GetKey(KeyCode.Alpha3)) {
            transform.Translate(35.0f, -135.0f, 0.0f);
        }/*
        /*if (Input.GetKey(KeyCode.D)) {
            transform.Translate(0.0f, 0.0f, 0.1f);
        }
		if(Input.GetKey(KeyCode.Q)) {
			transform.position = new Vector3(50.0f,50.0f,30.0f);
			
			//-85 -40 -70

		}*/
    }
}
