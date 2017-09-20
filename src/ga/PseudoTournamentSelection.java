package ga;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class PseudoTournamentSelection implements Selection{
	

	private int firstParent;
	private int secondParent;
	private int tournamentSize;
	private int populationSize;

	public PseudoTournamentSelection(int populationSize, int tournamentSize) {
		super();
		this.tournamentSize = tournamentSize;
		this.populationSize = populationSize;
	}

	@Override
	public int getFirstParent() {
		// TODO Auto-generated method stub
		
		return this.firstParent;
	}
	@Override
	public int getSecondParent() {
		// TODO Auto-generated method stub
		return this.secondParent;
	}

    @Override
	public void setParentList() {
		// TODO Auto-generated method stub
		//assume list is sorted
        List<Integer> idxList = new ArrayList<>();
        for(int i = 0; i < populationSize; i++){
            idxList.add(i);
        }
        Collections.shuffle(idxList);
        int min_idx = populationSize;

        for(int i = 0; i< tournamentSize; i++){
            if(min_idx > idxList.get(i)){
                min_idx = idxList.get(i);
            }
        }
        this.firstParent = min_idx;
        min_idx = populationSize;

        for(int i = tournamentSize; i < tournamentSize * 2; i++){
            if(min_idx > idxList.get(i)){
                min_idx = idxList.get(i);
            }
        }
        this.secondParent = min_idx;
	}
}
