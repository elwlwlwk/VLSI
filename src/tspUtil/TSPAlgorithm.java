package tspUtil;

public abstract class TSPAlgorithm {
	protected int map[][];
	protected int numOfCity;
	
	public TSPAlgorithm(){
		this.map = MapInfo.getInstance().getDistanceMap();
		this.numOfCity = MapInfo.getInstance().getNumOfCity();
	}
	
	public abstract int [] calculatePath(int startPoint);
	public abstract int [] calculatePath(int [] path);
}
