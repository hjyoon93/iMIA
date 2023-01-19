package edu.gmu.c4i.dalnim.sbn.data;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.io.UncheckedIOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import unbbayes.prs.Graph;
import unbbayes.prs.bn.ProbabilisticNetwork;
import unbbayes.prs.sbn.RunnableSBNParameterLearning.NetworkStructureDataTransferObject;
import unbbayes.simulation.montecarlo.io.MonteCarloIO;
import unbbayes.simulation.montecarlo.sampling.IMonteCarloSampling;
import unbbayes.simulation.montecarlo.sampling.MatrixMonteCarloSampling;

/**
 * This is the default implementation of {@link SBNSampler} which generates
 * sample data in a temporary file. It will use {@link MatrixMonteCarloSampling}
 * to generate samples from an existing network model.
 * 
 * @author Shou Matsumoto
 *
 * @see #setSampler(IMonteCarloSampling)
 */
public class TemporaryFileSBNSampler implements SBNSampler {

	private static Logger logger = LoggerFactory.getLogger(TemporaryFileSBNSampler.class);

	private IMonteCarloSampling sampler;

	private File outputLocation;

	private NetworkStructureDataTransferObject netToSample;

	private int dataSize = 100;

	private long elapsedTimeMillis = Integer.MAX_VALUE;

	/**
	 * Default constructor is protected to allow inheritance but disallow public
	 * access. Use {@link #getInstance()} for public access.
	 */
	protected TemporaryFileSBNSampler() {
		// Auto-generated constructor stub
	}

	/**
	 * @return {@link #getInstance(NetworkStructureDataTransferObject, File)} with
	 *         {@link File} (i.e., the second argument) being null.
	 */
	public static SBNSampler getInstance(NetworkStructureDataTransferObject netToSample) {
		return getInstance(netToSample, null);
	}

	/**
	 * Default constructor method initializing fields.
	 * 
	 * @param netToSample    : the network to sample. The generated data will convey
	 *                       the variables and the probability distribution in this
	 *                       network.
	 * @param outputLocation : the location to store the data. If null, a new
	 *                       temporary file will be generated.
	 * 
	 * @return a new instance of {@link TemporaryFileSBNSampler}
	 * 
	 * @see #setNetToSample(NetworkStructureDataTransferObject)
	 * @see #getNetToSample()
	 */
	public static SBNSampler getInstance(NetworkStructureDataTransferObject netToSample, File outputLocation) {
		TemporaryFileSBNSampler ret = new TemporaryFileSBNSampler();
		ret.setNetToSample(netToSample);
		ret.setOutputLocation(outputLocation);
		return ret;
	}

	/**
	 * Generate the data. Use {@link #getData()} to access its content. The data
	 * will be stored at {@link #getOutputLocation()}. If
	 * {@link #setOutputLocation(File)} is set to null, a new temporary file will be
	 * created.
	 */
	@Override
	public void run() {
		logger.debug("Starting the SBN sampler...");

		NetworkStructureDataTransferObject netDTO = getNetToSample();
		logger.debug("Extracted the network to sample: {}", ((netDTO != null) ? netDTO.getNetwork() : null));
		if (netDTO == null || !(netDTO.getNetwork() instanceof ProbabilisticNetwork)) {
			throw new IllegalArgumentException("Invalid network was provided. Expected an instance of '"
					+ ProbabilisticNetwork.class + "'. Obtained: "
					+ ((netDTO != null && netDTO.getNetwork() != null) ? netDTO.getNetwork().getClass() : null));
		}

		File file = getOutputLocation();
		if (file == null) {
			logger.debug("No output file was provided. Generating a temporary file...");
			try {
				file = File.createTempFile(getClass().getName(), ".samples.txt");
			} catch (IOException e) {
				throw new UncheckedIOException("Failed to create a temporary file to store the samples.", e);
			}
			setOutputLocation(file);
		}
		logger.debug("Output file set to '{}'", file);

		IMonteCarloSampling monteCarlo = getSampler();
		logger.debug("Extracted the sampler to use: {}", monteCarlo);
		if (monteCarlo == null) {
			throw new NullPointerException("No monte-carlo sampler implementation was provided.");
		}

		logger.info("Starting the monte-carlo simulation...");
		monteCarlo.start((ProbabilisticNetwork) netDTO.getNetwork(), getDataSize(), getElapsedTimeMillis());
		logger.info("Completed the monte-carlo simulation.");

		logger.info("Saving the samples to file: {}", file);
		try {
			MonteCarloIO io = new MonteCarloIO(monteCarlo.getSampledStatesMatrix(),
					monteCarlo.getSamplingNodeOrderQueue());
			io.setFile(file);
			io.makeFile(monteCarlo.getSamplingNodeOrderQueue());
		} catch (IOException e) {
			throw new UncheckedIOException("Failed to save the samples to file: " + file, e);
		}
	}

