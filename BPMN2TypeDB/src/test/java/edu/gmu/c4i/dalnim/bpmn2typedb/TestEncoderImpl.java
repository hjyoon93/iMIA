package edu.gmu.c4i.dalnim.bpmn2typedb;

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

import edu.gmu.c4i.dalnim.bpmn2typedb.encoder.Encoder;
import edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl;

/**
 * Default test unit for {@link EncoderImpl}
 * 
 * @author shou
 */
public class TestEncoderImpl {

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
	 * Test method for {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#loadInput(java.io.InputStream)}.
	 */
	@Test
	public final void testLoadInput() throws Exception {
		
		Encoder encoder = EncoderImpl.getEncoder();
		
		encoder.loadInput(getClass().getResourceAsStream("/simple.bpmn"));
		
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeSchema(java.io.OutputStream)}.
	 */
	@Test
	public final void testEncodeSchema() throws Exception {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeData(java.io.OutputStream)}.
	 */
	@Test
	public final void testEncodeData() throws Exception {
		fail("Not yet implemented"); // TODO
	}

}
