package createAlephFiles;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.Scanner;

public class CreateFiles {
	
	static int NRESIDUES = 134;
	static int[] ALL_RES = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 
		15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
		32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48,
		49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65,
		66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82,
		83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99,
		100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113,
		114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127,
		128, 129, 130, 131, 132, 133};
	static int[] CDR_RES = {26,27,28,29,30,31,32,33,34,35,36,53,54,55,56,57
		,58,59,60,61,62,63,64,103,104,105,106,107,108,109,110,111,112,113,
		114,115,116,117,118,119,120,121,122,123};
	static int[] FR_RES = {1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,124,125,126,127,128,129,130,131,132,133,134};
	static int[] OUTSIDE_RES = {33 ,35, 37, 39, 41, 42, 44, 46, 48, 50, 52, 65, 67, 68, 69,
	                            99, 101, 103, 105, 123, 125, 127, 129};
	static int[] residues = ALL_RES;

	
	
	public static void main(String[] args) throws IOException{
		if(args.length < 3){
			System.out.println("Usage: CreateFiles <pos> <neg> out [consult]");
			System.exit(0);
		} 
		
		String posFileName = args[0];
		String negFileName = args[1];
		String outPath = args[2];
		
		Scanner posScan = new Scanner(new File(posFileName));
		Scanner negScan = new Scanner(new File(negFileName));
		
		FileWriter backFW = new FileWriter(outPath + ".b");
		FileWriter posFW = new FileWriter(outPath + ".f");
		FileWriter negFW = new FileWriter(outPath + ".n");
		
		for(int i = 3; i < args.length; i++){
			backFW.write(":- consult('" + args[i] + "').\n");
		}
		
		backFW.write("\n\n");
		
		
		
		//determinations, modeb
		for(int i = 0; i < NRESIDUES; i++){
			int res = i+1;
			if(Arrays.binarySearch(residues, res) >= 0)
				backFW.write(":- modeb(*, resAt" + res + "(+sequence, -residue)).\n");
		}
		
		backFW.write("\n\n");
		
		for(int i = 0; i < NRESIDUES; i++){
			int res = i+1;
			if(Arrays.binarySearch(residues, res) >= 0)
				backFW.write(":- determination(accept/1, resAt" + res + "/2).\n");
		}
		
		backFW.write("\n\n");
		
		int nPos, nNeg;
		nPos = nNeg = 0;
		
		while(posScan.hasNextLine()){
			String line = posScan.nextLine();
			if(line.length() < NRESIDUES){
				continue;
			}
			nPos++;
			String name = "p" + nPos;

			posFW.write("accept(" + name + ").\n");
			writeToBackGround(line, name, backFW);
		}
		
		while(negScan.hasNextLine()) {
			String line = negScan.nextLine();
			if(line.length() < NRESIDUES){
				continue;
			}
			nNeg++;
			String name = "n" + nNeg;
			
			negFW.write("accept(" + name + ").\n");
			writeToBackGround(line, name, backFW);			
		}
		
		posScan.close();
		negScan.close();
		backFW.close();
		posFW.close();
		negFW.close();
		
	}
	
	public static void writeToBackGround(String s, String name, FileWriter backFW) throws IOException{
		backFW.write("\n");
		backFW.write("sequence(" + name + ").\n");
		for(int i = 0; i < s.length(); i++){
			char c = s.charAt(i);
			
			int res = i+1;
			if(Arrays.binarySearch(residues, res) >= 0)
				backFW.write("resAt" + res + "(" + name + ", " + resName(c) + ").\n");
			
		}
	}
	
	public static String resName (char c){
		if(c == '-'){
			return "gap";
		}
		else{
			
			return Character.toString(c).toLowerCase();
		}
	}

}
