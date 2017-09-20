package sa;

import java.util.Arrays;

import greedy.TwoOptSearch;
import tspUtil.GetTwoRandomNumber;
import tspUtil.PathCheck;
import tspUtil.TSPAlgorithm;

public class SASearch extends TSPAlgorithm{
	private double temperature;
	private double deltaTemperature;
	private int numOfNextHop;
	
	private TwoOptSearch twoOptSearch;
	
	public SASearch(double temperature, double deltaTemperature, int limitTrial, int numOfNextHop) {
		this.twoOptSearch = new TwoOptSearch(limitTrial);
		this.setSAParameter(temperature, deltaTemperature);
		this.numOfNextHop = numOfNextHop;
	}

	public void setSAParameter(double temperature, double deltaTemperature) {
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
	public int[] calculatePath(int startPoint) {
		// TODO Auto-generated method stub
		int[] path = this.twoOptSearch.calculatePath(startPoint);
		path = this.calculatePath(path);
		return path;
	}

	@Override
	public int[] calculatePath(int[] path) {
		// TODO Auto-generated method stub

		int[] copyPath = Arrays.copyOf(path, path.length);
		int bestScore = PathCheck.getPathCost(copyPath);
		while (this.temperature > 1) {
			
			int[] trialPath = Arrays.copyOf(copyPath, copyPath.length);
			
			for(int i = 0; i < this.numOfNextHop ; i++){
				int[] twoRandNumber = GetTwoRandomNumber.getTwoRandomNumber();
				int firstPoint = twoRandNumber[0];
				int secondPoint = twoRandNumber[1];
				this.twoOptSearch.swapPath(trialPath, firstPoint, secondPoint);
			}
			
			trialPath = this.twoOptSearch.calculatePath(trialPath);
			
			int trialScore = PathCheck.getPathCost(trialPath);
			if (Math.random() < this.getAcceptProbability(bestScore, trialScore)) {
				copyPath = Arrays.copyOf(trialPath, trialPath.length);
				bestScore = trialScore;
			} 
			
			this.temperature *= this.deltaTemperature;
		}
		return copyPath;
	}

	private double getAcceptProbability(int bestScore, int trialScore) {
		if (bestScore > trialScore)
			return 1;
		else {
			return Math.pow(Math.E, -(trialScore - bestScore) / this.temperature);
		}
	}
	
}
