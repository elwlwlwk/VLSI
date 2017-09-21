package tspUtil;

public class GetTwoRandomNumber {
	public static int[] getTwoRandomNumber(){
		int[] arr = new int[2];
		int numOfCity = MapInfo.getInstance().getNumOfCity();
		int firstNum = (int)(Math.random()*1000) % (numOfCity-1) + 1;
		int secondNum = (int)(Math.random()*1000) % (numOfCity-1) + 1;
		
		while(firstNum == secondNum) secondNum = (int)(Math.random()*1000) % (numOfCity-1) + 1;
		
		arr[0] = Math.min(firstNum, secondNum);
		arr[1] = Math.max(firstNum, secondNum);
		
		return arr;
	}
}
