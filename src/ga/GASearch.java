package ga;

import tspUtil.TSPAlgorithm;

public abstract class GASearch extends TSPAlgorithm {
	protected int populationSize;
	protected int generationSize;
	
	protected GAElement[] populationList;
	
	protected Initializer initializer;
	protected Selection	selection;
	protected Mutation mutation;
	protected Crossover crossover;
	
	
	public GASearch(int populationSize, int generationSize){
		this.populationSize = populationSize;
		this.generationSize = generationSize;
		
		this.populationList = null;
		this.initializer = null;
		this.mutation = null;
		this.crossover = null;
	}
	
	public void setCrossover(Crossover crossover){
		this.crossover = crossover;
	}
	
	public void setMutation(Mutation mutation){
		this.mutation = mutation;
	}
	public void setInitializer(Initializer initializer){
		this.initializer = initializer;
	}
	
	public void setSelctionAlgorithm(Selection selection){
		this.selection = selection;
	}
	
	public void setProcess(Initializer initializer, Crossover crossover, Selection selection, Mutation mutation){
		this.initializer = initializer;
		this.crossover = crossover;
		this.selection = selection;
		this.mutation = mutation;
	}
}
