/*
 * Created by Hyeongrok Heo
 * 2017-07-09
 * CameraScript.cs
 * 카메라의 시점 전환 및 좌표 변환을 담당하는 스크립트
 */

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraScript : MonoBehaviour {
	public float cameraSpeedX;
	public float cameraSpeedY;

	float cameraX, cameraY, cameraZ, angle;

	// Use this for initialization
	void Start () {
		angle = 45;
		//cameraX = 60.0f;
		cameraY = 30.0f;
		//cameraZ = -60.0f;
		
	}
	
	// Update is called once per frame
	void Update () {
		cameraX = 85.0f * Mathf.Sin(angle * Mathf.Deg2Rad);
		cameraZ = 85.0f * Mathf.Cos(angle * Mathf.Deg2Rad);

		transform.position = new Vector3(cameraX, cameraY, cameraZ);
		transform.rotation = Quaternion.LookRotation(new Vector3(-1*cameraX, -0.7f*cameraY, -1*cameraZ));
		//transform.rotation = Quaternion.LookRotation(new Vector3(30.0f, 0.0f, 30.0f));
		/*if (Input.GetKey(KeyCode.Alpha1)) {
			transform.position = new Vector3(60.0f, 30.0f, -60.0f);
			//transform.rotation = Quaternion.LookRotation(new Vector3(35.0f, -35.0f, 0.0f));
			transform.rotation = Quaternion.LookRotation(new Vector3(-60.0f, -30.0f, 60.0f));
		}*/
		/*if (Input.GetKey(KeyCode.Alpha2)) { // 2번 시점
            transform.position = new Vector3(60.0f, 30.0f, -60.0f);
			//transform.rotation = Quaternion.LookRotation(new Vector3(35.0f, -35.0f, 0.0f));
			transform.rotation = Quaternion.LookRotation(new Vector3(-60.0f, -30.0f, 60.0f));
		}
        if (Input.GetKey(KeyCode.Alpha3)) { // 3번 시점
            transform.position = new Vector3(60.0f, 30.0f, 60.0f);
			transform.rotation = Quaternion.LookRotation(new Vector3(-60.0f, -30.0f, -60.0f));
		}*/
        if (Input.GetKey(KeyCode.W)) { // 카메라 상 이동
            cameraY += cameraSpeedY;
			if (cameraY > 80)
				cameraY = 80;
        }
        if (Input.GetKey(KeyCode.S)) { // 카메라 하 이동
            cameraY -= cameraSpeedY;
			if (cameraY < 0)
				cameraY = 0;
        }
		if (Input.GetKey(KeyCode.A)) { // 카메라 좌 이동
			angle += cameraSpeedX;
		}
		if (Input.GetKey(KeyCode.D)) { // 카메라 우 이동
			angle -= cameraSpeedX;
		}/*
		if(Input.GetKey(KeyCode.Q)) {
			transform.position = new Vector3(50.0f,50.0f,30.0f);
			
			//-85 -40 -70

		}*/
	}
}