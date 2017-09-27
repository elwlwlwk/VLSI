package opt;

import DataStructure.Node;
import java.util.ArrayList;

public class ThreeOpt implements Opt {
		@Override
	public ArrayList<Node> Swap(ArrayList<Node> node) {
		int index1 = (int) (Math.random() * node.size());
		int index2 = (int) (Math.random() * node.size());
		int index3 = (int) (Math.random() * node.size());
			Node temp = node.get(index1);
			node.set(index1, node.get(index2));
			node.set(index2, node.get(index3));
			node.set(index3, temp);
		return node;
	}
}
