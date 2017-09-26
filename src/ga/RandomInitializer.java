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
			//임시로 int로 형 변환
			populationList[i].cost = (int)PathCheck.getPathCost(populationList[i].path);
		}
		return populationList;
	}
	
}
