package edu.gmu.c4i.dalnim.sbn;

import java.io.File;
import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import edu.gmu.c4i.dalnim.sbn.data.SBNSampler;
import edu.gmu.c4i.dalnim.sbn.data.TemporaryFileSBNSampler;
import unbbayes.io.BaseIO;
import unbbayes.io.CountCompatibleNetIO;
import unbbayes.prs.Graph;
import unbbayes.prs.Node;
import unbbayes.prs.bn.PotentialTable;
import unbbayes.prs.bn.ProbabilisticNode;
import unbbayes.prs.bn.cpt.impl.UniformTableFunction;
import unbbayes.prs.sbn.RunnableSBNParameterLearning;

/**
 * Default implementation of {@link RandomSBNParameterLearningDriver}
 * 
 * @author Shou Matsumoto
 * 
 * @see RunnableSBNParameterLearning
 * @see RandomSBNBuilder
 * @see RandomSBNBuilderImpl
 *
 */
public class RandomSBNParameterLearningDriverImpl implements RandomSBNParameterLearningDriver {

	private static Logger logger = LoggerFactory.getLogger(RandomSBNParameterLearningDriverImpl.class);

	private RunnableSBNParameterLearning parameterLearningRunner;

	private RandomSBNBuilder sbnBuilder;

	private SBNSampler dataGenerator;

	private int dataCounts = 100;

	private int numStates = 2;

	private int treeWidth = 15;

	private int numNodes = 600;

	private BaseIO netIO;

	private File initialNetFile;

	private File trainedNetFile;

	private File dataFile;

	/**
	 * Default constructor is protected to avoid public access, but to allow quick
	 * inheritance. Use {@link #getInstance()} for public access.
	 */
	protected RandomSBNParameterLearningDriverImpl() {
		// Auto-generated constructor stub
	}

	/**
	 * Default public constructor method.
	 * 
	 * @return a new instance of {@link RandomSBNParameterLearningDriverImpl}
	 */
	public static RandomSBNParameterLearningDriver getInstance() {
		RandomSBNParameterLearningDriverImpl ret = new RandomSBNParameterLearningDriverImpl();

		RandomSBNBuilder sbnBuilder = RandomSBNBuilderImpl.getInstance();
		ret.setSBNBuilder(sbnBuilder);

		SBNSampler sampler = TemporaryFileSBNSampler.getInstance(sbnBuilder);
		ret.setDataGenerator(sampler);

		ret.setParameterLearningRunner(RunnableSBNParameterLearning.getInstance(sbnBuilder, sampler));

		return ret;
	}

	@Override
	public synchronized void run() {

		logger.debug("Starting the random SBN parameter learning experiment...");

		logger.debug("Setting up the SBN generator...");
		RandomSBNBuilder netBuilder = getSBNBuilder();
		logger.debug("Number of nodes = {}", getNumNodes());
		netBuilder.setNumNodes(getNumNodes());
		logger.debug("Number of states = {}", getNumStates());
		netBuilder.setMinNumStates(getNumStates());
		netBuilder.setMaxNumStates(getNumStates());
		logger.debug("Number of parents per node = {}", getTreeWidth());
		netBuilder.setMaxTreeWidth(getTreeWidth());
		logger.debug("Beta/Dirichlet parameter magnitude (i.e., data counts) = {}", getDataCounts());
		netBuilder.setTotalCounts(getDataCounts());
		logger.debug("Generating random SBN structure...");
		// Just run this method 1 time.
		netBuilder.generateRandomNet();

		logger.debug("Generating training data...");
		SBNSampler dataSampler = getDataGenerator();
		if (dataSampler instanceof TemporaryFileSBNSampler) {
			((TemporaryFileSBNSampler) dataSampler).setOutputLocation(getDataFile());
		}
		// Note: this data sampler is already associated with the builder,
		// so we don't need to specify the network to sample now.
		dataSampler.setDataSize(getDataCounts());
		// run will invoke RandomSBNBuilder#getNetwork
		dataSampler.run();

		if (dataSampler instanceof TemporaryFileSBNSampler) {
			File file = ((TemporaryFileSBNSampler) dataSampler).getOutputLocation();
			logger.debug("The training data was saved to: {}", file);
		}

		// force the SBN to have uniform distribution
		// (to make sure the trained network is easi
		logger.debug("Resetting the SBN parameters...");
		// use RandomSBNBuilderImpl to access the count tables
		RandomSBNBuilderImpl countTableHandler = (RandomSBNBuilderImpl) RandomSBNBuilderImpl.getInstance();
		// the network to reset
		Graph rawNet = netBuilder.getNetwork();
		// the function that will make the CPT uniform
		UniformTableFunction uniform = new UniformTableFunction();
		for (Node node : netBuilder.getNetwork().getNodes()) {
			// reset (delete) the count table
			countTableHandler.setCountTable(rawNet, node, null);
			// set the CPT uniform
			if (node instanceof ProbabilisticNode) {
				PotentialTable cpt = ((ProbabilisticNode) node).getProbabilityFunction();
				uniform.applyFunction(cpt);
			}
		}

		logger.debug("Saving the generated SBN structure to file: {}", getInitialNetFile());
		try {
			getNetIO().save(getInitialNetFile(), rawNet);
		} catch (IOException e) {
			logger.warn("Failed to save initial net file '{}'", getInitialNetFile(), e);
		}

		logger.debug("Starting the parameter learning process...");
		if (getParameterLearningRunner().getNetStructure() != netBuilder) {
			getParameterLearningRunner().setNetStructure(netBuilder);
		}
		if (getParameterLearningRunner().getTrainingData() != dataSampler) {
			getParameterLearningRunner().setTrainingData(dataSampler);
		}
		// actually run the parameter learning with the specified network structure and
		// data
		getParameterLearningRunner().run();

		logger.debug("Saving the trained SBN to file: {}", getTrainedNetFile());
		try {
			getNetIO().save(getTrainedNetFile(), getParameterLearningRunner().getTrainedNet());
		} catch (IOException e) {
			logger.warn("Failed to save initial net file '{}'", getInitialNetFile(), e);
		}

		logger.debug("The experiment has completed.");
	}

