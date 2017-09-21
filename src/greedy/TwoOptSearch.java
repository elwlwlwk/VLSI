package greedy;

import java.util.Arrays;

import tspUtil.GetTwoRandomNumber;
import tspUtil.PathCheck;
import tspUtil.TSPAlgorithm;

public class TwoOptSearch extends TSPAlgorithm{

	protected int limitTrial;
	
	public TwoOptSearch(){
		this.limitTrial = 100000;
	}
	
	public TwoOptSearch(int limitTrial){
		this.setTwoOptSearchParameter(limitTrial);
	}
	
	public void setTwoOptSearchParameter(int limitTrial){
		this.limitTrial = limitTrial;
	}
	
	@Override
	public int[] calculatePath(int [] path) {
		// TODO Auto-generated method stub
		int bestScore = PathCheck.getPathCost(path);
		
		int [] copyPath = Arrays.copyOf(path, path.length);
		int [] maxPath = Arrays.copyOf(path, path.length);
		
		int trial = 0;
		
		while(trial < this.limitTrial){
			
			int [] twoRandArr = GetTwoRandomNumber.getTwoRandomNumber();
			
			int firstPoint = twoRandArr[0];
			int secondPoint = twoRandArr[1];
			
			int [] trialPath = Arrays.copyOf(copyPath, copyPath.length);
			
			swapPath(trialPath, firstPoint, secondPoint);
			
			int currentPath = PathCheck.getPathCost(trialPath);
			
			if(bestScore > currentPath){
				maxPath = Arrays.copyOf(trialPath, trialPath.length);
				copyPath = Arrays.copyOf(trialPath, trialPath.length);
				bestScore = currentPath;
			}
			trial++;
		}
		return maxPath;
	}

	@Override
	public int[] calculatePath(int startPoint) {
		// TODO Auto-generated method stub
		NearestNeighbor simpleGreedy = new NearestNeighbor();
		int [] path = simpleGreedy.calculatePath(startPoint);
		
		path = this.calculatePath(path);
		return path;
	}
	
	public void swapPath(int [] arr, int firstPoint, int secondPoint){
		if(firstPoint < 1 || secondPoint > arr.length-1){
			System.err.println("2opt.. index error in swapPath func");
			System.exit(1);			
		}
		for(int i = 0; i < (secondPoint - firstPoint)/2; i++){
			int temp = arr[secondPoint - i];
			arr[secondPoint - i] = arr[firstPoint + i];
			arr[firstPoint + i] = temp;
		}
	}
}
