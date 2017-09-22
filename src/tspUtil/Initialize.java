package tspUtil;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.lang.Math;
import java.util.Arrays;

class Node{
    private int index;
    private int x;
    private int y;

    public Node(int index, int x, int y){
        this.index = index;
        this.x = x;
        this.y = y;
    }

    public int getIndex(){
        return index - 1;
    }

    public int getX(){
        return x;
    }

    public int getY(){
        return y;
    }
    
    public double getDistance(Node objective){
	    int deltaX = this.getX() - objective.getX();
	    int deltaY = this.getY() - objective.getY();
	    return Math.sqrt(Math.pow(deltaX, 2) + Math.pow(deltaY, 2));
    }
}

public class Initialize{
    private Node[] nodes;
    private double[][] distance;
    private int numOfCity;

    public Initialize(String filepath){
    	try{
		    BufferedReader in = new BufferedReader(new FileReader(filepath));
		    String s;
		    for(int i = 0; i < 5; i++){
			    in.readLine();
		    }
		    s = in.readLine();
		    numOfCity = Integer.parseInt(s.split(" : ")[1]);
		    in.readLine();
		    in.readLine();
		    
		    this.nodes = new Node[this.numOfCity];
		    this.distance = new double[this.numOfCity][this.numOfCity];
		    
		    for(int i = 0; i < numOfCity; i++){
			    s = in.readLine();
			    String[] splited = s.split(" ");
			    nodes[i] = new Node(Integer.parseInt(splited[0]),
					    Integer.parseInt(splited[1]),
					    Integer.parseInt(splited[2]));
		    }
	    } catch(FileNotFoundException e){
    		System.err.println("File not found");
    		System.exit(1);
	    }catch(IOException e2){
		    System.err.println("File Info read error");
		    System.exit(1);
	    }
	    
        for(int i = 0; i < numOfCity; i++){
            for(int j = 0; j < numOfCity; j++){
                distance[i][j] = nodes[i].getDistance(nodes[j]);
            }
            //distance[i][i]는 따로 처리 안함
        }
    }
    
    public Node getNode(int index){
    	return nodes[index];
	}
	public Node[] getNodes(){
    	return nodes;
	}
	public double getDistance(Node subject, Node object){
		return distance[subject.getIndex()][object.getIndex()];
	}
	public double getDistance(int subjectIndex, int objectIndex){
		return distance[subjectIndex][objectIndex];
	}
	public double[][] getDistances(){
		return distance;
	}
	public int getNumOfCity(){
		return numOfCity;
	}
	
    private int getStartIndex(Node[] randomPath){
	    int start = 0;
	    double MAX = 0;
	    for(int i = 0; i < numOfCity; i++){
		    for(int j = 0; j < numOfCity; j++){
			    if(distance[i][j] > MAX){
				    MAX = distance[i][j];
				    start = i;
			    }
		    }
	    }
	    return start;
    }
    public void RandomPath(){
        Node[] randomPath = new Node[numOfCity];
        boolean[] isNoded = new boolean[numOfCity];
	    Arrays.fill(isNoded, Boolean.TRUE);
	    int start = getStartIndex(randomPath);
	    randomPath[0] = nodes[start];
		isNoded[start] = false;
		
        for(int i = 1; i < numOfCity; i++){
            double min = 10000.0;
            int index = 0;
            for(int j = 0; j < numOfCity; j++){
            	start = randomPath[i - 1].getIndex();
				if((distance[start][j] < min) && isNoded[j] && (start != j)){
					index = j;
					min = distance[start][j];
				}
            }
            randomPath[i] = nodes[index];
	        isNoded[index] = false;
        }
        nodes = randomPath;
    }
}