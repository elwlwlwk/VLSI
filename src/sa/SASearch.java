package sa;

import java.util.Arrays;
import greedy.ThreeOptSearch;
import tspUtil.Initialize;
import tspUtil.PathCheck;
import tspUtil.TSPAlgorithm;

public class SASearch extends TSPAlgorithm{
	private double temperature;
	private double deltaTemperature;
	
	public SASearch(double temperature, double deltaTemperature) {
		this.setSAParameter(temperature, deltaTemperature);
	}

	private void setSAParameter(double temperature, double deltaTemperature) {
		if (temperature <= 0) {
			System.err.println("Temperature must be bigger than 0");
			System.exit(1);
		}
		this.temperature = temperature;
		if (!(deltaTemperature < 1 && deltaTemperature > 0)) {
			System.err.println("delta value of temperature must be between 0 to 1");
			System.exit(1);
		}
		this.deltaTemperature = deltaTemperature;
	}

	@Override
	public int[] calculatePath() {
		// TODO Auto-generated method stub
		int[] path = Initialize.getInstance().getPath();
		path = this.calculatePath(path);
		return path;
	}

	@Override
	public int[] calculatePath(int[] path) {
		// TODO Auto-generated method stub
		int i = 1;
		int[] copyPath = Arrays.copyOf(path, path.length);
		double bestScore = PathCheck.getPathCost(copyPath);
		while (this.temperature > 1) {
			int[] trialPath = Arrays.copyOf(copyPath, copyPath.length);
			trialPath = ThreeOptSearch.swap(trialPath);
			double trialScore = PathCheck.getPathCost(trialPath);
			if (Math.random() < this.getAcceptProbability(bestScore, trialScore)) {
				copyPath = Arrays.copyOf(trialPath, trialPath.length);
				bestScore = trialScore;
			}
			this.temperature *= quadraticCooling(i);
		}
		return copyPath;
	}
	
	private double exponentialCooling(){
		return this.deltaTemperature;
	}
	
	private double logarithmicalCooling(int i){
		return (1 + this.deltaTemperature * Math.log(i))
				/ (1 + this.deltaTemperature * Math.log((i + 1)));
	}
	
	private double linearCooling(int i){
		return (1 + this.deltaTemperature * (i - 1))
				/ (1 + this.deltaTemperature * i);
	}
	
	private double quadraticCooling(int i){
		return (1 + this.deltaTemperature * Math.pow(i - 1, 2))
				/ (1 + this.deltaTemperature * Math.pow(i, 2));
	}

	private double getAcceptProbability(double bestScore, double trialScore) {
		if (bestScore > trialScore)
			return 1.0;
		else {
			return Math.pow(Math.E, (bestScore - trialScore) / this.temperature);
		}
	}
	
}
