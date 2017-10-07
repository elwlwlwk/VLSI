package util;

import java.util.Arrays;

public class RecencyTabu implements Tabu {
	private int memory[];
	private int count = 0;
	private int optSize;
	public RecencyTabu(int size, int optSize){
		memory = new int[size];
		this.optSize = optSize;
	}
	
	private boolean isValid(int i) {
		boolean ret = false;
		for(int iter : memory){
			ret = ret || (iter == i);
		}
		return ret;
	}
	
	private boolean isValid(int[] i) {
		boolean ret = false;
		for(int iter : i){
			ret = ret || isValid(iter);
		}
		return ret;
	}
	
	@Override
	public int[] getOptIndex(int nodeSize) {
		int opt[] = new int[this.optSize];
		Arrays.fill(opt, -1);
		while(!isValid(opt)){
			for(int i = 0; i < opt.length; i++){
				opt[i] = (int)(Math.random() * nodeSize);
			}
		}
		Arrays.sort(opt);
		for(int iter : opt){
			memory[count++ % memory.length] = iter;
		}
		return opt;
	}
}
