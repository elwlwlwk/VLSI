
package tspUtil;

import java.util.Arrays;
import java.io.*;
public class PathCheck {
	/*
	 * 모든 경로의 합 계산
	 * 경로 형식은 만약 5개의 도시면
	 * int형의 배열에
	 * 0 1 2 3 4 0
	 * 또는
	 * 0 2 4 1 3 0
	 * 식의 형태를 띄어야함(출발지와 도착지가 같아야하며 모든 도시의 index가 한번씩 있어야함)
	 */
	public static double getPathCost(int [] path){
		
		double totalCost = 0;
		double [][] map = Initialize.getInstance().getDistances();
		
		for(int i = 0; i < path.length - 1;i++){
			totalCost += map[path[i]][path[i+1]];
		}
		return totalCost;
	}
	/*
	 * 경로가 적합한 경로인지 확인
	 * 경로 형식은 만약 5개의 도시면
	 * int형의 배열에
	 * 0 1 2 3 4 0
	 * 또는
	 * 0 2 4 1 3 0
	 * 식의 형태를 띄어야함(출발지와 도착지가 같아야하며 모든 도시의 index가 한번씩 있어야함)
	 */
	public static boolean isPathDuplicated(int [] path){
		boolean [] visited = new boolean[ Initialize.getInstance().getNumOfCity()];
		
		Arrays.fill(visited, false);
		
		//출발지와 도착지가 같은지 확인
		if(path[0] != path[path.length-1]) return true;
		
		for(int i = 0; i < path.length-1;i++){
			if(visited[i]) return true;
			else visited[i] = true;
		}
		return false;
	}
	
	public static void printPath(int [] path){
		System.out.println(path.length);
		for(int i = 0; i < path.length; i++){
			System.out.println(path[i]+ " ");
		}
		
	}
	public static void writePath(int [] path){
		double score= getPathCost(path);
		try {
		     
		      BufferedWriter out = new BufferedWriter(new FileWriter("result.txt"));
		      
		      out.write(Double.toString(score));
		     
		      out.write(", path : "); 
		      for(int i = 0; i < path.length; i++){
					out.write(Integer.toString(path[i]));
					 out.write("\t"); 
		      }
		     
		      out.close();
		      
		    } catch (IOException e) {
		        System.err.println(e); 
		        System.exit(1);
		    }

		  }
	}

