package ga;

import java.util.Arrays;

import tspUtil.GetTwoRandomNumber;
import tspUtil.PathCheck;
import tspUtil.SwapCity;

public class PMXCrossover implements Crossover{
	
	
	
	@Override
	public GAElement[] crossover(GAElement firstParent, GAElement secondParent) {
		// TODO Auto-generated method stub
		GAElement [] child = new GAElement[2];
		child[0] = new GAElement();
		child[1] = new GAElement();
		
		int [] firstPath = Arrays.copyOf(firstParent.path, firstParent.path.length);
		int [] secondPath = Arrays.copyOf(secondParent.path, secondParent.path.length);
		
		int [] twoRandNumber = GetTwoRandomNumber.getTwoRandomNumber();
		
		int firstPoint = twoRandNumber[0];
		int secondPoint = twoRandNumber[1];
		
		for(int i = firstPoint; i <= secondPoint; i++){
			int idx1 = this.getIndexOfCity(firstPath, secondParent.path[i]);
			SwapCity.swapCity(firstPath, i, idx1);
			
			int idx2 = this.getIndexOfCity(secondPath, firstParent.path[i]);
			SwapCity.swapCity(secondPath, i, idx2);
		}
		
		child[0].path = firstPath;
		child[0].cost = PathCheck.getPathCost(child[0].path);
		child[1].path = secondPath;
		child[1].cost = PathCheck.getPathCost(child[1].path);
		
		return child;
	}
	
	private int getIndexOfCity(int [] arr, int city){
		for(int i = 0; i < arr.length; i++){
			if(arr[i] == city) return i;
		}
		return -1;
	}
	
}
