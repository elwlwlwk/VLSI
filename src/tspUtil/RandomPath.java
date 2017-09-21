package tspUtil;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class RandomPath {
	public static int[]	 getRandomPath(int startCity){
		int numOfCity = MapInfo.getInstance().getNumOfCity();
		int [] path = new int[numOfCity + 1];
		
		List<Integer> list = new ArrayList<Integer>();
		int idx = 0;
		for(int i = 0; i < numOfCity; i++){
			if(idx == startCity){
				idx++;
				continue;
			}
			list.add(idx);
			idx++;
		}
		
		Collections.shuffle(list);
		
		path[0] = startCity;
		path[numOfCity] = startCity;
		
		for(int i = 0; i < list.size(); i++){
			path[i+1] = list.get(i);
		}
		return path;
	}
}
