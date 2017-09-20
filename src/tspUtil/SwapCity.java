package tspUtil;

public class SwapCity {
	public static void swapCity(int [] arr, int firstCity, int secondCity){
		int temp = arr[firstCity];
		arr[firstCity] = arr[secondCity];
		arr[secondCity] = temp;
	}
}
