package ga;

import tspUtil.PathCheck;
import tspUtil.RandomPath;

public class RandomInitializer implements Initializer{

	
	@Override
	public GAElement[] initializePopulation(int populationSize, int startCity) {
		// TODO Auto-generated method stub
		GAElement[] populationList = new GAElement[populationSize];
		for(int i = 0; i < populationSize; i++){
			populationList[i] = new GAElement();
			populationList[i].path = RandomPath.getRandomPath(startCity);
			populationList[i].cost = PathCheck.getPathCost(populationList[i].path);
		}
		return populationList;
	}
	
}
