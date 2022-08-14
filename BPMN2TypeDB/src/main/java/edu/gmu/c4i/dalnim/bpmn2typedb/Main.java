package edu.gmu.c4i.dalnim.bpmn2typedb;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.file.Files;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Options;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import edu.gmu.c4i.dalnim.bpmn2typedb.encoder.Encoder;
import edu.gmu.c4i.dalnim.util.ApplicationProperties;

/**
 * Main entrypoint of the BPMN2TypeDB tool
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
	 * --help,  -h :	Prints this help. See application.properties for more configurable parameters.
	 * --input, -i :	The input BPMN file. 
	 * 					Will be ignored if "--url" is present.
	 * 					Default is "input.bpmn"
	 * 
	 * --output, -o :	Output directory. 
	 * 					If running with "--url", then this program will output a BPMN file read from TypeDB.
	 * 					If not running with "--url", then this will be the folder to write 
	 * 					TypeQL schema (schema.tql) and data (data.tql).
	 * 					Default is "./output/"
	 *             </pre>
	 */
	public static void main(String[] args) throws Exception {

		// set up the command line arguments
		Options options = new Options();
		options.addOption("h", "help", false, "Prints this help. See application.properties for more configurable parameters.");
		options.addOption("i", "input", true, "The input BPMN file. Default is \"input.bpmn\"");
		options.addOption("o", "output", true, "Output directory. Default is \"./output/\"");

		// parse the command line arguments
		logger.debug("Reading the command line arguments.");
		CommandLine cmd = new DefaultParser().parse(options, args);

		// print help if argument is set
		if (cmd.hasOption('h')) {
			new HelpFormatter().printHelp("sparql.http.request", options);
			return;
		}

		// read the input location
		File inputFile = new File(cmd.getOptionValue("input", "input.bpmn")).getAbsoluteFile();
		logger.debug("Input file location is: {}", inputFile);
		if (!inputFile.exists()) {
			throw new IOException("Input file does not exist or cannot be accessed: " + inputFile);
		}

		// read the output location
		File outputDir = new File(cmd.getOptionValue("output", "./output/")).getAbsoluteFile();
		logger.debug("Output directory location is: {}", outputDir);

		// the encoder to run
		Encoder encoder = Encoder.getDefaultEncoder();

		// load the input file
		try (InputStream inputStream = new BufferedInputStream(new FileInputStream(inputFile))) {
			encoder.loadInput(inputStream);
		}

		// read some properties from application.properties
		ApplicationProperties properties = ApplicationProperties.getInstance();
		// the name of the schema file to write
		String schemaFileName = properties.getProperty(Main.class.getName() + ".schemaFileName",
				// default is 'schema.tql'
				"schema.tql");
		// the name of the data file to write
		String dataFileName = properties.getProperty(Main.class.getName() + ".dataFileName",
				// default is 'data.tql'
				"data.tql");

		// Generate the outputs...

		// Make sure the output directory exists.
		Files.createDirectories(outputDir.toPath());

		// Generate the schema file...
		try (OutputStream schemaOutput = new BufferedOutputStream(
				// create the schema TypeQL inside the output directory
				new FileOutputStream(new File(outputDir, schemaFileName)))) {
			encoder.encodeSchema(schemaOutput);
		}
		// generate the data file
		try (OutputStream dataOutput = new BufferedOutputStream(
				// create the data TypeQL inside the output directory
				new FileOutputStream(new File(outputDir, dataFileName)))) {
			encoder.encodeData(dataOutput);
		}
	}

}
