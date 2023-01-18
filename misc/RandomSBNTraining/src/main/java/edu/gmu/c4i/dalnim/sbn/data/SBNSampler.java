package edu.gmu.c4i.dalnim.sbn.data;

import unbbayes.prs.sbn.RunnableSBNParameterLearning.TrainingDataTransferObject;
import unbbayes.simulation.montecarlo.sampling.IMonteCarloSampling;

/**
 * 
 * @author smats
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

}