package opt;

import dataStructure.Node;
import util.ArrayUtill;

import java.util.ArrayList;
import java.util.Arrays;

public class TwoOpt implements Opt {
	@Override
	public ArrayList<Node> Swap(ArrayList<Node> node) {
		int TrialMax = 10000;
		ArrayList<Node> bestPath = new ArrayList<Node>(node);
		System.out.println("start : " + ArrayUtill.cost(node));
		for(int trial = 0; trial < TrialMax; trial++){
			int index[] = {(int)(Math.random() * bestPath.size()),
					(int)(Math.random() * bestPath.size())};
			Arrays.sort(index);
			
			ArrayList<Node> subPath1 = new ArrayList<Node>(bestPath.subList(0, index[0]));
			ArrayList<Node> subPath2 = new ArrayList<Node>(bestPath.subList(index[0], index[1]));
			ArrayList<Node> subPath3 = new ArrayList<Node>(bestPath.subList(index[1], bestPath.size()));
			
			subPath2 = ArrayUtill.reverse(subPath2);
			bestPath = ArrayUtill.concat(subPath1, ArrayUtill.concat(subPath2, subPath3));
		}
		
		return bestPath;
	}
}
