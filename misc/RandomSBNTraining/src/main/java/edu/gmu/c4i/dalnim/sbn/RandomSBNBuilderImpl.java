package edu.gmu.c4i.dalnim.sbn;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import unbbayes.io.CountCompatibleNetIO;
import unbbayes.prs.Graph;
import unbbayes.prs.INode;
import unbbayes.prs.Node;
import unbbayes.prs.bn.PotentialTable;
import unbbayes.prs.bn.ProbabilisticNode;
import unbbayes.prs.builder.INodeBuilder;
import unbbayes.util.Debug;
import unbbayes.util.random.RandomNetworkGenerator;

/**
 * Default implementation of {@link RandomSBNBuilder}
 * 
 * @author Shou Matsumoto
 *
 */
public class RandomSBNBuilderImpl extends RandomNetworkGenerator implements RandomSBNBuilder {

	public static final int DEFAULT_TREEWIDTH = 15;

	public static final int DEFAULT_NET_SIZE = 600;

	public static final int DEFAULT_NUM_STATES = 2;

	private static Logger logger = LoggerFactory.getLogger(RandomSBNBuilderImpl.class);

	private int totalCounts = 100;

	private Graph networkCache = null;

	private boolean ignoreWarnings = true;

	/**
	 * Default constructor is protected to avoid public access, but to allow quick
	 * inheritance. Use {@link #getInstance()} instead.
	 */
	protected RandomSBNBuilderImpl() {
		try {
			// force default settings
			this.setMaxTreeWidth(DEFAULT_TREEWIDTH);
			this.setNumNodes(DEFAULT_NET_SIZE);

			// set max and min states size to the same value
			this.setMinNumStates(DEFAULT_NUM_STATES);
			this.setMaxNumStates(DEFAULT_NUM_STATES);
		} catch (Exception e) {
			logger.warn("Failed to bootstrap instance '{}'", this);
		}
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

	/**
	 * Obtains a network from cache.
	 * 
	 * @see #getNetworkCache()
	 * @see #resetNetworkCache()
	 * @see #generateRandomNet()e
	 */
	@Override
	public synchronized Graph getNetwork() {

		// retrieving from cache
		Graph net = getNetworkCache();

		// generate network if cache was not present
		if (net != null) {
			logger.debug("Returning cached network");
		} else {
			// Note: generateRandomNet will update cache
			net = this.generateRandomNet();
		}

		return net;
	}

	/**
	 * Generates a random network. It will also force the cache to be updated with
	 * {@link #setNetworkCache(Graph)}
	 * 
	 * @see #getNetwork()
	 * @see #resetNetworkCache()
	 */
	@Override
	public synchronized Graph generateRandomNet() {

		// generate new net and fill its count tables
		logger.debug("Generating new network");
		Graph net = this.fillCountTables(this.renameStates(super.generateRandomNet()));

		logger.debug("Setting network cache: {}", net);
		setNetworkCache(net);

		return net;
	}

	/**
	 * Renames the states of nodes.
	 * 
	 * @param graph : the graph with the nodes to rename
	 * @return the argument
	 */
	protected Graph renameStates(Graph graph) {

		logger.debug("Renaming the states of nodes in the network {}", graph);

		if (graph != null) {
			for (Node node : graph.getNodes()) {
				if (node.getStatesSize() <= 2) {
					// This is a boolean node.
					// Rename to false or true.
					if (node.getStatesSize() >= 1) {
						node.setStateAt("false", 0);
					}
					if (node.getStatesSize() >= 2) {
						node.setStateAt("true", 1);
					}
				} else {
					// This is non-boolean node.
					// Rename to state<N>
					for (int state = 0; state < node.getStatesSize(); state++) {
						node.setStateAt("state" + state, state);
					}
				}
			}
		}

		return graph;
	}

	/**
	 * @param graph : the network where the node belongs to. This reference will be
	 *              used to access network properties with
	 *              {@link Graph#getProperty(String)}
	 * @param owner : the node to obtain its count table.
	 * 
	 * @return the Beta/Dirichlet count (absolute frequencies, or magnitude) table
	 *         of the specified node. A new count table will be created if the node
	 *         was not associated with any count table.
	 * 
	 * @see CountCompatibleNetIO#DEFAULT_COUNT_TABLE_PREFIX
	 * @see #setCountTable(Graph, INode, PotentialTable)
	 */
	public PotentialTable getCountTable(Graph graph, INode owner) {

		if (owner == null) {
			throw new NullPointerException("The owner of the table must be specified");
		}

		if (graph != null) {
			PotentialTable countTable = (PotentialTable) graph
					.getProperty(CountCompatibleNetIO.DEFAULT_COUNT_TABLE_PREFIX + owner.getName());
			if (owner instanceof ProbabilisticNode) {
				// this boolean var will become true
				// if we need to create a new count table
				boolean createCountTable = false;
				if (countTable == null) {
					Debug.println(getClass(),
							"No count table found for " + owner + ". Creating a new one from its CPT...");
					createCountTable = true;
				} else if (countTable.tableSize() != ((ProbabilisticNode) owner).getProbabilityFunction().tableSize()) {
					Debug.println(getClass(),
							"Size of count table is not matching. CPT size = "
									+ ((ProbabilisticNode) owner).getProbabilityFunction().tableSize()
									+ ",  count table size = " + countTable.tableSize());
					Debug.println(getClass(), "Count table of " + owner + " will be reallocated");
					createCountTable = true;
				} // else reuse the obtained count table

				if (createCountTable) {
					Debug.println(getClass(), "Creating count table of " + owner);
					try {
						// copy the potential table and use it as the count table
						countTable = (PotentialTable) ((ProbabilisticNode) owner).getProbabilityFunction().clone();
						// store the cloned table
						this.setCountTable(graph, owner, countTable);
					} catch (Exception e) {
						Debug.println(getClass(), "Failed to create a new count table for node " + owner, e);
					}
				}
			}
			return countTable;
		}

		return null;
	}

	/**
	 * @param graph : the network where the node belongs to. This reference will be
	 *              used to set the network properties with
	 *              {@link Graph#addProperty(String, Object)}
	 * @param owner : the node that will own the count table (the count table will
	 *              be set for this node).
	 * 
	 * @param table : the Beta/Dirichlet count (absolute frequencies, or magnitude)
	 *              table to set.
	 * 
	 * @see CountCompatibleNetIO#DEFAULT_COUNT_TABLE_PREFIX
	 * @see #getCountTable(Graph, INode)
	 */
	public void setCountTable(Graph graph, INode owner, PotentialTable table) {

		if (owner == null || graph == null) {
			throw new NullPointerException("The owner of the table (and its network) must be specified");
		}

		logger.debug("Setting the count table of node '{}' in network '{}' to: {}", owner, graph, table);
		if (table == null) {
			graph.removeProperty(CountCompatibleNetIO.DEFAULT_COUNT_TABLE_PREFIX + owner.getName());
		} else {
			graph.addProperty(CountCompatibleNetIO.DEFAULT_COUNT_TABLE_PREFIX + owner.getName(), table);
		}

	}

	/**
	 * Makes sure the count tables in the network are populated proportionally to
	 * the CPTs.
	 * 
	 * @param net : the network to modify
	 * 
	 * @return the modified network (this implementation simply returns the object
	 *         passed as argument).
	 * 
	 * @see #getCountTable(Graph, INode)
	 * @see #setCountTable(Graph, INode, PotentialTable)
	 */
	protected Graph fillCountTables(Graph net) {

		logger.debug("Generating count tables");

		// generate/update count tables for all nodes
		for (Node node : net.getNodes()) {

			// we assume all nodes are probabilistic
			if (node instanceof ProbabilisticNode) {

				ProbabilisticNode probNode = (ProbabilisticNode) node;

				// extract the CPT
				PotentialTable cpt = probNode.getProbabilityFunction().getTemporaryClone();
				if (cpt == null) {
					logger.warn("Failed to extract CPT of node {}", probNode);
					if (!isIgnoreWarnings()) {
						throw new IllegalArgumentException(
								"Node '" + probNode + "' was not associated with any conditional probability table");
					}
					continue;
				}

				// extract the count table
				PotentialTable countTable = this.getCountTable(net, probNode);
				// getCountTable supposedly returns a non-null consistent table,
				// but let's just double-check
				if (countTable == null || countTable.tableSize() != cpt.tableSize()) {
					logger.warn("No count table was found for node {}. Creating new instance...", probNode);
					if (!isIgnoreWarnings()) {
						throw new IllegalArgumentException(
								"Failed to obtain a count table for node '" + probNode + "'");
					}
					countTable = (PotentialTable) cpt.clone();
				} else {
					logger.debug("Updating count table of node {}", probNode);
				}

				// set the absolute frequency to CPT * total
				// (i.e. Beta/Dirichlet parameter will become distribution * magnitude)
				logger.debug("Setting the count table to \"distribution * magnitude\"");
				countTable.fillTable(getTotalCounts());
				cpt.normalize();
				countTable.opTab(cpt, PotentialTable.PRODUCT_OPERATOR);

				// this is to make sure we overwrite the original count table
				setCountTable(net, probNode, countTable);

			} else {
				if (isIgnoreWarnings()) {
					logger.warn("Ignoring node '{}' with incompatible node type: {}", node,
							// print node's class if not null.
							((node != null) ? node.getClass() : null));
				} else {
					throw new IllegalArgumentException("Node '" + node + "' was expected to be an instance of '"
							+ ProbabilisticNode.class + "', but it was: "
							// print node's class if not null.
							+ ((node != null) ? node.getClass() : null));

				}
			}
		}

		// just return the same instance we got from the argument
		return net;
	}

	@Override
	public void setTotalCounts(int totalCounts) {
		this.totalCounts = totalCounts;
	}

	/**
	 * @return the totalCounts (Beta/Dirichlet virtual counts/magnitude).
	 * 
	 * @see #setTotalCounts(int)
	 * @see #generateRandomNet()e
	 */
	public int getTotalCounts() {
		return totalCounts;
	}

	/**
	 * @return a cache to be used in {@link #getNetwork()}.
	 *         {@link #generateRandomNet()} shall overwrite this cache.
	 */
	protected synchronized Graph getNetworkCache() {
		return networkCache;
	}

	/**
	 * @param networkCache : a cache to be used in {@link #getNetwork()}.
	 *                     {@link #generateRandomNet()} shall overwrite this cache.
	 */
	protected synchronized void setNetworkCache(Graph networkCache) {
		this.networkCache = networkCache;
	}

	/**
	 * Resets the cache at {@link #getNetwork()}
	 */
	public void resetNetworkCache() {
		logger.debug("Resetting network cache...");
		this.setNetworkCache(null);
	}

	/**
	 * @return if true, {@link #generateRandomNet()} will ignore warnings. If false,
	 *         it will throw exceptions on warnings.
	 */
	public boolean isIgnoreWarnings() {
		return ignoreWarnings;
	}

	/**
	 * @param ignoreWarnings : if true, {@link #generateRandomNet()} will ignore
	 *                       warnings. If false, it will throw exceptions on
	 *                       warnings.
	 */
	public void setIgnoreWarnings(boolean ignoreWarnings) {
		this.ignoreWarnings = ignoreWarnings;
	}

}
