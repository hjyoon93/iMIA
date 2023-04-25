package edu.gmu.c4i.dalnim.typedb2sbn;

import java.io.File;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Options;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Main entrypoint of the TypeDB2SBN tool
 * 
 * @author shou
 *
 */
public class Main {

	private static Logger logger = LoggerFactory.getLogger(Main.class);

	public Main() {
		// Auto-generated constructor stub
	}

	/**
	 * @param args :
	 * 
	 *             <pre>
	 * --help,	-h :	Prints this help. See application.properties for more configurable parameters.
	 * --url,		-u :	Address of TypeDB. Default is "localhost:1729"
	 * --database,	-d :	Name of database in TypeDB to open a session. Default is "BPMN"
	 * --uid,		-i :	UID of concept model element to query (regex supported). E.g., "https://camunda.org/examples/#.*"
	 * --output,	-o :	The output NET file. Default is "structure.net"
	 *             </pre>
	 */
	public static void main(String[] args) throws Exception {

		// set up the command line arguments
		Options options = new Options();
		options.addOption("h", "help", false,
				"Prints this help. See application.properties for more configurable parameters.");
		options.addOption("u", "url", true, "Address of TypeDB. Default is \"localhost:1729\"");
		options.addOption("d", "database", true, "Name of database in TypeDB to open a session. Default is \"demo\"");
		options.addOption("i", "uid", true,
				"UID of concept model element to query (regex supported). E.g., \"https://camunda.org/examples/#.*\"");
		options.addOption("o", "output", true, "The output NET file. Default is \"structure.net\"");

		// parse the command line arguments
		logger.debug("Reading the command line arguments.");
		CommandLine cmd = new DefaultParser().parse(options, args);

		// print help if argument is set
		if (cmd.hasOption('h')) {
			new HelpFormatter().printHelp("TypeDB2SBN", options);
			return;
		}

		// the decoder to run
		Decoder writer = Decoder.getDefaultDecoder();

		// read URL
		if (cmd.hasOption("url")) {
			writer.setTypeDBAddress(cmd.getOptionValue("url"));
		}

		// read database name
		if (cmd.hasOption("database")) {
			writer.setDatabaseName(cmd.getOptionValue("database"));
		}

		// read uid of definitions to query
		if (cmd.hasOption("uid")) {
			writer.setRootUID(cmd.getOptionValue("uid"));
		}

		// read the output location
		File outputFile = new File(cmd.getOptionValue("output",
				// default is 'structure.net'
				"structure.net")).getAbsoluteFile();
		logger.debug("Output location is: {}", outputFile);

		// Generate the SBN structure...
		logger.info("Starting the process...");
		writer.saveSBNFile(outputFile);
		logger.info("Finished the process.");

	}

}
