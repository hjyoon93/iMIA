package edu.gmu.c4i.dalnim.sbn;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import unbbayes.prs.Graph;
import unbbayes.prs.Node;
import unbbayes.prs.bn.PotentialTable;
import unbbayes.prs.bn.ProbabilisticNetwork;
import unbbayes.prs.bn.ProbabilisticNode;

/**
 * @author Shou Matsumoto
 *
 */
public class RandomSBNBuilderImplTest {

	private static Logger logger = LoggerFactory.getLogger(RandomSBNBuilderImplTest.class);

	/**
	 * @throws java.lang.Exception
	 */
	@BeforeClass
	public static void setUpBeforeClass() throws Exception {
	}

	/**
	 * @throws java.lang.Exception
	 */
	@AfterClass
	public static void tearDownAfterClass() throws Exception {
	}

	/**
	 * @throws java.lang.Exception
	 */
	@Before
	public void setUp() throws Exception {
	}

	/**
	 * @throws java.lang.Exception
	 */
	@After
	public void tearDown() throws Exception {
	}

	/**
	 * Test method for
	 * {@link edu.gmu.c4i.dalnim.sbn.RandomSBNBuilderImpl#generateRandomNet()}.
	 */
	@Test
	public final void testGenerateRandomNet() {
		long seed = System.currentTimeMillis();
		logger.info("Seed = {}", seed);
		
		int numStates = 2;
		int numNodes = 50;
		int treewidth = 15;
		int totalCounts = 100;

		RandomSBNBuilderImpl builder = (RandomSBNBuilderImpl) RandomSBNBuilderImpl.getInstance();
		assertNotNull(builder);
		builder.setMinNumStates(numStates);
		builder.setMaxNumStates(numStates);
		builder.setNumNodes(numNodes);
		builder.setMaxTreeWidth(treewidth);
		builder.setTotalCounts(totalCounts);

		Graph net = builder.generateRandomNet();
		assertTrue(net instanceof ProbabilisticNetwork);

		assertEquals(numNodes, net.getNodeCount());
		assertTrue(net.getEdges().size() > 0);

		// #getNetwork should use a cache
		assertEquals(net, builder.getNetwork());

		for (Node node : net.getNodes()) {
			assertEquals(numStates, node.getStatesSize());
			assertTrue(node.getParentNodes().size() <= treewidth);
			assertTrue(node instanceof ProbabilisticNode);
			PotentialTable table = builder.getCountTable(net, node);
			assertNotNull(table);
			assertEquals((double)totalCounts, table.getSum(), 0.5d);
		}

	}

}
