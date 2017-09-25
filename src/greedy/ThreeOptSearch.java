package greedy;

import java.util.Arrays;
import java.util.Random;
import java.util.Vector;

import tspUtil.PathCheck;

public class ThreeOptSearch {

	public static int[] reverse(int[] arr){
		int [] result= arr.clone();
		for(int i=0; i<arr.length; i++){
			result[result.length-i-1]= arr[i];
		}
		return result;
	}

	public static int[] concat(int[] arr1, int[] arr2){
		int [] result= new int[arr1.length+ arr2.length];
		for(int i=0; i< arr1.length; i++){
			result[i]= arr1[i];
		}
		for(int i=0; i< arr2.length; i++){
			result[arr1.length+i]= arr2[i];
		}
		return result;
	}

	public static int[] swap(int[] arr){
		Random random= new Random();

		int[] best_path= arr.clone();
		double best_score= PathCheck.getPathCost(arr);

		int trial_max= 10000;
		for(int trial=0; trial< trial_max; trial++){
			int [] idx= {(int) (random.nextFloat() * (best_path.length)), (int) (random.nextFloat() * (best_path.length)), (int) (random.nextFloat() * (best_path.length))};
			Arrays.sort(idx);
			if(idx[0]>= best_path.length || idx[1]>= best_path.length || idx[2]>= best_path.length){
				continue;
			}
			int [] sub_path1= Arrays.copyOfRange(best_path, 0, idx[0]);
			int [] sub_path2= Arrays.copyOfRange(best_path, idx[0], idx[1]);
			int [] sub_path3= Arrays.copyOfRange(best_path, idx[1], idx[2]);
			int [] sub_path4= Arrays.copyOfRange(best_path, idx[2], best_path.length);

			int [] rev_sub_path2= reverse(sub_path2);
			int [] rev_sub_path3= reverse(sub_path3);

			int[][] paths= new int[7][];
			paths[0]= concat(concat(concat(sub_path1, rev_sub_path2), sub_path3), sub_path4);
			paths[1]= concat(concat(concat(sub_path1, sub_path2), rev_sub_path3), sub_path4);
			paths[2]= concat(concat(concat(sub_path1, rev_sub_path2), rev_sub_path3), sub_path4);
			paths[3]= concat(concat(concat(sub_path1, sub_path3), sub_path2), sub_path4);
			paths[4]= concat(concat(concat(sub_path1, rev_sub_path3), sub_path2), sub_path4);
			paths[5]= concat(concat(concat(sub_path1, sub_path3), rev_sub_path2), sub_path4);
			paths[6]= concat(concat(concat(sub_path1, rev_sub_path3), rev_sub_path2), sub_path4);

			for(int i=1; i< paths.length; i++){
				double cur_score= PathCheck.getPathCost(paths[i]);
				if(cur_score< best_score){
					best_score= cur_score;
					best_path= paths[i].clone();
				}
			}
		}
		return best_path;
	}
}
