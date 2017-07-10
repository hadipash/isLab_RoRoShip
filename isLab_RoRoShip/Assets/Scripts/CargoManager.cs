using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CargoManager : MonoBehaviour {
	public static string data;
	public static int cargoNum = 0;

	string[] datas;

	// Use this for initialization
	void Start () {
		string path = "./Assets/Sources/test.txt";
		datas = System.IO.File.ReadAllLines(path);
		nextCargo();
	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown(KeyCode.Space)) { // 화물 생성
			nextCargo();
		}
	}

	void nextCargo() {
		data = datas[cargoNum];
		cargoNum++;
		Debug.Log(data);
	}
}
