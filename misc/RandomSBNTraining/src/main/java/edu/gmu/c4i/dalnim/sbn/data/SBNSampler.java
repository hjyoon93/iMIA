package edu.gmu.c4i.dalnim.sbn.data;

import unbbayes.prs.sbn.RunnableSBNParameterLearning.TrainingDataTransferObject;
import unbbayes.simulation.montecarlo.sampling.IMonteCarloSampling;

/**
 * 
 * This is a common interface for
 * 
 * {@link #run()} will generate samples. {@link #getData()} can be used to
 * access the generated samples.
 * 
 * @author Shou Matsumoto
 *
 */
public interface SBNSampler extends TrainingDataTransferObject, Runnable {

	/**
	 * @return the sampler
	 */
	IMonteCarloSampling getSampler();

	/**
	 * @param sampler the sampler to set
	 */
	void setSampler(IMonteCarloSampling sampler);
	
	/**
	 * @param dataSize : the number of samples to generate.
	 */
	public void setDataSize(int dataSize);


}