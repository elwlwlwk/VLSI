package greedy;

import java.util.Arrays;

import tspUtil.Sorting;
import tspUtil.TSPAlgorithm;

public class NearestNeighbor extends TSPAlgorithm {

	public NearestNeighbor() {
		super();
	}

	/*
	 * 시작점으로부터 시작해서 방문되지 않은 가장 가까운 노드로 방문
	 */
	@Override
	public int[] calculatePath(int startPoint) {
		// TODO Auto-generated method stub
		int[] path = new int[this.numOfCity + 1];

		

		path[0] = startPoint;
		path[this.numOfCity] = startPoint;
		
		
		path = this.calculatePath(path);
		return path;
	}

	@Override
	public int[] calculatePath(int[] path) {
		// TODO Auto-generated method stub
		boolean[] visited = new boolean[this.numOfCity];
		Arrays.fill(visited, false);
		
		visited[0] = true;
		
		for (int i = 0; i < this.numOfCity; i++) {
			int[] indexOfSortedArr = Sorting.getIndexOfSortedArray(this.map[path[i]]);

			for (int j = 0; j < this.numOfCity; j++) {
				if (!visited[indexOfSortedArr[j]]) {
					path[i + 1] = indexOfSortedArr[j];
					visited[indexOfSortedArr[j]] = true;
					break;
				}
			}
		}
		return path;
	}
}
