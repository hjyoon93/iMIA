package edu.gmu.dalnim;

/**
 * Main entrypoint of the BPMN2TypeDB tool
 * 
 * @author shou
 *
 */
public class Main {

	public Main() {
		// Auto-generated constructor stub
	}

	/**
	 * @param args :
	 * 
	 *             <pre>
	 * --db, -d URL :	URL of TypeDB database to load. 
	 * 					If this parameter is specified, the program will read a 
	 * 					TypeDB database from a URL and saves the loaded BPMN process to a BPMN2 file. 
	 * 					If not specified, then the program will run in BPMN to TypeQL file mode 
	 * 					(i.e., it reads a BPMN and saves TypeQL script files).
	 * 
	 * --input, -i :	The input BPMN file. 
	 * 					Will be ignored if "--db" is present.
	 * 					Default is "input.bpmn"
	 * 
	 * --output, -o :	Output directory. 
	 * 					If running with "--db", then this program will output a BPMN file read from TypeDB.
	 * 					If not running with "--db", then this will be the folder to write 
	 * 					TypeQL schema (schema.tql) and data (data.tql).
	 * 					Default is "./output/"
	 * 
	 * --
	 *             </pre>
	 */
	public static void main(String[] args) throws Exception {
		throw new UnsupportedOperationException("Not implemented yet");
	}

}
