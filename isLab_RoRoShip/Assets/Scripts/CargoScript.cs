using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CargoScript : MonoBehaviour {

	// Use this for initialization
	void Start () {
		//cargoManager = 
		string moveData = CargoManager.currentCargoData;
		Debug.Log("in cargo : " + moveData);
		move();
	}
	
	// Update is called once per frame
	void Update () {
		
	}

	void move() {

	}
}
