using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CargoScript : MonoBehaviour {
	public float cargoSpeed;

	string moveData;
	float targetX, targetY;
	int index = 0;
	int[] newData;

	// Use this for initialization
	void Start () {
		//cargoManager = 
		moveData = CargoManager.currentCargoData;
		//Debug.Log("in cargo : " + moveData);
		//Move();
		string[] data = moveData.Split(';');
		newData = new int[data.Length];
		targetX = 50;
		targetY = 0;
		for (int i = 0; i < data.Length; i++) {
			newData[i] = System.Convert.ToInt32(data[i]);
		}
	}
	
	// Update is called once per frame
	void Update () {
		if (index < newData.Length) {
			if (targetX == transform.position.x && targetY == transform.position.z) {
				//Debug.Log("aa");
				StopCoroutine("MoveCoroutine");
				targetX = newData[index];
				targetY = newData[index + 1];
				StartCoroutine("MoveCoroutine");
				index += 2;
			}
		}
	}

	void Move() {
		string[] data = moveData.Split(';');
		int[] newData = new int[data.Length];
		for(int i=0;i<data.Length;i++) {
			newData[i] = System.Convert.ToInt32(data[i]);
		}

		Debug.Log(newData[0]);
		Debug.Log(newData[1]);
		Debug.Log(newData[2]);
		Debug.Log(newData[3]);
		Debug.Log(newData[4]);

		for(int i=0;i<newData.Length;i+=2) {
			targetX = newData[i];
			targetY = newData[i + 1];
			if (targetX != transform.position.x || targetY != transform.position.z) {
				StartCoroutine("MoveCoroutine");
				
			}
		}
	}

	IEnumerator MoveCoroutine() {
		while (targetX != transform.position.x || targetY != transform.position.z) {
			if(targetX == transform.position.x) {
				float dif = targetY - transform.position.z;
				if (dif > cargoSpeed)
					dif = cargoSpeed;
				if (dif < -cargoSpeed)
					dif = -cargoSpeed;
				transform.Translate(new Vector3(0, 0, dif));
			}
			else if (targetY == transform.position.z) {
				float dif = targetX - transform.position.x;
				if (dif > cargoSpeed)
					dif = cargoSpeed;
				if (dif < -cargoSpeed)
					dif = -cargoSpeed;
				transform.Translate(new Vector3(dif, 0, 0));
			}
			yield return new WaitForSeconds(0.01f);
		}
	}


}
