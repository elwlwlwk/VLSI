package tspUtil;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.LineNumberReader;

public class MapInfo {
	//Singleton pattern
	private static MapInfo instance = null;
	private int numOfCity; // 도시 숫자
	private int distanceMap[][]; // 두 도시간의 거리 저장, symmetric matrix

	

	public static void setMapInfoInstance(String filename){
		instance = new MapInfo(filename);
	}
	
	public static MapInfo getInstance(){
		return instance;
	}
	
	private MapInfo(String filename) {
		this.setNumOfCity(filename);
		this.setDistanceMap(filename);
	}
	
	public int getNumOfCity() {
		return numOfCity;
	}
	
	public int[][] getDistanceMap() {
		return distanceMap;
	}

	public int getTwoCityDistance(int firstCityIndex, int secondCityIndex){
		return this.distanceMap[firstCityIndex][secondCityIndex];
	}
	
	//지도 정보 초기화
	//각 도시간의 거리를 나타내는 2차원 행렬로써 symmetric한 지도라고 가정
	
	private void setDistanceMap(String filename) {
		this.distanceMap = new int[this.numOfCity][this.numOfCity];

		BufferedReader reader = null;

		try {
			reader = new BufferedReader(new FileReader(filename));
		} catch (FileNotFoundException e) {
			System.err.println("File not found");
			System.exit(1);
		}

		for (int i = 0; i < numOfCity; i++) {
			try {
				String str = reader.readLine();

				String[] splitedStr = str.split(" ");

				for (int j = 0; j < splitedStr.length; j++) {
					this.distanceMap[i][j] = Integer.parseInt(splitedStr[j]);
				}

			} catch (IOException e) {
				System.err.println("File read error");
				System.exit(1);
			}
		}
		try {
			reader.close();
		} catch (IOException e) {
			System.err.println("Reader close error");
			System.exit(1);
		}
		for(int i = 0; i < numOfCity; i++){
			for(int j = i + 1; j < numOfCity; j++){
				this.distanceMap[i][j] = this.distanceMap[j][i];
			}
		}
	}
	// 파일에서 도시의 숫자를 초기화
	// 도시 개수 = 파일의 줄 수
	private void setNumOfCity(String filename) {
		this.numOfCity = 0;

		LineNumberReader reader = null;

		try {
			reader = new LineNumberReader(new FileReader(filename));
		} catch (FileNotFoundException e) {
			System.err.println("File not found");
			System.exit(1);
		}
		String str = null;
		while (true) {
			try {
				str = reader.readLine();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				System.err.println("File read error");
				System.exit(1);
			}
			if (str == null || str.equals(""))
				break;

			this.numOfCity++;
		}
		try {
			reader.close();
		} catch (IOException e) {
			System.err.println("Reader close error");
			System.exit(1);
		}
	}
}
