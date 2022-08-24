package edu.gmu.c4i.dalnim.bpmn2typedb;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.io.ByteArrayOutputStream;
import java.text.ParseException;
import java.util.List;
import java.util.stream.Collectors;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
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
	 * 
	 * @return the typeql script
	 * 
	 * @see #testEncodeBPMNSchema()
	 */
	public String testEncodeSchema(String resource) throws Exception {
		EncoderImpl encoder = (EncoderImpl) EncoderImpl.getInstance();
		assertNotNull(encoder);

		encoder.setRunSanityCheck(true);
		encoder.loadInput(getClass().getResourceAsStream(resource));

		ByteArrayOutputStream out = new ByteArrayOutputStream();
		encoder.encodeSchema(out);
		out.flush();

		String schema = out.toString();
//		logger.debug("Generated typeql schema: \n{}", schema);

		assertFalse(schema.trim().isEmpty());

		// make sure the typeql schema can be parsed
		assertTrue(encoder.checkDefinitionReferences(schema));

		return schema;
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
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeData(java.io.OutputStream)}
	 * for simple.bpmn.
	 */
	@Test
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
		List<TypeQLQuery> parsedList = TypeQL.parseQueries(typeql).collect(Collectors.toList());
		// there should be many commands
		assertFalse("Size = " + parsedList.size(), parsedList.isEmpty());
		// the 1st command should be an insert
		assertNotNull(parsedList.get(0).asInsert());
	}

	/**
	 * Test method for
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeData(java.io.OutputStream)}
	 * for UAV_material_transport_eclipse.bpmn.
	 */
	@Test
	public final void testEncodeDataUAV() throws Exception {
		EncoderImpl encoder = (EncoderImpl) EncoderImpl.getInstance();

		encoder.loadInput(getClass().getResourceAsStream("/UAV_material_transport_eclipse.bpmn"));

		ByteArrayOutputStream out = new ByteArrayOutputStream();
		encoder.encodeData(out);
		out.flush();

		String typeql = out.toString();
		logger.debug("Generated typeql data: \n{}", typeql);

		assertFalse(typeql.trim().isEmpty());

		// make sure the typeql can be parsed
		List<TypeQLQuery> parsedList = TypeQL.parseQueries(typeql).collect(Collectors.toList());
		// there should be many commands
		assertFalse("Size = " + parsedList.size(), parsedList.isEmpty());
		// the 1st command should be an insert
		assertNotNull(parsedList.get(0).asInsert());
	}

	/**
	 * Test method for
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeSchema(java.io.OutputStream)}
	 * and
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeD(java.io.OutputStream)}
	 * for a simple BPMN model about data object.
	 * 
	 * @see #testEncodeSchema(String)
	 */
	@Test
	public final void testEncodeBPMNDataObjectWithMapping() throws Exception {

		// make sure the schema can be generated
		testEncodeSchema("/dataObject.bpmn");

		// generate the data
		EncoderImpl encoder = (EncoderImpl) EncoderImpl.getInstance();

		// force-enable mapping from BPMN to concept model
		encoder.setMapBPMNToConceptualModel(true);

		encoder.loadInput(getClass().getResourceAsStream("/dataObject.bpmn"));
		String dataTypeQL;
		try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
			encoder.encodeData(out);
			dataTypeQL = out.toString();
		}

		logger.debug("Generated typeql data: \n{}", dataTypeQL);
		assertFalse(dataTypeQL.trim().isEmpty());

		// make sure the typeql data can be parsed
		List<TypeQLQuery> parsedList = TypeQL.parseQueries(dataTypeQL).collect(Collectors.toList());
		// there should be many commands
		assertFalse("Size = " + parsedList.size(), parsedList.isEmpty());
		// the 1st command should be an insert
		assertNotNull(parsedList.get(0).asInsert());

		// check presence of relations that represent
		// mapping between BPMN and concept model
		assertTrue(encoder.isMapBPMNToConceptualModel());

		/**
		 * We should find declarations like the following:
		 * 
		 * <pre>
		 * insert $concept isa Asset, has uid (...);
		 * match
		 * 		$bpmnEntity isa BPMN_Entity, has uid (...);
		 * 		$concept isa entity, has uid (...);
		 * insert $rel (bpmnEntity: $bpmnEntity, conceptualModel: $concept) isa BPMN_hasConceptualModelElement;
		 * </pre>
		 */
		boolean foundConcept = false;
		for (int i = 0; i < parsedList.size(); i++) {
			TypeQLQuery insertQuery = parsedList.get(i);
			if (insertQuery.toString().startsWith("insert $concept isa Asset, has UID")) {
				foundConcept = true;
				// the next element should be the "match" command
				TypeQLQuery matchQuery = parsedList.get(i + 1);
				assertTrue(matchQuery.toString(),
						// should be an insert command with a "match" block
						matchQuery.asInsert().match().get()
								// it should contain reference to the data object's ID
								.toString().contains("DataObject_2"));
				break;
			}
		}
		assertTrue(foundConcept);

		/**
		 * We should also find declarations like the following:
		 * 
		 * <pre>
		 * insert $concept isa Service, has uid (...);
		 * match
		 * 		$bpmnEntity isa BPMN_Entity, has uid (...);
		 * 		$concept isa entity, has uid (...);
		 * insert $rel (bpmnEntity: $bpmnEntity, conceptualModel: $concept) isa BPMN_hasConceptualModelElement;
		 * </pre>
		 */
		foundConcept = false;
		for (int i = 0; i < parsedList.size(); i++) {
			TypeQLQuery insertQuery = parsedList.get(i);
			if (insertQuery.toString().startsWith("insert $concept isa Service, has UID")) {
				foundConcept = true;
				// the next element should be the "match" command
				TypeQLQuery matchQuery = parsedList.get(i + 1);
				assertTrue(matchQuery.toString(),
						// should be an insert command with a "match" block
						matchQuery.asInsert().match().get()
								// it should contain reference to the dataInputAssociation ID
								.toString().contains("DataInputAssociation_1"));
				break;
			}
		}
		assertTrue(foundConcept);

	}

	/**
	 * Test method for
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeSchema(java.io.OutputStream)}
	 * and
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeD(java.io.OutputStream)}
	 * for a simple BPMN model about data object.
	 * 
	 * @see #testEncodeSchema(String)
	 */
	@Test
	public final void testEncodeBPMNDataObjectWithoutMapping() throws Exception {

		// make sure the schema can be generated
		testEncodeSchema("/dataObject.bpmn");

		// generate the data
		EncoderImpl encoder = (EncoderImpl) EncoderImpl.getInstance();

		// disable mapping of BPMN to Concept model
		encoder.setMapBPMNToConceptualModel(false);

		encoder.loadInput(getClass().getResourceAsStream("/dataObject.bpmn"));
		String dataTypeQL;
		try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
			encoder.encodeData(out);
			dataTypeQL = out.toString();
		}

		logger.debug("Generated typeql data: \n{}", dataTypeQL);
		assertFalse(dataTypeQL.trim().isEmpty());

		// make sure the typeql data can be parsed
		List<TypeQLQuery> parsedList = TypeQL.parseQueries(dataTypeQL).collect(Collectors.toList());
		// there should be many commands
		assertFalse("Size = " + parsedList.size(), parsedList.isEmpty());
		// the 1st command should be an insert
		assertNotNull(parsedList.get(0).asInsert());

		// No need to check presence of relations that represent
		assertFalse(encoder.isMapBPMNToConceptualModel());

	}

	/**
	 * Test method for
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeSchema(java.io.OutputStream)}
	 * and
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeD(java.io.OutputStream)}
	 * for uavanet.bpmn.
	 * 
	 * @see #testEncodeSchema(String)
	 */
	@Test
	public final void testEncodeBPMNuavanet() throws Exception {

		// make sure the schema can be generated
		testEncodeSchema("/uavanet.bpmn");

		// generate the data
		EncoderImpl encoder = (EncoderImpl) EncoderImpl.getInstance();

		encoder.loadInput(getClass().getResourceAsStream("/uavanet.bpmn"));
		String dataTypeQL;
		try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
			encoder.encodeData(out);
			dataTypeQL = out.toString();
		}

		logger.debug("Generated typeql data: \n{}", dataTypeQL);
		assertFalse(dataTypeQL.trim().isEmpty());

		// make sure the typeql data can be parsed
		List<TypeQLQuery> parsedList = TypeQL.parseQueries(dataTypeQL).collect(Collectors.toList());
		// there should be many commands
		assertFalse("Size = " + parsedList.size(), parsedList.isEmpty());
		// the 1st command should be an insert
		assertNotNull(parsedList.get(0).asInsert());

	}

	/**
	 * Test method for
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeSchema(java.io.OutputStream)}
	 * and
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeD(java.io.OutputStream)}
	 * for sequence.bpmn.
	 * 
	 * @see #testEncodeSchema(String)
	 */
	@Test
	public final void testEncodeBPMNSequence() throws Exception {

		// make sure the schema can be generated
		testEncodeSchema("/sequence.bpmn");

		// generate the data
		EncoderImpl encoder = (EncoderImpl) EncoderImpl.getInstance();

		encoder.loadInput(getClass().getResourceAsStream("/sequence.bpmn"));
		String dataTypeQL;
		try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
			encoder.encodeData(out);
			dataTypeQL = out.toString();
		}

		logger.debug("Generated typeql data: \n{}", dataTypeQL);
		assertFalse(dataTypeQL.trim().isEmpty());

		// make sure the typeql data can be parsed
		List<TypeQLQuery> parsedList = TypeQL.parseQueries(dataTypeQL).collect(Collectors.toList());
		// there should be many commands
		assertFalse("Size = " + parsedList.size(), parsedList.isEmpty());
		// the 1st command should be an insert
		assertNotNull(parsedList.get(0).asInsert());

		/**
		 * We should also find declarations like the following:
		 * 
		 * <pre>
		 * insert $concept isa PrecedenceTask, has UID "http://c4i.gmu.edu/dalnim/sequence/#PrecedenceTask_SequenceFlow_1";
		 * match
		 * $bpmnEntity isa BPMN_Entity, has UID 'http://c4i.gmu.edu/dalnim/sequence/#SequenceFlow_1';
		 * $concept isa entity, has UID 'http://c4i.gmu.edu/dalnim/sequence/#PrecedenceTask_SequenceFlow_1';
		 * insert $rel (bpmnEntity: $bpmnEntity, conceptualModel: $concept) isa BPMN_hasConceptualModelElement;
		 * </pre>
		 */
		boolean foundConcept = false;
		for (int i = 0; i < parsedList.size(); i++) {
			TypeQLQuery insertQuery = parsedList.get(i);
			if (insertQuery.toString().startsWith("insert $concept isa PrecedenceTask, has UID")) {
				foundConcept = true;
				// the next element should be the "match" command
				TypeQLQuery matchQuery = parsedList.get(i + 1);
				assertTrue(matchQuery.toString(),
						// should be an insert command with a "match" block
						matchQuery.asInsert().match().get()
								// it should contain reference to the sequenceFlow ID
								.toString().contains("SequenceFlow_1"));
				break;
			}
		}
		assertTrue(foundConcept);
	}

	/**
	 * Test method for
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeSchema(java.io.OutputStream)}
	 * and
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeD(java.io.OutputStream)}
	 * for parallelGateway.bpmn.
	 * 
	 * @see #testEncodeSchema(String)
	 */
	@Test
	public final void testEncodeBPMNParallel() throws Exception {

		// make sure the schema can be generated
		testEncodeSchema("/parallelGateway.bpmn");

		// generate the data
		EncoderImpl encoder = (EncoderImpl) EncoderImpl.getInstance();

		encoder.loadInput(getClass().getResourceAsStream("/parallelGateway.bpmn"));
		String dataTypeQL;
		try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
			encoder.encodeData(out);
			dataTypeQL = out.toString();
		}

		logger.debug("Generated typeql data: \n{}", dataTypeQL);
		assertFalse(dataTypeQL.trim().isEmpty());

		// make sure the typeql data can be parsed
		List<TypeQLQuery> parsedList = TypeQL.parseQueries(dataTypeQL).collect(Collectors.toList());
		// there should be many commands
		assertFalse("Size = " + parsedList.size(), parsedList.isEmpty());
		// the 1st command should be an insert
		assertNotNull(parsedList.get(0).asInsert());

		/**
		 * We should also find declarations like the following:
		 * 
		 * <pre>
		 * insert $concept isa ANDPrecedenceTaskList, has UID (...);
		 * match
		 * $bpmnEntity isa BPMN_Entity, has UID  (...);
		 * $concept isa entity, has UID (...);
		 * insert $rel (bpmnEntity: $bpmnEntity, conceptualModel: $concept) isa BPMN_hasConceptualModelElement;
		 * </pre>
		 */
		boolean foundConcept = false;
		for (int i = 0; i < parsedList.size(); i++) {
			TypeQLQuery insertQuery = parsedList.get(i);
			if (insertQuery.toString().startsWith("insert $concept isa ANDPrecedenceTaskList, has UID")) {
				// the next element should be the "match" command
				TypeQLQuery matchQuery = parsedList.get(i + 1);
				// should be an insert command with a "match" block
				if (matchQuery.asInsert().match().get()
						// it should contain reference to the parallelGateway ID
						.toString().contains("ParallelGateway_1")) {
					foundConcept = true;
					break;
				}
			}
		}
		assertTrue(foundConcept);
	}

	/**
	 * Test method for
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeSchema(java.io.OutputStream)}
	 * and
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeD(java.io.OutputStream)}
	 * for gatewayChain.bpmn.
	 * 
	 * @see #testEncodeSchema(String)
	 */
	@Test
	public final void testEncodeBPMNGatewayChain() throws Exception {

		// make sure the schema can be generated
		testEncodeSchema("/gatewayChain.bpmn");

		// generate the data
		EncoderImpl encoder = (EncoderImpl) EncoderImpl.getInstance();

		encoder.loadInput(getClass().getResourceAsStream("/gatewayChain.bpmn"));
		String dataTypeQL;
		try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
			encoder.encodeData(out);
			dataTypeQL = out.toString();
		}

		logger.debug("Generated typeql data: \n{}", dataTypeQL);
		assertFalse(dataTypeQL.trim().isEmpty());

		// make sure the typeql data can be parsed
		List<TypeQLQuery> parsedList = TypeQL.parseQueries(dataTypeQL).collect(Collectors.toList());
		// there should be many commands
		assertFalse("Size = " + parsedList.size(), parsedList.isEmpty());
		// the 1st command should be an insert
		assertNotNull(parsedList.get(0).asInsert());

		/**
		 * We should also find declarations like the following:
		 * 
		 * <pre>
		 * insert $concept isa ORPrecedenceTaskList, has UID (...);
		 * match
		 * $bpmnEntity isa BPMN_Entity, has UID  (...);
		 * $concept isa entity, has UID (...);
		 * insert $rel (bpmnEntity: $bpmnEntity, conceptualModel: $concept) isa BPMN_hasConceptualModelElement;
		 * </pre>
		 */
		boolean foundConcept = false;
		for (int i = 0; i < parsedList.size(); i++) {
			TypeQLQuery insertQuery = parsedList.get(i);
			if (insertQuery.toString().startsWith("insert $concept isa ORPrecedenceTaskList, has UID")) {
				// the next element should be the "match" command
				TypeQLQuery matchQuery = parsedList.get(i + 1);
				// should be an insert command with a "match" block
				if (matchQuery.asInsert().match().get()
						// it should contain reference to the inclusiveGateway ID
						.toString().contains("InclusiveGateway_")) {
					foundConcept = true;
					break;
				}
			}
		}
		assertTrue(foundConcept);
		foundConcept = false;
		for (int i = 0; i < parsedList.size(); i++) {
			TypeQLQuery insertQuery = parsedList.get(i);
			if (insertQuery.toString().startsWith("insert $concept isa ORPrecedenceTaskList, has UID")) {
				// the next element should be the "match" command
				TypeQLQuery matchQuery = parsedList.get(i + 1);
				// should be an insert command with a "match" block
				if (matchQuery.asInsert().match().get()
						// it should contain reference to the complexGateway ID
						.toString().contains("ComplexGateway_")) {
					foundConcept = true;
					break;
				}
			}
		}
		assertTrue(foundConcept);
	}

}
