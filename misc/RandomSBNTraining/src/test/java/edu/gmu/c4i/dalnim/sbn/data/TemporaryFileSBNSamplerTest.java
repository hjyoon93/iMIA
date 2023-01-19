package edu.gmu.c4i.dalnim.sbn.data;

import static org.junit.Assert.*;

import java.io.File;
import java.nio.file.Files;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

import unbbayes.io.CountCompatibleNetIO;
import unbbayes.prs.Graph;
import unbbayes.prs.bn.ProbabilisticNetwork;
import unbbayes.prs.sbn.RunnableSBNParameterLearning.NetworkStructureDataTransferObject;

/**
 * Unit test of {@link TemporaryFileSBNSampler}
 * 
 * @author Shou Matsumoto
 */
public class TemporaryFileSBNSamplerTest {

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

	@Test
	public final void test() throws Exception {

		int dataSize = 10;

		File netFile = new File(getClass().getResource("/DEF.net").toURI());
		assertTrue(netFile.exists());

		Graph graph = new CountCompatibleNetIO().load(netFile);
		assertTrue(graph instanceof ProbabilisticNetwork);

		TemporaryFileSBNSampler sampler = (TemporaryFileSBNSampler) TemporaryFileSBNSampler.getInstance(() -> graph);
		assertNotNull(sampler);

		sampler.setDataSize(dataSize);
		sampler.run();

		File dataFile = sampler.getOutputLocation();
		assertTrue(dataFile.exists());

		String dataContent = Files.readString(dataFile.toPath());
		assertFalse(dataContent.trim().isEmpty());

		//
		String[] lines = dataContent.split("[\\n\\r]+");
		assertTrue(lines[0].matches("D\\s+E\\sF"));
		for (int line = 1; line < lines.length; line++) {
			assertTrue(lines[line].matches("((true|false)\\s+){2}(true|false){1}"));
		}

		Files.delete(dataFile.toPath());
	}

}
