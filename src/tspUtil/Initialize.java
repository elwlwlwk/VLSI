package tspUtil;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.lang.Math;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

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
	private static Initialize instance =null;
    private Node[] nodes;
    private double[][] distance;
    private int numOfCity;
    private int[] path;
    
    public static void getfile(String filename){
		instance = new Initialize(filename);
	}
    public static Initialize getInstance(){
		return instance;
	}
	

    public Initialize(String filepath){
	    String s;
	    int i = 0;
	    List<Node> tempNodes = new ArrayList<Node>();
    	try{
		    BufferedReader in = new BufferedReader(new FileReader(filepath));
		    s = in.readLine();
		    while(s != null) {
			    String[] splited = s.split(" ");
			    tempNodes.add(new Node(Integer.parseInt(splited[0]),
					    Integer.parseInt(splited[1]),
					    Integer.parseInt(splited[2])));
//			    nodes[i++] = new Node(Integer.parseInt(splited[0]),
//					    Integer.parseInt(splited[1]),
//					    Integer.parseInt(splited[2]));
			    s = in.readLine();
		    }
	    } catch(FileNotFoundException e){
    		System.err.println("File not found");
    		System.exit(1);
	    }catch(IOException e2){
		    System.err.println("File Info read error");
		    System.exit(1);
	    }
	    this.numOfCity = tempNodes.size();
	    
	    //Initialize fields
	    path = new int[numOfCity];
	    nodes = new Node[numOfCity];
	    nodes = tempNodes.toArray(nodes);
	    distance = new double[numOfCity][];
     
	    for( i = 0; i < numOfCity; i++){
        	distance[i] = new double[numOfCity];
            for(int j = 0; j < numOfCity; j++){
                distance[i][j] = nodes[i].getDistance(nodes[j]);
            }
            //distance[i][i]는 따로 처리 안함
        }
        this.RandomPath();
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
	
	public int[] getPath(){
	return path;
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
	    this.path[0]=nodes[start].getIndex();
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
            this.path[i]=nodes[index].getIndex();
	        isNoded[index] = false;
        }
        nodes = randomPath;
    }
}
