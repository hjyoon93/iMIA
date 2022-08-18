package edu.gmu.c4i.dalnim.typedb2bpmn;

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.OutputStream;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Options;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import edu.gmu.c4i.dalnim.typedb2bpmn.decoder.Decoder;
import edu.gmu.c4i.dalnim.util.ApplicationProperties;

/**
 * Main entrypoint of the TypeDB2BPMN tool
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
	 * --help,			-h :	Prints this help. See application.properties for more configurable parameters.
	 * --url,			-u :	Address of TypeDB. Default is "localhost:1729"
	 * --database,	-d :	Name of database in TypeDB to open a session. Default is "BPMN"
	 * --uid,			-i :	UID of BPMN project to query (regex supported). E.g., "https://camunda.org/examples/#.*"
	 * --output,		-o :	The output BPMN file. Default is "output.bpmn"
	 *             </pre>
	 */
	public static void main(String[] args) throws Exception {

		// set up the command line arguments
		Options options = new Options();
		options.addOption("h", "help", false,
				"Prints this help. See application.properties for more configurable parameters.");
		options.addOption("u", "url", true, "ddress of TypeDB. Default is \"localhost:1729\"");
		options.addOption("d", "database", true, "Name of database in TypeDB to open a session. Default is \"BPMN\"");
		options.addOption("i", "uid", true,
				"UID of BPMN project to query (regex supported). E.g., \"https://camunda.org/examples/#.*\"");
		options.addOption("o", "output", true, "The output BPMN file. Default is \"output.bpmn\"");

		// parse the command line arguments
		logger.debug("Reading the command line arguments.");
		CommandLine cmd = new DefaultParser().parse(options, args);

		// print help if argument is set
		if (cmd.hasOption('h')) {
			new HelpFormatter().printHelp("TypeDB2BPMN", options);
			return;
		}

		// TODO read other parameters

		// read some properties from application.properties
		ApplicationProperties properties = ApplicationProperties.getInstance();
		// The default name of the BPMN file to write
		String bpmnFileName = properties.getProperty(Main.class.getName() + ".BPMNFileName",
				// default is 'output.bpmn'
				"output.bpmn");

		// read the output location
		File outputFile = new File(cmd.getOptionValue("output", bpmnFileName)).getAbsoluteFile();
		logger.debug("Output location is: {}", outputFile);

		// the decoder to run
		Decoder decoder = Decoder.getDefaultDecoder();

		// Generate the BPMN file...
		try (OutputStream bpmnOutput = new BufferedOutputStream(new FileOutputStream(outputFile))) {
			logger.info("Starting the process...");
			decoder.saveBPMN(bpmnOutput);
			logger.info("Finished the process.");
		}

	}

}
