package greedy;

import java.util.Arrays;

import tspUtil.Sorting;
import tspUtil.TSPAlgorithm;

public class NearestNeighbor extends TSPAlgorithm {

	public NearestNeighbor() {
		super();
	}

	/*
	 * ���������κ��� �����ؼ� �湮���� ���� ���� ����� ���� �湮
	 */
	@Override
	public int[] calculatePath() {
		// TODO Auto-generated method stub
		int[] path = new int[this.numOfCity + 1];

		
		//임시로 0으로 설정
		path[0] = 0;
		path[this.numOfCity] = 0;
		
		
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
