package ga;

import sa.SASearch;
import tspUtil.PathCheck;
import tspUtil.RandomPath;

import java.util.Random;

public class SAInitalizer implements Initializer{

	private double temperature;
	private double deltaTemperature;
	private int limitTrial;
	private int numOfNextHop;
	
	
	public SAInitalizer(double temperature, double deltaTemperature, int limitTrial, int numOfNextHop) {
		this.temperature = temperature;
		this.deltaTemperature = deltaTemperature;
		this.limitTrial = limitTrial;
		this.numOfNextHop = numOfNextHop;
	}


	@Override
	public GAElement[] initializePopulation(int populationSize, int startCity) {
		// TODO Auto-generated method stub
		Random gen = new Random();
		GAElement[] populationList = new GAElement[populationSize];
		for(int i = 0; i < populationSize; i++){
			int randTrail = (int)( this.limitTrial * gen.nextFloat());
			SASearch sa = new SASearch(this.temperature, this.deltaTemperature, randTrail, numOfNextHop);
			populationList[i] = new GAElement();
			populationList[i].path = sa.calculatePath(RandomPath.getRandomPath(startCity));
			populationList[i].cost = PathCheck.getPathCost(populationList[i].path);
		}
		return populationList;
	}
	
}
