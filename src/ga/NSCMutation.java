package ga;

import tspUtil.MapInfo;
import tspUtil.PathCheck;

public class NSCMutation implements Mutation {

	private double mutationRate;

	private int neighborSize;
	
	public NSCMutation(double mutationRate, int neighborSize) {
		this.mutationRate = mutationRate;
		this.neighborSize = neighborSize;
	}

	@Override
	public void doMutation(GAElement[] populationList) {
		// TODO Auto-generated method stub
		int populationSize = populationList.length;

		int mutationSize = (int) (populationSize * mutationRate);

		for (int i = 1; i <= mutationSize; i++) {

			int firstPoint = (int)(Math.random()*1000) % (MapInfo.getInstance().getNumOfCity()-1 - neighborSize) + 1;
			int secondPoint = firstPoint + (int)(Math.random()*1000) % (neighborSize);
			
			
			swift(populationList[populationSize - i].path, firstPoint, secondPoint);

			populationList[populationSize - i].cost = PathCheck.getPathCost(populationList[populationSize - i].path);
		}
	}
	
	private void swift(int [] arr, int firstPoint, int secondPoint){
		int temp = arr[secondPoint];
		for(int i = secondPoint - 1; i >= firstPoint; i--){
			arr[i+1] = arr[i];
		}
		arr[firstPoint] = temp;
	}
}
