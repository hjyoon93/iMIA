package edu.gmu.c4i.dalnim.bpmn2typedb;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.fail;

import java.io.ByteArrayOutputStream;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

import edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl;

/**
 * Default test unit for {@link EncoderImpl}
 * 
 * @author shou
 */
public class TestEncoderImpl {

	private EncoderImpl encoder;

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
		encoder = (EncoderImpl) EncoderImpl.getInstance();
		assertNotNull(encoder);
	}

	/**
	 * @throws java.lang.Exception
	 */
	@After
	public void tearDown() throws Exception {
	}

	/**
	 * Test method for
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#loadInput(java.io.InputStream)}.
	 */
	@Test
	public final void testLoadInput() throws Exception {

		encoder.loadInput(getClass().getResourceAsStream("/simple.bpmn"));

		assertNotNull(encoder.getBPMNModel());
		assertNotNull(encoder.getInstanceNamespace());
		assertNotNull(encoder.getSchemaNamespace());

		assertEquals("https://camunda.org/examples", encoder.getInstanceNamespace());
		assertEquals("http://www.omg.org/spec/BPMN/20100524/MODEL", encoder.getSchemaNamespace());

		encoder = (EncoderImpl) EncoderImpl.getInstance();
		assertNotNull(encoder);

		encoder.loadInput(getClass().getResourceAsStream("/Models and Diagrams/Process.bpmn"));

		assertNotNull(encoder.getBPMNModel());
		assertNotNull(encoder.getInstanceNamespace());
		assertNotNull(encoder.getSchemaNamespace());

		assertEquals("http://www.trisotech.com/definitions/_1275486223307", encoder.getInstanceNamespace());
		assertEquals("http://www.omg.org/spec/BPMN/20100524/MODEL", encoder.getSchemaNamespace());
	}

	/**
	 * Test method for
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeSchema(java.io.OutputStream)}.
	 */
	@Test
	public final void testEncodeSchema() throws Exception {

		encoder.loadInput(getClass().getResourceAsStream("/simple.bpmn"));
		
		ByteArrayOutputStream out = new ByteArrayOutputStream();
		encoder.encodeSchema(out);
		
		fail("Not yet implemented"); // TODO
	}

	/**
	 * Test method for
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeData(java.io.OutputStream)}.
	 */
	@Test
	public final void testEncodeData() throws Exception {
		fail("Not yet implemented"); // TODO
	}

	/**
	 * @return the encoder
	 */
	public EncoderImpl getEncoder() {
		return encoder;
	}

	/**
	 * @param encoder the encoder to set
	 */
	public void setEncoder(EncoderImpl encoder) {
		this.encoder = encoder;
	}

}
