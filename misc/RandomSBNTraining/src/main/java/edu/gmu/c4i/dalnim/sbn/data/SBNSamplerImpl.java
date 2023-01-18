/**
 * 
 */
package edu.gmu.c4i.dalnim.sbn.data;

import java.io.InputStream;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import unbbayes.simulation.montecarlo.sampling.IMonteCarloSampling;

/**
 * @author smats
 *
 */
public class SBNSamplerImpl implements SBNSampler {

	private static Logger logger = LoggerFactory.getLogger(SBNSamplerImpl.class);	
	
	private IMonteCarloSampling sampler;
	
	/**
	 * 
	 */
	protected SBNSamplerImpl() {
		// TODO Auto-generated constructor stub
	}
	
	/**
	 * 
	 * @return
	 */
	public static SBNSampler getInstance() {
		return new SBNSamplerImpl();
	}

	@Override
	public InputStream getData() {
		logger.debug("Retrieving input stream of sampled data...");
		// TODO Auto-generated method stub
		return null;
	}
	
	/**
	 * @return the sampler
	 */
	@Override
	public IMonteCarloSampling getSampler() {
		return sampler;
	}

	/**
	 * @param sampler the sampler to set
	 */
	@Override
	public void setSampler(IMonteCarloSampling sampler) {
		this.sampler = sampler;
	}

	@Override
	public void run() {
		// TODO Auto-generated method stub
		
	}

}
