import cooling.CoolingFunction;
import cooling.ExponentialCooling;
import cooling.LinearCooling;
import cooling.QuadraticCooling;
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
			TSPPath neighborPath = new TSPPath(currentPath);
			neighborPath.swap();
			
			double currentEnergy = currentPath.getDistance();
			double neighborEnergy = neighborPath.getDistance();
			System.out.println("current Energy : " + currentEnergy);
			System.out.println("neighbour Energy : " + neighborEnergy);
			
			double random = Math.random();
			double real = acceptanceProbability(currentEnergy, neighborEnergy, temperature);
			
			if (real > random) {
//				if(neighborPath.getDistance() > currentPath.getDistance()){
//					System.out.println("Up!");
//				}
//				else {
//					System.out.println("Down!");
//				}
				System.out.println("Accepted : " + real);
				System.out.println("Random : " + random);
				
				currentPath = new TSPPath(neighborPath);
			}
			
			if(currentPath.getDistance() < best.getDistance()){
				best = new TSPPath(currentPath);
			}
			
			temperature *= cooling.coolingRate(deltaTemperature, counter++);
			System.out.println("Temperature : " + temperature);
		}
		return best;
	}
	
	private double acceptanceProbability(double currentEnergy, double neighborEnergy, double temperature){
		if(neighborEnergy < currentEnergy){
			return 1.0;
		}
		return 1 / Math.exp((neighborEnergy - currentEnergy) / temperature);
	}
}
