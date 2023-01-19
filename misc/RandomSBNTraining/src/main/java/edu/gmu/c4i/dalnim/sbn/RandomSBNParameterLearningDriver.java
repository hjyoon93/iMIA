package edu.gmu.c4i.dalnim.sbn;

import java.io.File;

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

	/**
	 * @param dataCounts the dataCounts to set
	 */
	public void setDataCounts(int dataCounts);

	/**
	 * @param numStates the numStates to set
	 */
	public void setNumStates(int numStates);

	/**
	 * @param treeWidth the treeWidth to set
	 */
	public void setTreeWidth(int treeWidth);

	/**
	 * @return the numNodes
	 */
	public int getNumNodes();

	/**
	 * @param numNodes the numNodes to set
	 */
	public void setNumNodes(int numNodes);

	/**
	 * @param initialNetFile the initialNetFile to set
	 */
	public void setInitialNetFile(File initialNetFile);

	/**
	 * @param trainedNetFile the trainedNetFile to set
	 */
	public void setTrainedNetFile(File trainedNetFile);

	/**
	 * @param dataFile the dataFile to set
	 */
	public void setDataFile(File dataFile);

}