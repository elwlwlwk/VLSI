package ga;

import java.util.ArrayList;

public interface Initializer {
	public GAElement [] initializePopulation(int populationSize, int startCity);
}
