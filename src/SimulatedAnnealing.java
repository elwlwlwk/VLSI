import cooling.CoolingFunction;
import cooling.ExponentialCooling;
import dataStructure.TSPPath;

public class SimulatedAnnealing {
	private double temperature;
	private double deltaTemperature;
	private CoolingFunction cooling;
	public SimulatedAnnealing(double temp, double delta){
		this(temp, delta, new ExponentialCooling());
	}
	
	public SimulatedAnnealing(double temp, double delta, CoolingFunction cooling){
		this.temperature = temp;
		this.deltaTemperature = delta;
		this.cooling = cooling;
	}
	
	public void setCoolingFunction(CoolingFunction clooling){
		this.cooling = cooling;
	}
	
	public TSPPath run(TSPPath currentPath){
		TSPPath best = new TSPPath(currentPath);
		int counter = 0;
		while(temperature > 1) {
			TSPPath now = new TSPPath(best);
			now.swap();
			
			double currentEnergy = currentPath.getDistance();
			double neighbourEnergy = now.getDistance();
			
			if (acceptanceProbability(currentEnergy, neighbourEnergy, temperature) > Math.random()) {
				currentPath = new TSPPath(now);
			}
			
			if(currentPath.getDistance() < best.getDistance()){
				best = new TSPPath(currentPath);
			}
			
			temperature *= cooling.coolingRate(deltaTemperature, counter++);
		}
		return best;
	}
	
	private double acceptanceProbability(double cEnergy, double nEnergy, double temperature){
		if(nEnergy < cEnergy){
			return 1.0;
		}
		return Math.exp((cEnergy - nEnergy) / temperature);
	}
}
