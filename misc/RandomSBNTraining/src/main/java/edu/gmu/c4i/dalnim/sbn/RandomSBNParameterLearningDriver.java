package edu.gmu.c4i.dalnim.sbn;

import unbbayes.prs.sbn.RunnableSBNParameterLearning;

/**
 * 
 * @author Shou Matsumoto
 *
 */
public interface RandomSBNParameterLearningDriver extends Runnable {

	/**
	 * @return the parameterLearningRunner
	 */
	RunnableSBNParameterLearning getParameterLearningRunner();

	/**
	 * @param parameterLearningRunner the parameterLearningRunner to set
	 */
	void setParameterLearningRunner(RunnableSBNParameterLearning parameterLearningRunner);

	/**
	 * @return the sbnBuilder
	 */
	RandomSBNBuilder getSBNBuilder();

	/**
	 * @param sbnBuilder the sbnBuilder to set
	 */
	void setSBNBuilder(RandomSBNBuilder sbnBuilder);

}