	/**
	 * @return the parameterLearningRunner
	 */
	@Override
	public synchronized RunnableSBNParameterLearning getParameterLearningRunner() {
		return parameterLearningRunner;
	}

	/**
	 * @param parameterLearningRunner the parameterLearningRunner to set
	 */
	@Override
	public synchronized void setParameterLearningRunner(RunnableSBNParameterLearning parameterLearningRunner) {
		this.parameterLearningRunner = parameterLearningRunner;
	}

	/**
	 * @return the sbnBuilder
	 */
	@Override
	public synchronized RandomSBNBuilder getSBNBuilder() {
		return sbnBuilder;
	}

	/**
	 * @param sbnBuilder the sbnBuilder to set
	 */
	@Override
	public synchronized void setSBNBuilder(RandomSBNBuilder sbnBuilder) {
		this.sbnBuilder = sbnBuilder;
	}

	/**
	 * @return the dataGenerator
	 */
	public synchronized SBNSampler getDataGenerator() {
		return dataGenerator;
	}

	/**
	 * @param dataGenerator the dataGenerator to set
	 */
	public synchronized void setDataGenerator(SBNSampler dataGenerator) {
		this.dataGenerator = dataGenerator;
	}

	/**
	 * @return the dataCounts
	 */
	public int getDataCounts() {
		return dataCounts;
	}

	/**
	 * @param dataCounts the dataCounts to set
	 */
	public void setDataCounts(int dataCounts) {
		this.dataCounts = dataCounts;
	}

	/**
	 * @return the numStates
	 */
	public int getNumStates() {
		return numStates;
	}

	/**
	 * @param numStates the numStates to set
	 */
	public void setNumStates(int numStates) {
		this.numStates = numStates;
	}

	/**
	 * @return the treeWidth
	 */
	public int getTreeWidth() {
		return treeWidth;
	}

	/**
	 * @param treeWidth the treeWidth to set
	 */
	public void setTreeWidth(int treeWidth) {
		this.treeWidth = treeWidth;
	}

	/**
	 * @return the numNodes
	 */
	public int getNumNodes() {
		return numNodes;
	}

	/**
	 * @param numNodes the numNodes to set
	 */
	public void setNumNodes(int numNodes) {
		this.numNodes = numNodes;
	}

	/**
	 * @return the netIO
	 */
	public synchronized BaseIO getNetIO() {
		if (netIO == null) {
			netIO = new CountCompatibleNetIO();
		}
		return netIO;
	}

	/**
	 * @param netIO the netIO to set
	 */
	public synchronized void setNetIO(BaseIO netIO) {
		this.netIO = netIO;
	}

	/**
	 * @return the initialNetFile
	 */
	public synchronized File getInitialNetFile() {
		if (initialNetFile == null) {
			initialNetFile = new File("./netStructure.net");
		}
		return initialNetFile;
	}

	/**
	 * @param initialNetFile the initialNetFile to set
	 */
	public synchronized void setInitialNetFile(File initialNetFile) {
		this.initialNetFile = initialNetFile;
	}

	/**
	 * @return the trainedNetFile
	 */
	public synchronized File getTrainedNetFile() {
		if (trainedNetFile == null) {
			trainedNetFile = new File("./trained.net");
		}
		return trainedNetFile;
	}

	/**
	 * @param trainedNetFile the trainedNetFile to set
	 */
	public synchronized void setTrainedNetFile(File trainedNetFile) {
		this.trainedNetFile = trainedNetFile;
	}

	/**
	 * @return the dataFile
	 */
	public synchronized File getDataFile() {
		if (dataFile == null) {
			dataFile = new File("./trainingData.txt");
		}
		return dataFile;
	}

	/**
	 * @param dataFile the dataFile to set
	 */
	public synchronized void setDataFile(File dataFile) {
		this.dataFile = dataFile;
	}

}
