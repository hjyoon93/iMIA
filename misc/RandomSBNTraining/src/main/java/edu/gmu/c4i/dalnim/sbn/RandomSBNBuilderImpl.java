package edu.gmu.c4i.dalnim.sbn;

import java.util.HashMap;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import unbbayes.prs.Graph;
import unbbayes.prs.Node;
import unbbayes.prs.bn.ProbabilisticNetwork;
import unbbayes.prs.builder.INodeBuilder;
import unbbayes.prs.builder.impl.DefaultProbabilisticNodeBuilder;

/**
 * Default implementation of {@link RandomSBNBuilder}
 * 
 * @author Shou Matsumoto
 *
 */
public class RandomSBNBuilderImpl implements RandomSBNBuilder {

	private static Logger logger = LoggerFactory.getLogger(RandomSBNBuilderImpl.class);

	private int numNodes = 600;

	private int numParents = 15;

	private INodeBuilder probabilisticNodeBuilder;

	private Map<String, ProbabilisticNetwork> multipletonMap = new HashMap<>();

	/**
	 * Default constructor is protected to avoid public access, but to allow quick
	 * inheritance. Use {@link #getInstance()} instead.
	 */
	protected RandomSBNBuilderImpl() {
		// Auto-generated constructor stub
	}

	/**
	 * Default public constructor method.
	 * 
	 * @return a builder of SBN. Use {@link RandomSBNBuilder#buildNetwork(String)}
	 *         to obtain an instance of the SBN.
	 * 
	 * @see #setProbabilisticNodeBuilder(INodeBuilder)
	 * @see #setNumNodes(int)
	 * @see #setNumParents(int)
	 */
	public static RandomSBNBuilder getInstance() {
		return new RandomSBNBuilderImpl();
	}

	@Override
	public ProbabilisticNetwork buildNetwork(String netName) {

		logger.debug("Building network {}...", netName);

		// extract the parameters
		int totalNumNodes = getNumNodes();
		int maxParents = getNumParents();
		INodeBuilder nodeBuilder = getProbabilisticNodeBuilder();
		logger.debug("Number of nodes: {}", totalNumNodes);
		logger.debug("Number of parents: {}", maxParents);
		logger.debug("Network builder: {}", nodeBuilder);

		// TODO Auto-generated method stub

		throw new UnsupportedOperationException("Not implemented yet");
	}

	@Override
	public INodeBuilder getContinuousNodeBuilder() {
		throw new UnsupportedOperationException("Continuous nodes are not supported.");
	}

	@Override
	public INodeBuilder getDecisionNodeBuilder() {
		throw new UnsupportedOperationException("Decision nodes are not supported.");
	}

	@Override
	public synchronized INodeBuilder getProbabilisticNodeBuilder() {
		if (probabilisticNodeBuilder == null) {
			logger.debug("Instantiating a boolean node builder...");
			probabilisticNodeBuilder = new DefaultProbabilisticNodeBuilder() {
				@Override
				public Node buildNode() {
					Node node = super.buildNode();
					// boolean nodes should have 2 states
					for (int i = 0; i < Integer.MAX_VALUE; i++) {
						if (node.getStatesSize() < 2) {
							node.appendState(Integer.toString(i));
						}
					}
					// at this point, the node must have 2 (or more) states
					if (node.getStatesSize() != 2) {
						throw new IllegalStateException("Failed to generate a node with 2 states (boolean)");
					}
					// make sure the names of the states are 'false' and 'true'
					node.setStateAt("false", 0);
					node.setStateAt("true", 1);
					return node;
				}
			};
		}
		return probabilisticNodeBuilder;
	}

	@Override
	public INodeBuilder getUtilityNodeBuilder() {
		throw new UnsupportedOperationException("Utility nodes are not supported.");
	}

	@Override
	public void setContinuousNodeBuilder(INodeBuilder arg0) {
		throw new UnsupportedOperationException("Continuous nodes are not supported.");
	}

	@Override
	public void setDecisionNodeBuilder(INodeBuilder arg0) {
		throw new UnsupportedOperationException("Decision nodes are not supported.");
	}

	@Override
	public synchronized void setProbabilisticNodeBuilder(INodeBuilder builder) {
		this.probabilisticNodeBuilder = builder;
	}

	@Override
	public void setUtilityNodeBuilder(INodeBuilder arg0) {
		throw new UnsupportedOperationException("Utility nodes are not supported.");
	}

	@Override
	public void setNumParents(int numParents) {
		this.numParents = numParents;
	}

	@Override
	public void setNumNodes(int numNodes) {
		this.numNodes = numNodes;
	}

	/**
	 * @return the number of nodes to generate in {@link #buildNetwork(String)}
	 * 
	 * @see #setNumNodes(int)
	 */
	public int getNumNodes() {
		return numNodes;
	}

	/**
	 * @return the number of parents to generate for each node in the network of
	 *         {@link #buildNetwork(String)}
	 * 
	 * @see #setNumParents(int)
	 */
	public int getNumParents() {
		return numParents;
	}

	/**
	 * @return the multipletonMap
	 * 
	 * @see {@link #getNetwork()}
	 */
	protected Map<String, ProbabilisticNetwork> getMultipletonMap() {
		return multipletonMap;
	}

	/**
	 * @param multipletonMap the multipletonMap to set
	 * 
	 * @see {@link #getNetwork()}
	 */
	protected void setMultipletonMap(Map<String, ProbabilisticNetwork> multipletonMap) {
		this.multipletonMap = multipletonMap;
	}

	@Override
	public Graph getNetwork() {

		String netName = this.toString();
		if (getMultipletonMap().containsKey(netName)) {
			logger.debug("[MULTIPLETON] reusing network {}", netName);
			return getMultipletonMap().get(netName);
		}

		ProbabilisticNetwork net = buildNetwork(netName);
		getMultipletonMap().put(netName, net);
		return net;
	}

}
