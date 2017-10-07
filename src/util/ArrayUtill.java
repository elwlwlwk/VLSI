package util;

import dataStructure.Node;

import java.util.ArrayList;

public class ArrayUtill {
	public static ArrayList<Node> reverse(ArrayList<Node> path){
		ArrayList<Node> ret = new ArrayList<Node>();
		for(int i = 0; i < path.size(); i++){
			ret.add(path.get(path.size() - i - 1));
		}
		return ret;
	}
	
	public static ArrayList<Node> concat(ArrayList<Node> added, ArrayList<Node> adding){
		ArrayList<Node> ret = new ArrayList<Node>(added);
		ret.addAll(adding);
//		for(int i = 0; i < adding.size(); i++){
//			ret.add(adding.get(i));
//		}
		return ret;
	}
	
	public static double cost(ArrayList<Node> path){
		double ret = 0;
		for(int i = 0; i < path.size() - 1; i++){
			ret += path.get(i).getDistance(path.get(i + 1));
		}
		return ret;
	}
}
