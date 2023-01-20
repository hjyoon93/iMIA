package edu.gmu.c4i.dalnim.sbn;

import java.io.File;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.DefaultParser;
import org.apache.commons.cli.HelpFormatter;
import org.apache.commons.cli.Options;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * This is the main entry point (CLI) of
 * {@link RandomSBNParameterLearningDriver}
 * 
 * @author Shou Matsumoto
 *
 * @see RandomSBNParameterLearningDriverImpl
 */
public class Main {

	public static final int DEFAULT_NUM_NODES = 600;
	public static final int DEFAULT_NUM_STATES = 2;
	public static final int DEFAULT_TREEWIDTH = 15;
	public static final int DEFAULT_SAMPLE_SIZE = 100;
	public static final String DEFAULT_OUTPUT_DIRECTORY = "./output/";

	public static final String PARAM_NODES = "nodes";
	public static final String PARAM_STATES = "states";
	public static final String PARAM_TREEWIDTH = "treewidth";
	public static final String PARAM_DATASIZE = "datasize";
	public static final String PARAM_OUTPUT = "output";

	private static Logger logger = LoggerFactory.getLogger(Main.class);

	/**
	 * Auto-generated constructor stub
	 */
	public Main() {
		// Auto-generated constructor stub
	}

	/**
	 * The CLI entrypoint of {@link RandomSBNParameterLearningDriverImpl}
	 * 
	 * @param args :
	 * 
	 *             <pre>
	 *  -d,--datasize <arg>    Number of data samples to generate (i.e., size of
	 *                         training data). Default is 100
	 *  -h,--help              Prints the help.
	 *  -n,--nodes <arg>       Number of nodes. Default is 600
	 *  -o,--output <arg>      The output folder where the random SBN structure,
	 *                         the training data, and the trained SBN will be
	 *                         stored. Default is: "./output/"
	 *  -s,--states <arg>      Number of states. Default is 2
	 *  -t,--treewidth <arg>   The treewidth (number of parents per node).
	 *                         Default is 15
	 *             </pre>
	 */
	public static void main(String[] args) throws Exception {

		// set up the command line arguments
		Options options = new Options();
		options.addOption("h", "help", false, "Prints this help.");

		options.addOption("n", PARAM_NODES, true, "Number of nodes. Default is " + DEFAULT_NUM_NODES);
		options.addOption("s", PARAM_STATES, true, "Number of states. Default is " + DEFAULT_NUM_STATES);
		options.addOption("t", PARAM_TREEWIDTH, true,
				"The treewidth (number of parents per node). Default is " + DEFAULT_TREEWIDTH);
		options.addOption("d", PARAM_DATASIZE, true,
				"Number of data samples to generate (i.e., size of training data). Default is " + DEFAULT_SAMPLE_SIZE);

		options.addOption("o", PARAM_OUTPUT, true,
				"The output folder where the random SBN structure, the training data, and the trained SBN will be stored. Default is: \""
						+ DEFAULT_OUTPUT_DIRECTORY + "\"");

		// parse the command line arguments
		logger.debug("Reading the command line arguments.");
		CommandLine cmd = new DefaultParser().parse(options, args);

		// print help if argument is set
		if (cmd.hasOption('h')) {
			new HelpFormatter().printHelp("java -jar RandomSBNTraining-<VERSION>-jar-with-dependencies.jar [OPTIONS]",
					options);
			return;
		}

		// the object to setup
		RandomSBNParameterLearningDriver driver = RandomSBNParameterLearningDriverImpl.getInstance();

		// number of nodes in the SBN to generate
		if (cmd.hasOption(PARAM_NODES)) {
			String value = cmd.getOptionValue(PARAM_NODES);
			logger.debug("Setting the number of nodes to {}", value);
			driver.setNumNodes(Integer.parseInt(value));
		} else {
			logger.debug("Using default number of nodes: {}", DEFAULT_NUM_NODES);
			driver.setNumNodes(DEFAULT_NUM_NODES);
		}

		// number of states of nodes
		if (cmd.hasOption(PARAM_STATES)) {
			String value = cmd.getOptionValue(PARAM_STATES);
			logger.debug("Setting the number of states to {}", value);
			driver.setNumStates(Integer.parseInt(value));
		} else {
			logger.debug("Using default number of states: {}", DEFAULT_NUM_STATES);
			driver.setNumStates(DEFAULT_NUM_STATES);
		}

		// treewidth (number of parents per node)
		if (cmd.hasOption(PARAM_TREEWIDTH)) {
			String value = cmd.getOptionValue(PARAM_TREEWIDTH);
			logger.debug("Setting the treewidth to {}", value);
			driver.setTreeWidth(Integer.parseInt(value));
		} else {
			logger.debug("Using default treewidth: {}", DEFAULT_TREEWIDTH);
			driver.setTreeWidth(DEFAULT_TREEWIDTH);
		}

		// the number of samples (size of training data)
		if (cmd.hasOption(PARAM_DATASIZE)) {
			String value = cmd.getOptionValue(PARAM_DATASIZE);
			logger.debug("Setting the data size to {}", value);
			driver.setDataCounts(Integer.parseInt(value));
		} else {
			logger.debug("Using default data sample size: {}", DEFAULT_SAMPLE_SIZE);
			driver.setDataCounts(DEFAULT_SAMPLE_SIZE);
		}

		// the directory where the output files will be saved to
		File outputDir = null;
		if (cmd.hasOption(PARAM_OUTPUT)) {
			outputDir = new File(cmd.getOptionValue(PARAM_OUTPUT));
		} else {
			outputDir = new File(DEFAULT_OUTPUT_DIRECTORY);
		}
		logger.debug("Setting the output directory to '{}'", outputDir);
		driver.setDataFile(new File(outputDir, "trainingData.txt"));
		driver.setInitialNetFile(new File(outputDir, "untrained.net"));
		driver.setTrainedNetFile(new File(outputDir, "trained.net"));

		logger.info("Starting the driver.");
		driver.run();
		logger.info("Process completed.");

	}

}
