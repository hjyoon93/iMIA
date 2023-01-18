package edu.gmu.c4i.dalnim.sbn;

import unbbayes.prs.builder.IProbabilisticNetworkBuilder;
import unbbayes.prs.sbn.RunnableSBNParameterLearning.NetworkStructureDataTransferObject;

/**
 * <p>
 * This is a miscellaneous class for experiments. It generates a random SBN
 * structure given arguments like max number of parents, number of states
 * (controlled with
 * {@link #setProbabilisticNodeBuilder(unbbayes.prs.builder.INodeBuilder)}), and
 * number of nodes.
 * </p>
 * <p>
 * Additional arguments can be passed in the constructor as well.
 * </p>
 * <p>
 * The following sub-builders will be ignored:
 * </p>
 * <ul>
 * <li>{@link #getContinuousNodeBuilder()}</li>
 * <li>{@link #getDecisionNodeBuilder()}</li>
 * <li>{@link #getUtilityNodeBuilder()}</li>
 * </ul>
 * 
 * @author Shou Matsumoto
 *
 * @see IProbabilisticNetworkBuilder
 * @see RandomSBNBuilderImpl
 */
public interface RandomSBNBuilder extends IProbabilisticNetworkBuilder, NetworkStructureDataTransferObject {

	/**
	 * @param numParents : the maximum number of parents in the network to be
	 *                   generated with {@link #buildNetwork()}.
	 * 
	 * @see #setNumNodes(int)
	 */
	void setNumParents(int numParents);

	/**
	 * 
	 * @param numNodes : the number of nodes in the network to be generated with
	 *                 {@link #buildNetwork()}.
	 * 
	 * @see #setNumStates(int)
	 * @see #setNumParents(int)
	 */
	void setNumNodes(int numNodes);

}
