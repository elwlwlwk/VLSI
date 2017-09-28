package opt;

import dataStructure.Node;
import util.ArrayUtill;

import java.util.ArrayList;
import java.util.Arrays;

public class TwoOpt implements Opt {
	@Override
	public ArrayList<Node> Swap(ArrayList<Node> node) {
		int index[] = {(int)(Math.random() * node.size()),
				(int)(Math.random() * node.size())};
		Arrays.sort(index);
		
		ArrayList<Node> subPath1 = (ArrayList)node.subList(0, index[0]);
		ArrayList<Node> subPath2 = (ArrayList)node.subList(index[0], index[1]);
		ArrayList<Node> subPath3 = (ArrayList)node.subList(index[1], node.size());
		
		subPath2 = ArrayUtill.reverse(subPath2);
		node = ArrayUtill.concat(subPath1, ArrayUtill.concat(subPath2, subPath3));
		return node;
	}
}
