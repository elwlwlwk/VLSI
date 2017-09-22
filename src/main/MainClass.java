package main;

import java.util.Scanner;

import ga.Crossover;
import ga.Initializer;
import ga.Mutation;
import ga.MyGASearch;
import ga.NSCMutation;
import ga.PMXCrossover;
import ga.PseudoTournamentSelection;
import ga.RandomInitializer;
import ga.SAInitalizer;
import ga.Selection;
import ga.SwapMutation;
import greedy.NearestNeighbor;
import greedy.TwoOptSearch;
import sa.SASearch;
import tspUtil.MapInfo;
import tspUtil.PathCheck;

public class MainClass {
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		System.out.print("Enter Map name (Usually Sample.txt): ");
		Scanner scan = new Scanner(System.in);
		String mapName = scan.next();
		MapInfo.setMapInfoInstance(mapName);
		System.out.print("Select Alg (1. Nearest Neighbor, 2. Two-Opt, 3. SA, 4. GA) : ");

		int input = scan.nextInt();
		scan.close();
		switch(input){
		case 1:

			NearestNeighbor nearestNeighbor = new NearestNeighbor();
			int [] path = nearestNeighbor.calculatePath(0);
			System.out.println("Nearest Neighbor: " + PathCheck.getPathCost(path));
			break;
		case 2:
			TwoOptSearch twoOptSearch = new TwoOptSearch(1000000);
			int [] path2 = twoOptSearch.calculatePath(0);
			System.out.println("two opt search: " + PathCheck.getPathCost(path2));
			break;
		case 3:
			double [] temperatureTrial = {10, 20, 30, 50, 100, 1000};

			SASearch saSearch = new SASearch(temperatureTrial[3],0.8, 100000, 1);
			int [] path3 = saSearch.calculatePath(0);
			System.out.println("SA search: " + PathCheck.getPathCost(path3));
			break;
		case 4:
			int populationSize = 100;
			int generationSize = 10000;

			//Initialize by SA
			Initializer saInitializer = new SAInitalizer(30, 0.8, 10000, 5);
			//Random Initialize
			Initializer randInitializer = new RandomInitializer();

			Selection ptSelection = new PseudoTournamentSelection(populationSize, 10);

			Mutation swapMutation = new SwapMutation(0.3);
			//Mutation nscMutation = new NSCMutation(0.3, 4);


			Crossover pmxCrossover = new PMXCrossover();

			MyGASearch myGASearch = new MyGASearch(populationSize , generationSize);

			myGASearch.setProcess(saInitializer, pmxCrossover, ptSelection, swapMutation);
			//myGASearch.setProcess(randInitializer, pmxCrossover, ptSelection, swapMutation);

			int [] path4 = myGASearch.calculatePath(0);
			for(int i = 0; i< myGASearch.generationScore.length;i++){
				System.out.println(myGASearch.generationScore[i]);
			}

			System.out.println("GA: " + PathCheck.getPathCost(path4));
			break;
		}
		System.out.println("Experiment End");
	}
}
