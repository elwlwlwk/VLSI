package ga;

public interface Crossover {
	public GAElement[] crossover(GAElement firstParent, GAElement secondParent);
}
