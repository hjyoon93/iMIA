package edu.gmu.c4i.dalnim.bpmn2typedb;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.io.ByteArrayOutputStream;
import java.text.ParseException;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Ignore;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.vaticle.typeql.lang.TypeQL;
import com.vaticle.typeql.lang.common.exception.TypeQLException;
import com.vaticle.typeql.lang.query.TypeQLQuery;

import edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl;

/**
 * Default test unit for {@link EncoderImpl}
 * 
 * @author shou
 */
public class EncoderImplTest {

	private static Logger logger = LoggerFactory.getLogger(EncoderImplTest.class);

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
	 * @param resource : location of BPMN file to load.
	 * @see #testEncodeBPMNSchema()
	 */
	public void testEncodeSchema(String resource) throws Exception {
		EncoderImpl encoder = (EncoderImpl) EncoderImpl.getInstance();
		assertNotNull(encoder);

		encoder.setRunSanityCheck(true);
		encoder.loadInput(getClass().getResourceAsStream(resource));

		ByteArrayOutputStream out = new ByteArrayOutputStream();
		encoder.encodeSchema(out);
		out.flush();

		String schema = out.toString();
		logger.debug("Generated typeql schema: \n{}", schema);

		assertFalse(schema.trim().isEmpty());

		// make sure the typeql schema can be parsed
		assertTrue(encoder.checkDefinitionReferences(schema));

	}

	/**
	 * Basic tests for TypeQL parsing at
	 * {@link EncoderImpl#checkDefinitionReferences(String)}
	 * 
	 * @throws Exception
	 */
	@Test
	public final void testParseTypeQL() throws Exception {
		EncoderImpl encoder = (EncoderImpl) EncoderImpl.getInstance();
		assertNotNull(encoder);

		String typeql = "define\n" + "\n" + "## BPMN entities in general\n" + "id sub attribute, value string;\n"
				+ "BPMN asdfsdf entity, owns id;\n" + "       \n" + "## BPMN 'definitions' tag (header)\n"
				+ "definitions sub BPMN;\n" + "\n" + "targetNamespace sub attribute, value string;\n"
				+ "xmlns sub attribute, value string;\n" + "\n" + "definitions owns targetNamespace, owns xmlns;\n"
				+ "BPMN_definitions_collaboration sub relation,\n" + "  relates BPMN_parent,\n"
				+ "  relates BPMN_child;\n" + "definitions plays BPMN_definitions_collaboration:BPMN_parent;\n"
				+ "collaboration plays BPMN_definitions_collaboration:BPMN_child;";
		// parsing must fail
		try {
			assertTrue(encoder.checkDefinitionReferences(typeql));
			fail("Must fail");
		} catch (ParseException | TypeQLException e) {
			assertFalse(e.getMessage().trim().isEmpty());
			assertTrue(e.getMessage().toLowerCase().contains("syntax error"));
		}

		typeql = "define\n" + "\n" + "## BPMN entities in general\n" + "id sub attribute, value string;\n"
				+ "BPMN sub entity, owns id;\n" + "       \n" + "## BPMN 'definitions' tag (header)\n"
				+ "definitions sub BPMN_A;\n" + "\n" + "targetNamespace sub attribute, value string;\n"
				+ "xmlns sub attribute, value string;\n" + "\n" + "definitions owns targetNamespace, owns xmlns;\n"
				+ "BPMN_definitions_collaboration sub relation,\n" + "  relates BPMN_parent,\n"
				+ "  relates BPMN_child;\n" + "definitions plays BPMN_definitions_collaboration:BPMN_parent;\n"
				+ "collaboration plays BPMN_definitions_collaboration:BPMN_child;";
		// verification must fail because BPMN_A is never declared
		try {
			assertTrue(encoder.checkDefinitionReferences(typeql));
			fail("Must fail");
		} catch (ParseException | TypeQLException e) {
			assertTrue(e.getMessage().contains("BPMN_A"));
		}

		typeql = "define\n" + "\n" + "## BPMN entities in general\n" + "id sub attribute, value string;\n"
				+ "BPMN sub entity, owns id;\n" + "       \n" + "## BPMN 'definitions' tag (header)\n"
				+ "definitions sub BPMN;\n" + "\n" + "targetNamespace sub attribute, value string;\n"
				+ "xmlns sub attribute, value string;\n" + "\n" + "definitions owns targetNamespace, owns xmlns;\n"
				+ "BPMN_definitions_collaboration sub relation,\n" + "  relates BPMN_parent,\n"
				+ "  relates BPMN_child;\n" + "definitions plays BPMN_definitions_collaboration_A:BPMN_parent;\n"
				+ "collaboration plays BPMN_definitions_collaboration:BPMN_child;";
		// parsing/verification must fail:
		// BPMN_definitions_collaboration_A never declared
		try {
			assertTrue(encoder.checkDefinitionReferences(typeql));
			fail("Must fail");
		} catch (ParseException | TypeQLException e) {
			assertTrue(e.getMessage().contains("BPMN_definitions_collaboration_A"));
		}

		typeql = "define\n" + "\n" + "## BPMN entities in general\n" + "id sub attribute, value string;\n"
				+ "BPMN sub entity, owns id;\n" + "       \n" + "## BPMN 'definitions' tag (header)\n"
				+ "definitions sub BPMN;\n" + "\n" + "targetNamespace sub attribute, value string;\n"
				+ "xmlns sub attribute, value string;\n" + "\n" + "definitions owns targetNamespace, owns xmlns;\n"
				+ "BPMN_definitions_collaboration sub relation,\n" + "  relates BPMN_parent,\n"
				+ "  relates BPMN_child;\n" + "definitions plays BPMN_definitions_collaboration:BPMN_parent;\n"
				+ "collaboration plays BPMN_definitions_collaboration:qwerty";
		// parsing/verification must fail:
		// BPMN_definitions_collaboration:qwerty never declared
		try {
			assertTrue(encoder.checkDefinitionReferences(typeql));
			fail("Must fail");
		} catch (ParseException | TypeQLException e) {
			assertTrue(e.getMessage().contains("qwerty"));
		}

		typeql = "define\n" + "\n" + "## BPMN entities in general\n" + "id sub attribute, value string;\n"
				+ "BPMN sub entity, owns id;\n" + "       \n" + "## BPMN 'definitions' tag (header)\n"
				+ "definitions sub BPMN;\n" + "\n" + "targetNamespace sub attribute, value string;\n"
				+ "xmlns sub attribute, value string;\n" + "\n" + "definitions owns targetNamespace, owns xmlns;\n"
				+ "BPMN_definitions_collaboration sub relation,\n" + "  relates BPMN_parent,\n"
				+ "  relates BPMN_child;\n" + "definitions plays BPMN_definitions_collaboration:BPMN_parent;\n"
				+ "collaboration plays BPMN_definitions_collaboration:BPMN_child;";
		// should pass now
		assertTrue(encoder.checkDefinitionReferences(typeql));
	}

