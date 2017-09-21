package tspUtil;

public class GetShiftedTSPPath {

	public static int [] getShiftedTSPPath(int [] path, int startCity){
		
		int numOfCity = path.length;
		int [] retPath = new int[numOfCity + 1];
		int idx =0;
		for(int i = 0; i < path.length; i++){
			if(path[i] == startCity) idx = i;
		}
		
		retPath[numOfCity] = startCity;
		
		int offset = path.length - idx;
		
		for(int i = 0;i < path.length; i++){
			retPath[(i + offset) % path.length] = path[i];
		}
		
		return retPath;
	}
}
