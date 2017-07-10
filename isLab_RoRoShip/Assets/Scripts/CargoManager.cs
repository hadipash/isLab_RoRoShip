using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CargoManager : MonoBehaviour {
	public static string currentCargoData;
	public static int cargoNum = 0;

	public GameObject cargo1;
	public Text cargoNumTextbox;
	public Text cargoDataTextbox;

	string[] datas;

	// Use this for initialization
	void Start () {
		string path = "./Assets/Sources/test.txt";
		datas = System.IO.File.ReadAllLines(path);
		//nextCargo();
	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown(KeyCode.Space)) { // 화물 생성
			nextCargo();
		}
	}

	void nextCargo() {
		currentCargoData = datas[cargoNum];
		cargoNum++;
		cargoNumTextbox.text = "화물 수 : " + cargoNum;
		cargoDataTextbox.text = "화물 정보 : " + currentCargoData;
		Instantiate(cargo1, transform);
		Debug.Log(currentCargoData);
	}
}