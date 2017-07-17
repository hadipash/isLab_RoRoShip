using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ShipManager : MonoBehaviour {
	string[] datas;
	public GameObject MainCamera;
	public GameObject[] Floor;
	public GameObject[] Wall;

	// Use this for initialization
	void Start () {
		string path = "./Assets/Sources/shipData.txt";
		datas = System.IO.File.ReadAllLines(path);
		float max = 0;
		float[] shipData = new float[9];

		int flag = 0;
		for (int i = 0; i < 3; i++) {
			string[] data = datas[i].Split(';');

			shipData[flag] = System.Convert.ToSingle(data[0]);
			shipData[flag + 1] = System.Convert.ToSingle(data[1]);
			shipData[flag + 2] = System.Convert.ToSingle(data[2]);
			Debug.Log(shipData[flag]);
			Debug.Log(shipData[flag + 1]);
			Debug.Log(shipData[flag + 2]);
			flag += 3;

			Floor[i].transform.localScale = new Vector3(shipData[flag], 1, shipData[flag + 1]);

			if (max < shipData[flag])
				max = shipData[flag];
		}

		CameraScript.cameraDistance = (max / 2) + 0.2f * max;

		//Wall[0].transform.SetPositionAndRotation(new Vector3(shipData[0]/20,))
	}
	
	// Update is called once per frame
	void Update () {
		
	}
}
