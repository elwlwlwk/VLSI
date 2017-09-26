package tspUtil;

public abstract class TSPAlgorithm {
	protected double map[][];
	protected int numOfCity;
	
	public TSPAlgorithm(){
		this.map = Initialize.getInstance().getDistances();
		this.numOfCity = Initialize.getInstance().getNumOfCity();
	}
	
	public abstract int [] calculatePath();
	public abstract int [] calculatePath(int [] path);
}
