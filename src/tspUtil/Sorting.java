package tspUtil;

import java.util.Arrays;

public class Sorting {
	public static int[] getIndexOfSortedArray(double [] arr){
		int [] retArr = new int[arr.length];
		boolean [] visited = new boolean[arr.length];
		double [] sortedArr = Arrays.copyOf(arr, arr.length);
		
		Arrays.sort(sortedArr);
		
		for(int i = 0; i < retArr.length; i++){
			for(int j = 0; j < retArr.length; j++){
				if(arr[j] == sortedArr[i] && visited[j] != true) {
					retArr[i] = j;
					visited[j] = true;
					break;
				}
			}
		}
		return retArr;
	}
}
