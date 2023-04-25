package edu.gmu.c4i.dalnim.sbn;

import unbbayes.prs.builder.IProbabilisticNetworkBuilder;
import unbbayes.prs.sbn.RunnableSBNParameterLearning.NetworkStructureDataTransferObject;
import unbbayes.util.random.IRandomNetworkGenerator;

/**
 * <p>
 * This is a miscellaneous class for experiments. It generates a random SBN
 * structure given arguments like max number of parents, number of states,
 * number of nodes, etc.
 * </p>
 * <p>
 * Additional arguments can be passed in the constructor as well.
 * </p>
 * 
 * @author Shou Matsumoto
 *
 * @see IProbabilisticNetworkBuilder
 * @see RandomSBNBuilderImpl
 */
public interface RandomSBNBuilder extends IRandomNetworkGenerator, NetworkStructureDataTransferObject {

	/**
	 * @param count : the magnitude of the Beta/Dirichlet distribution (i.e.,
	 *              virtual data counts).
	 * 
	 * @see unbbayes.io.CountCompatibleNetIO#DEFAULT_COUNT_TABLE_PREFIX
	 */
	void setTotalCounts(int count);

	/**
	 * @param minNumStates : the minimum number of states of nodes.
	 */
	public void setMinNumStates(int minNumStates);

	/**
	 * @param maxNumStates : the maximum number of states of nodes.
	 */
	public void setMaxNumStates(int maxNumStates);

	/**
	 * @param treeWidth : the maximum number of parents per node.
	 */
	public void setMaxTreeWidth(int treeWidth);

	/**
	 * @param numNodes : the number of nodes to be created in the network.
	 */
	public void setNumNodes(int numNodes);

}
