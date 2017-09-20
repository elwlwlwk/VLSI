package ga;

import java.util.Comparator;

public class GAElementComparator implements Comparator<GAElement>{

	@Override
	public int compare(GAElement o1, GAElement o2) {
		// TODO Auto-generated method stub
		
		return o1.cost < o2.cost ? -1 :(o1.cost == o2.cost ? 0: 1);
	}
	
}
