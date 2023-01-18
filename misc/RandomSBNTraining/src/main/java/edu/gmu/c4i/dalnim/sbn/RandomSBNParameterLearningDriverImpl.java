package edu.gmu.c4i.dalnim.sbn;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import edu.gmu.c4i.dalnim.sbn.data.SBNSampler;
import edu.gmu.c4i.dalnim.sbn.data.SBNSamplerImpl;
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

	/**
	 * Default constructor is protected to avoid public access, but to allow quick
	 * inheritance. Use {@link #getInstance()} for public access.
	 */
	protected RandomSBNParameterLearningDriverImpl() {
		// TODO Auto-generated constructor stub
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

		SBNSampler sampler = SBNSamplerImpl.getInstance();
		ret.setDataGenerator(sampler);

		ret.setParameterLearningRunner(RunnableSBNParameterLearning.getInstance(sbnBuilder, sampler));

		return ret;
	}

	/**
	 * @return the parameterLearningRunner
	 */
	@Override
	public RunnableSBNParameterLearning getParameterLearningRunner() {
		return parameterLearningRunner;
	}

	/**
	 * @param parameterLearningRunner the parameterLearningRunner to set
	 */
	@Override
	public void setParameterLearningRunner(RunnableSBNParameterLearning parameterLearningRunner) {
		this.parameterLearningRunner = parameterLearningRunner;
	}

	/**
	 * @return the sbnBuilder
	 */
	@Override
	public RandomSBNBuilder getSBNBuilder() {
		return sbnBuilder;
	}

	/**
	 * @param sbnBuilder the sbnBuilder to set
	 */
	@Override
	public void setSBNBuilder(RandomSBNBuilder sbnBuilder) {
		this.sbnBuilder = sbnBuilder;
	}

	/**
	 * @return the dataGenerator
	 */
	public SBNSampler getDataGenerator() {
		return dataGenerator;
	}

	/**
	 * @param dataGenerator the dataGenerator to set
	 */
	public void setDataGenerator(SBNSampler dataGenerator) {
		this.dataGenerator = dataGenerator;
	}

	@Override
	public void run() {
		logger.debug("Starting the experiment...");
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException("Not implemented yet");
	}

}