	/**
	 * Retrieves the data generated at {@link #run()}. The file at
	 * {@link #getOutputLocation()} will be loaded.
	 */
	@Override
	public InputStream getData() {

		// retrieve the data file
		File file = getOutputLocation();

		logger.debug("Retrieving input stream of sampled data from file: {}", file);

		// if data file is null, #run() was not executed.
		if (file == null) {
			throw new NullPointerException("Data file was null. The method 'run()' should be invoked first.");
		}

		// just return a stream to read this file
		try {
			return new FileInputStream(file);
		} catch (FileNotFoundException e) {
			throw new IllegalStateException(
					"No data was found at '" + file + "'. The method 'run()' should be invoked first.", e);
		}
	}

	/**
	 * @return the sampler to be used to generate the data. If null, a new object of
	 *         {@link MatrixMonteCarloSampling} will be instantiated.
	 */
	@Override
	public synchronized IMonteCarloSampling getSampler() {
		if (sampler == null) {
			sampler = new MatrixMonteCarloSampling();
		}
		return sampler;
	}

	/**
	 * @param sampler : the sampler to be used to generate the data. If null, a new
	 *                object of {@link MatrixMonteCarloSampling} will be
	 *                instantiated.
	 */
	@Override
	public synchronized void setSampler(IMonteCarloSampling sampler) {
		this.sampler = sampler;
	}

	/**
	 * @return the location of the data generated in {@link #run()} and to be
	 *         accessed with {@link #getData()}. If null, a new temporary file
	 *         should be created.
	 */
	public File getOutputLocation() {
		return outputLocation;
	}

	/**
	 * @param outputLocation : the location of the data generated in {@link #run()}
	 *                       and to be accessed with {@link #getData()}. If null, a
	 *                       new temporary file should be created.
	 */
	public void setOutputLocation(File outputLocation) {
		this.outputLocation = outputLocation;
	}

	/**
	 * @return the network to sample at {@link #run()}. The generated data will
	 *         convey the variables and the probability distribution in this
	 *         network.
	 * 
	 * @see #setNetToSample(Graph)
	 */
	public NetworkStructureDataTransferObject getNetToSample() {
		return netToSample;
	}

	/**
	 * @param netToSample : the network to sample at {@link #run()}. The generated
	 *                    data will convey the variables and the probability
	 *                    distribution in this network.
	 * 
	 * @see #getNetToSample()
	 */
	public void setNetToSample(NetworkStructureDataTransferObject netToSample) {
		this.netToSample = netToSample;
	}

	/**
	 * @param dataSize : the number of samples to generate at {@link #run()}
	 */
	@Override
	public void setDataSize(int dataSize) {
		this.dataSize = dataSize;
	}

	/**
	 * @return the number of samples to generate at {@link #run()}
	 */
	public int getDataSize() {
		return dataSize;
	}

	/**
	 * @return milliseconds to stop sampling at {@link #run()}.
	 */
	public long getElapsedTimeMillis() {
		return elapsedTimeMillis;
	}

	/**
	 * @param elapsedTimeMillis : milliseconds to stop sampling at {@link #run()}.
	 */
	public void setElapsedTimeMillis(long elapsedTimeMillis) {
		this.elapsedTimeMillis = elapsedTimeMillis;
	}

}
