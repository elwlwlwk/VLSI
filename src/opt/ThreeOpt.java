package opt;

import dataStructure.Node;
import util.ArrayUtill;

import java.util.ArrayList;
import java.util.Arrays;

public class ThreeOpt implements Opt {
	@Override
	public ArrayList<Node> Swap(ArrayList<Node> node) {
		int trialMax = 10000;
		double bestScore = ArrayUtill.cost(node) + 5;
		ArrayList<Node> bestPath = new ArrayList<Node>(node);
		
		System.out.println("start : " + ArrayUtill.cost(node));
		
		for(int trial = 0; trial < trialMax; trial++){
			double dist1 = ArrayUtill.cost(bestPath);
			int index[] = {(int)(Math.random() * bestPath.size()),
					(int)(Math.random() * bestPath.size()),
					(int)(Math.random() * bestPath.size())};
			Arrays.sort(index);
			if(index[0] >= node.size()
					|| index[0] >= node.size()
					|| index[0] >= node.size()){
				continue;
			}
			
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
			
			for(int i = 0; i < createdPath.length; i++){
				if(ArrayUtill.cost(createdPath[i]) < bestScore){
					bestScore = ArrayUtill.cost(createdPath[i]);
					bestPath = createdPath[i];
				}
			}
			double dist2 = ArrayUtill.cost(bestPath);
			if(dist2 > dist1){
				System.out.println("up!! " + dist2);
			}
		}
		return bestPath;
	}
}
