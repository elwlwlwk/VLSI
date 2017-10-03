package opt;

import dataStructure.Node;
import util.ArrayUtill;
import util.RecencyTabu;
import util.Tabu;

import java.awt.*;
import java.lang.reflect.Array;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Queue;


public class ThreeOpt implements Opt {
	Tabu tabu;
	
	public ThreeOpt(){
		this(new RecencyTabu(30, 3));
	}
	
	public ThreeOpt(Tabu tabu){
		this.tabu = tabu;
	}
	
	@Override
	public ArrayList<Node> Swap(ArrayList<Node> node) {
		int trialMax = 500;
		double bestScore = Double.MAX_VALUE;
		ArrayList<Node> bestPath = new ArrayList<Node>(node);
		
		for(int trial = 0; trial < trialMax; trial++){
			int index[] = tabu.getOptIndex(node.size());
			
			ArrayList<Node> subPath1 = new ArrayList<Node>(bestPath.subList(0, index[0]));
			ArrayList<Node> subPath2 = new ArrayList<Node>(bestPath.subList(index[0], index[1]));
			ArrayList<Node> subPath3 = new ArrayList<Node>(bestPath.subList(index[1], index[2]));
			ArrayList<Node> subPath4 = new ArrayList<Node>(bestPath.subList(index[2], bestPath.size()));
			
			ArrayList<Node> reverseSubPath2 = ArrayUtill.reverse(subPath2);
			ArrayList<Node> reverseSubPath3 = ArrayUtill.reverse(subPath3);
			
			ArrayList[] createdPath = new ArrayList[7];
			createdPath[0] = ArrayUtill.concat(subPath1, ArrayUtill.concat(subPath2, ArrayUtill.concat(reverseSubPath3, subPath4)));
			createdPath[1] = ArrayUtill.concat(subPath1, ArrayUtill.concat(reverseSubPath2, ArrayUtill.concat(subPath3, subPath4)));
			createdPath[2] = ArrayUtill.concat(subPath1, ArrayUtill.concat(reverseSubPath2, ArrayUtill.concat(reverseSubPath3, subPath4)));
			createdPath[3] = ArrayUtill.concat(subPath1, ArrayUtill.concat(subPath3, ArrayUtill.concat(subPath2, subPath4)));
			createdPath[4] = ArrayUtill.concat(subPath1, ArrayUtill.concat(subPath3, ArrayUtill.concat(reverseSubPath2, subPath4)));
			createdPath[5] = ArrayUtill.concat(subPath1, ArrayUtill.concat(reverseSubPath3, ArrayUtill.concat(subPath2, subPath4)));
			createdPath[6] = ArrayUtill.concat(subPath1, ArrayUtill.concat(reverseSubPath3, ArrayUtill.concat(reverseSubPath2, subPath4)));
			for(ArrayList iter : createdPath){
				if(ArrayUtill.cost(iter) < bestScore){
					bestScore = ArrayUtill.cost(iter);
					bestPath = iter;
				}
			}
		}
		System.out.println();
		return bestPath;
	}
}