	/**
	 * Test method for
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#loadInput(java.io.InputStream)}.
	 */
	@Test
	public final void testLoadInput() throws Exception {
		EncoderImpl encoder = (EncoderImpl) EncoderImpl.getInstance();
		assertNotNull(encoder);

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
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeSchema(java.io.OutputStream)}
	 * for simple BPMN models.
	 * 
	 * @see #testEncodeSchema(String)
	 */
	@Test
	public final void testEncodeBPMNSchemaSimple() throws Exception {

		testEncodeSchema("/simple.bpmn");

		testEncodeSchema("/UAV_material_transport_eclipse.bpmn");

	}

	/**
	 * Test method for
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeSchema(java.io.OutputStream)}
	 * for multiple examples of BPMN models obtained from the web.
	 * 
	 * @see #testEncodeSchema(String)
	 */
	@Test
	public final void testEncodeBPMNSchemaExamles() throws Exception {

		testEncodeSchema("/Models and Diagrams/Process.bpmn");
		testEncodeSchema("/Models and Diagrams/Pool.bpmn");
		testEncodeSchema("/Models and Diagrams/Laneset.bpmn");
		testEncodeSchema("/Models and Diagrams/Expanded SubProcess.bpmn");
		testEncodeSchema("/Models and Diagrams/Collapsed SubProcess.bpmn");
		testEncodeSchema("/Models and Diagrams/Call Activity.bpmn");

		testEncodeSchema("/Diagram Interchange/Examples - DI -Collapsed Sub-Process.bpmn");
		testEncodeSchema("/Diagram Interchange/Examples - DI - Expanded Sub-Process.bpmn");

		testEncodeSchema("/eMail Voting/Email Voting 2.bpmn");

		testEncodeSchema("/Hardware Retailer/triso - Hardware Retailer v2.bpmn");

		testEncodeSchema("/Incident Management/Incident Management(Account Manager Only).bpmn");
		testEncodeSchema("/Incident Management/Incident Management(Process Engine Executable).bpmn");
		testEncodeSchema("/Incident Management/Incident Management(Process Engine Only).bpmn");
		testEncodeSchema("/Incident Management/Incident Management(Whole Collab).bpmn");
		testEncodeSchema("/Incident Management/Incident Management - coll chor.bpmn");
		testEncodeSchema("/Incident Management/Incident Management level 1.bpmn");

		testEncodeSchema("/Nobel Prize/Nobel Prize Process.bpmn");

		testEncodeSchema(
				"/Order Fulfillment/Procurement Processes with Error Handling - Stencil Trisotech 3 pages.bpmn");

		testEncodeSchema("/Pizza/triso - Order Process for Pizza V4.bpmn");

		testEncodeSchema("/Travel Booking/Tavel Booking.bpmn");

	}

	/**
	 * Test method for
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeData(java.io.OutputStream)}.
	 */
	@Test
	@Ignore("Still fixing")
	public final void testEncodeDataSimple() throws Exception {
		EncoderImpl encoder = (EncoderImpl) EncoderImpl.getInstance();

		encoder.loadInput(getClass().getResourceAsStream("/simple.bpmn"));

		ByteArrayOutputStream out = new ByteArrayOutputStream();
		encoder.encodeData(out);
		out.flush();

		String typeql = out.toString();
		logger.debug("Generated typeql data: \n{}", typeql);

		assertFalse(typeql.trim().isEmpty());

		// make sure the typeql schema can be parsed
		TypeQLQuery parsed = TypeQL.parseQuery(typeql);
		assertNotNull(parsed.asInsert());

	}

}
