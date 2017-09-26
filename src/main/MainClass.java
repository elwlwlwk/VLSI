package main;

import java.util.Scanner;

import ga.Crossover;
import ga.Initializer;
import ga.Mutation;
import ga.MyGASearch;
import ga.PMXCrossover;
import ga.PseudoTournamentSelection;
import ga.RandomInitializer;
import ga.SAInitalizer;
import ga.Selection;
import ga.SwapMutation;
import greedy.NearestNeighbor;
import greedy.TwoOptSearch;
import sa.SASearch;
import tspUtil.PathCheck;
import tspUtil.Initialize;

public class MainClass {
	public static void main(String[] args){
		String mapName = "xqf131.tsp";
		Initialize.getfile(mapName);
		long start = System.currentTimeMillis();
		SASearch saSearch = new SASearch(1000, 0.99);
		int [] path3 = saSearch.calculatePath();
		long end = System.currentTimeMillis();
		System.out.println("실행시간 : " + (end - start) / 1000.0);
		System.out.println("SA search: " + PathCheck.getPathCost(path3));
		PathCheck.printPath(path3);
		//Initialize.getInstance().checkPath(path3);
		PathCheck.writePath(path3);
	}
//	public static void main(String[] args) {
//		// TODO Auto-generated method stub
//		System.out.print("Enter Map name (Usually Sample.txt): ");
//		Scanner scan = new Scanner(System.in);
//		String mapName = scan.next();
//		Initialize.getfile(mapName);
//		System.out.print("Select Alg (1. Nearest Neighbor, 2. Two-Opt, 3. SA, 4. GA) : ");
//
//		int input = scan.nextInt();
//		scan.close();
//		switch(input){
//		case 1:
//
//			NearestNeighbor nearestNeighbor = new NearestNeighbor();
//			int [] path = nearestNeighbor.calculatePath();
//			System.out.println("Nearest Neighbor: " + PathCheck.getPathCost(path));
//			break;
//		case 2:
//			TwoOptSearch twoOptSearch = new TwoOptSearch(1000000);
//			int [] path2 = twoOptSearch.calculatePath();
//			System.out.println("two opt search: " + PathCheck.getPathCost(path2));
//			break;
//		case 3:
//			double [] temperatureTrial = {10, 20, 30, 50, 100, 1000};
//
//			SASearch saSearch = new SASearch(1000, 0.98);
//			int [] path3 = saSearch.calculatePath();
//			System.out.println("SA search: " + PathCheck.getPathCost(path3));
//			PathCheck.printPath(path3);
//			//Initialize.getInstance().checkPath(path3);
//			PathCheck.writePath(path3);
//			break;
//		case 4:
//			int populationSize = 100;
//			int generationSize = 10000;
//
//			//Initialize by SA
//			Initializer saInitializer = new SAInitalizer(30, 0.8, 10000, 5);
//			//Random Initialize
//			Initializer randInitializer = new RandomInitializer();
//
//			Selection ptSelection = new PseudoTournamentSelection(populationSize, 10);
//
//			Mutation swapMutation = new SwapMutation(0.3);
//			//Mutation nscMutation = new NSCMutation(0.3, 4);
//
//
//			Crossover pmxCrossover = new PMXCrossover();
//
//			MyGASearch myGASearch = new MyGASearch(populationSize , generationSize);
//
//			myGASearch.setProcess(saInitializer, pmxCrossover, ptSelection, swapMutation);
//			//myGASearch.setProcess(randInitializer, pmxCrossover, ptSelection, swapMutation);
//
//			int [] path4 = myGASearch.calculatePath();
//			for(int i = 0; i< myGASearch.generationScore.length;i++){
//				System.out.println(myGASearch.generationScore[i]);
//			}
//
//			System.out.println("GA: " + PathCheck.getPathCost(path4));
//			break;
//		}
//		System.out.println("Experiment End");
//	}
}
