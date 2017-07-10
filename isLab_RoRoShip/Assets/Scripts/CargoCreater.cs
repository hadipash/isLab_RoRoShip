/*
 * Created by Hyeongrok Heo
 * 2017-07-10
 * CargoCreater.cs
 * 화물 생성 코드
 */

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CargoCreater : MonoBehaviour {
	public GameObject cargo1;

	// Use this for initialization
	void Start () {
		
	}
	
	// Update is called once per frame
	void Update () {
		if (Input.GetKeyDown(KeyCode.Space)) { // 화물 생성
			Instantiate(cargo1, transform);
		}
	}
}