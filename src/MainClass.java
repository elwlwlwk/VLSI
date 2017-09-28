import cooling.*;
import dataStructure.TSPPath;
import route.GreedyRoute;
import route.Route;

public class MainClass {
	public static void main(String[] args){
		DataManager manager = new DataManager("pbd984.tsp");
		Route gr = new GreedyRoute(manager.getData());
		long start = System.currentTimeMillis();
		CoolingFunction coolingFunction[] = {new ExponentialCooling(),
				new LinealCooling(),
				new LogarithmicalCooling(),
				new QuadraticCooling()};
		//calculate SE
		SimulatedAnnealing SA = new SimulatedAnnealing(100, 0.9999, coolingFunction[3]);
		TSPPath temp = SA.run(gr.getRoute());
		manager.setData(temp);
		long end = System.currentTimeMillis();
		//print and write result to file
		System.out.println("\n" + (end - start) / 1000.0);
		manager.writeResult();
		System.out.println(temp.getDistance());
	}
}
