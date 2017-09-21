package ga;

import java.util.Arrays;

public class GAElement {
	public int [] path;
	public int cost;
	
	@Override
	protected Object clone() throws CloneNotSupportedException {
		// TODO Auto-generated method stub
		GAElement cloneObj = new GAElement();
		cloneObj.cost = this.cost;
		cloneObj.path = Arrays.copyOf(this.path, path.length);
		
		return cloneObj;
	}
	
}
