package ga;

import tspUtil.GetTwoRandomNumber;
import tspUtil.PathCheck;
import tspUtil.SwapCity;

public class SwapMutation implements Mutation {

	private double mutationRate;
	public SwapMutation(double mutationRate) {
		super();
		this.mutationRate = mutationRate;
	}

	@Override
	public void doMutation(GAElement[] populationList) {
		// TODO Auto-generated method stub
		int populationSize = populationList.length;

		int mutationSize = (int) (populationSize * mutationRate);

		for (int i = 1; i <= mutationSize; i++) {

			int [] twoRandNumber = GetTwoRandomNumber.getTwoRandomNumber();
			
			SwapCity.swapCity(populationList[populationSize - i].path, twoRandNumber[0], twoRandNumber[1]);

			populationList[populationSize - i].cost = PathCheck.getPathCost(populationList[populationSize - i].path);

		}
	}
}
