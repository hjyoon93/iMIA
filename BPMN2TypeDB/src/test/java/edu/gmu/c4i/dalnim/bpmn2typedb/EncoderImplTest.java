package edu.gmu.c4i.dalnim.bpmn2typedb;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;

import java.io.ByteArrayOutputStream;
import java.text.ParseException;
import java.util.Collection;
import java.util.HashSet;
import java.util.List;
import java.util.Optional;
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
import com.vaticle.typeql.lang.pattern.schema.Rule;
import com.vaticle.typeql.lang.pattern.variable.BoundVariable;
import com.vaticle.typeql.lang.pattern.variable.ThingVariable;
import com.vaticle.typeql.lang.pattern.variable.TypeVariable;
import com.vaticle.typeql.lang.query.TypeQLDefine;
import com.vaticle.typeql.lang.query.TypeQLMatch.Unfiltered;
import com.vaticle.typeql.lang.query.TypeQLQuery;

import edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl;

/**
 * Default test unit for {@link EncoderImpl}
 * 
 * @author shou
 */
public class EncoderImplTest {

	private static Logger logger = LoggerFactory.getLogger(EncoderImplTest.class);

	private Collection<String> conceptModelKeywords = new HashSet<>();
	{
		getConceptModelKeywords().add("MIAEntity");
		getConceptModelKeywords().add("Mission");
		getConceptModelKeywords().add(" Task");
		getConceptModelKeywords().add("Performer");
		getConceptModelKeywords().add("Service");
		getConceptModelKeywords().add("Asset");
		getConceptModelKeywords().add("PrecedenceTask");
		getConceptModelKeywords().add("ORPrecedenceTaskList");
		getConceptModelKeywords().add("ANDPrecedenceTaskList");
		getConceptModelKeywords().add("isCompoundBy");
		getConceptModelKeywords().add("isPerformedBy");
		getConceptModelKeywords().add("provides");
		getConceptModelKeywords().add("isCompoundBySetOfTask");
		getConceptModelKeywords().add("isPrecededBySetOfTask");
		getConceptModelKeywords().add("BPMN_hasConceptualModelElement");
	};

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
	 * Delegates to {@link #testEncodeSchema(String, boolean)} with true as its
	 * second argument.
	 */
	public String testEncodeSchema(String resource) throws Exception {
		return this.testEncodeSchema(resource, true);
	}

	/**
	 * @param resource        : location of BPMN file to load.
	 * @param hasConceptModel : if true, mappings to concept model will be
	 *                        generated. If false, the mappings will not be
	 *                        generated and ensured to be absent.
	 * 
	 * @return the typeql script
	 * 
	 * @see #testEncodeBPMNSchema()
	 */
	public String testEncodeSchema(String resource, boolean hasConceptModel) throws Exception {
		EncoderImpl encoder = (EncoderImpl) EncoderImpl.getInstance();
		assertNotNull(encoder);
		encoder.setMapBPMNToConceptualModel(hasConceptModel);

		encoder.setRunSanityCheck(true);
		encoder.loadInput(getClass().getResourceAsStream(resource));

		ByteArrayOutputStream out = new ByteArrayOutputStream();
		encoder.encodeSchema(out);
		out.flush();
		assertEquals(hasConceptModel, encoder.isMapBPMNToConceptualModel());

		String schema = out.toString();
//		logger.debug("Generated typeql schema: \n{}", schema);

		assertFalse(schema.trim().isEmpty());

		// make sure the typeql schema can be parsed
		assertTrue(encoder.checkDefinitionReferences(schema));

		if (!hasConceptModel) {
			checkAbsenseOfConceptModelInSchema(schema);
		}

		return schema;
	}

	/**
	 * Makes sure the definitions in the TypeQL schema will not contain the
	 * entities/relations in the concept model.
	 * 
	 * @param schema
	 * 
	 * @see #checkAbsenseOfConceptModelInData(List)
	 * @see #getConceptModelKeywords()
	 */
	public void checkAbsenseOfConceptModelInSchema(String schema) {

		TypeQLDefine define = TypeQL.parseQuery(schema).asDefine();

		for (TypeVariable variable : define.variables()) {
			for (String keyword : getConceptModelKeywords()) {
				assertFalse("Keyword = " + keyword + "; query = " + variable.toString(),
						variable.toString().contains(keyword));
			}

		}

		for (Rule rule : define.rules()) {
			for (String keyword : getConceptModelKeywords()) {
				assertFalse("Keyword = " + keyword + "; query = " + rule.toString(), rule.toString().contains(keyword));
			}
		}
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

		// test with default configuration
		testEncodeSchema("/simple.bpmn");
		testEncodeSchema("/UAV_material_transport_eclipse.bpmn");

		// also test without the mappings to concept model
		testEncodeSchema("/simple.bpmn", false);
		testEncodeSchema("/UAV_material_transport_eclipse.bpmn", false);

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
	 * for simple.bpmn, but without the mapping to conceptual model.
	 */
	@Test
	public final void testEncodeDataSimpleNoMapping() throws Exception {
		EncoderImpl encoder = (EncoderImpl) EncoderImpl.getInstance();
		encoder.setMapBPMNToConceptualModel(false);

		encoder.loadInput(getClass().getResourceAsStream("/simple.bpmn"));

		ByteArrayOutputStream out = new ByteArrayOutputStream();
		encoder.encodeData(out);
		out.flush();

		assertFalse(encoder.isMapBPMNToConceptualModel());

		String typeql = out.toString();
		logger.debug("Generated typeql data: \n{}", typeql);

		assertFalse(typeql.trim().isEmpty());

		// make sure the typeql schema can be parsed
		List<TypeQLQuery> parsedList = TypeQL.parseQueries(typeql).collect(Collectors.toList());
		// there should be many commands
		assertFalse("Size = " + parsedList.size(), parsedList.isEmpty());
		// the 1st command should be an insert
		assertNotNull(parsedList.get(0).asInsert());

		// make sure it does not use any of the classes/relations in the concept model
		checkAbsenseOfConceptModelInData(parsedList);
	}

	/**
	 * This method will make sure some relevant entities and relationships of the
	 * concept model are NOT present in the provided query list.
	 * 
	 * The following should be present anyway:
	 * <p>
	 * UID sub attribute, value string;
	 * </p>
	 * 
	 * The following are the relevant entities/relations in the conceptual model
	 * which should NOT be present when
	 * {@link EncoderImpl#isMapBPMNToConceptualModel()} is false:
	 * 
	 * <pre>
	 * MIAEntity sub entity, owns UID @key;
	 * Mission sub MIAEntity;
	 * Task sub MIAEntity;
	 * Performer sub MIAEntity;
	 * Service sub Performer;
	 * Asset sub MIAEntity;
	 * PrecedenceTask sub MIAEntity;
	 * ORPrecedenceTaskList sub PrecedenceTask;
	 * ANDPrecedenceTaskList sub PrecedenceTask;
	 * isCompoundBy sub relation, relates mission, relates task;
	 * Mission plays isCompoundBy:mission;
	 * Task plays isCompoundBy:task;
	 * isPerformedBy sub relation, relates task, relates performer;
	 * Task plays isPerformedBy:task;
	 * Performer plays isPerformedBy:performer;
	 * provides sub relation, relates asset, relates service;
	 * Asset plays provides:asset;
	 * Service plays provides:service;
	 * isCompoundBySetOfTask sub relation, relates precedence_task, relates task;
	 * PrecedenceTask plays isCompoundBySetOfTask:precedence_task;
	 * Task plays isCompoundBySetOfTask:task;
	 * isPrecededBySetOfTask sub relation, relates precedence_task, relates task;
	 * PrecedenceTask plays isPrecededBySetOfTask:precedence_task;
	 * Task plays isPrecededBySetOfTask:task;
	 * </pre>
	 * 
	 * BPMN_hasConceptualModelElement should also be absent.
	 * 
	 * @see #checkAbsenseOfConceptModelInSchema(String)
	 * @see #getConceptModelKeywords()
	 */
	public void checkAbsenseOfConceptModelInData(List<TypeQLQuery> parsed) {
		for (TypeQLQuery query : parsed) {
			for (ThingVariable<?> var : query.asInsert().variables()) {
				if (var.isa().isPresent()) {
					for (String keyword : getConceptModelKeywords()) {
						assertFalse("Keyword = " + keyword + "; query = " + query.toString(),
								var.isa().get().toString().contains(keyword));
					}
				}
			}
			Optional<Unfiltered> match = query.asInsert().match();
			if (match.isPresent()) {
				for (BoundVariable var : match.get().variables()) {
					for (String keyword : getConceptModelKeywords()) {
						if (var.isType()) {
							assertFalse("Keyword = " + keyword + "; query = " + query.toString(),
									var.asType().toString().contains(keyword));
						} else if (var.isThing() && var.asThing().isa().isPresent()) {
							assertFalse("Keyword = " + keyword + "; query = " + query.toString(),
									var.asThing().isa().get().toString().contains(keyword));
						}
					}
				}
			}
		}
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
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeData(java.io.OutputStream)}
	 * for UAV_material_transport_eclipse.bpmn with
	 * {@link EncoderImpl#setMapBPMNToConceptualModel(boolean)} set to false.
	 */
	@Test
	public final void testEncodeDataUAVNoMapping() throws Exception {
		EncoderImpl encoder = (EncoderImpl) EncoderImpl.getInstance();
		encoder.setMapBPMNToConceptualModel(false);

		encoder.loadInput(getClass().getResourceAsStream("/UAV_material_transport_eclipse.bpmn"));

		ByteArrayOutputStream out = new ByteArrayOutputStream();
		encoder.encodeData(out);
		out.flush();
		assertFalse(encoder.isMapBPMNToConceptualModel());

		String typeql = out.toString();
		logger.debug("Generated typeql data: \n{}", typeql);

		assertFalse(typeql.trim().isEmpty());

		// make sure the typeql can be parsed
		List<TypeQLQuery> parsedList = TypeQL.parseQueries(typeql).collect(Collectors.toList());
		// there should be many commands
		assertFalse("Size = " + parsedList.size(), parsedList.isEmpty());
		// the 1st command should be an insert
		assertNotNull(parsedList.get(0).asInsert());

		checkAbsenseOfConceptModelInData(parsedList);
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
		testEncodeSchema("/dataObject.bpmn", false);

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
	 * for uavanet2.bpmn.
	 * 
	 * @see #testEncodeSchema(String)
	 */
	@Test
	public final void testEncodeBPMNuavanet2() throws Exception {

		// make sure the schema can be generated
		testEncodeSchema("/uavanet2.bpmn");

		// generate the data
		EncoderImpl encoder = (EncoderImpl) EncoderImpl.getInstance();

		encoder.loadInput(getClass().getResourceAsStream("/uavanet2.bpmn"));
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
	 * for sequence.bpmn, but with
	 * {@link EncoderImpl#setMapBPMNToConceptualModel(boolean)} set to false.
	 * 
	 * @see #testEncodeSchema(String)
	 */
	@Test
	public final void testEncodeBPMNSequenceNoMapping() throws Exception {

		// make sure the schema can be generated
		testEncodeSchema("/sequence.bpmn", false);

		// generate the data
		EncoderImpl encoder = (EncoderImpl) EncoderImpl.getInstance();
		encoder.setMapBPMNToConceptualModel(false);

		encoder.loadInput(getClass().getResourceAsStream("/sequence.bpmn"));
		String dataTypeQL;
		try (ByteArrayOutputStream out = new ByteArrayOutputStream()) {
			encoder.encodeData(out);
			dataTypeQL = out.toString();
		}
		assertFalse(encoder.isMapBPMNToConceptualModel());

		logger.debug("Generated typeql data: \n{}", dataTypeQL);
		assertFalse(dataTypeQL.trim().isEmpty());

		// make sure the typeql data can be parsed
		List<TypeQLQuery> parsedList = TypeQL.parseQueries(dataTypeQL).collect(Collectors.toList());
		// there should be many commands
		assertFalse("Size = " + parsedList.size(), parsedList.isEmpty());
		// the 1st command should be an insert
		assertNotNull(parsedList.get(0).asInsert());

		checkAbsenseOfConceptModelInData(parsedList);

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

	/**
	 * Test method for
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeSchema(java.io.OutputStream)}
	 * and
	 * {@link edu.gmu.c4i.dalnim.bpmn2typedb.encoder.EncoderImpl#encodeD(java.io.OutputStream)}
	 * for messageFlow.bpmn.
	 * 
	 * @see #testEncodeSchema(String)
	 */
	@Test
	public final void testEncodeBPMNMessageFlow() throws Exception {

		// make sure the schema can be generated
		testEncodeSchema("/messageFlow.bpmn");

		// generate the data
		EncoderImpl encoder = (EncoderImpl) EncoderImpl.getInstance();

		encoder.loadInput(getClass().getResourceAsStream("/messageFlow.bpmn"));
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
		 * insert $x isa BPMN_messageFlow,
		 * 	has BPMNattrib_targetRef "Activity_1m6lr6g",
		 * 	has BPMNattrib_name "Request",
		 * 	has BPMNattrib_id "Flow_0915wqb",
		 * 	has BPMNattrib_sourceRef "Participant_0thms36",
		 * 	has UID "http://bpmn.io/schema/bpmn/#Flow_0915wqb";
		 * match
		 * 	$parent isa BPMN_Entity, has UID "http://bpmn.io/schema/bpmn/#Collaboration_0njkluv";
		 * 	$child isa BPMN_Entity, has UID "http://bpmn.io/schema/bpmn/#Flow_0915wqb";
		 * 	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
		 * </pre>
		 */
		boolean foundConcept = false;
		for (int i = 0; i < parsedList.size(); i++) {
			TypeQLQuery insertQuery = parsedList.get(i);
			if (insertQuery.toString().startsWith("insert $x isa BPMN_messageFlow")) {
				// the next element should be the "match" command
				TypeQLQuery matchQuery = parsedList.get(i + 1);
				// should be an insert command with a "match" block
				if (matchQuery.asInsert().match().get()
						// it should contain reference to the collaboration ID
						.toString().contains("Collaboration_1")) {
					foundConcept = true;
					break;
				}
			}
		}
		assertTrue(foundConcept);

		/**
		 * <pre>
		 * insert $concept isa Asset, has UID "http://www.c4i.gmu.edu/dalnim/messageFlow/#Asset_MessageFlow_1";
		 * match
		 * 	$bpmnEntity isa BPMN_Entity, has UID 'http://www.c4i.gmu.edu/dalnim/messageFlow/#MessageFlow_1';
		 * 	$concept isa entity, has UID 'http://www.c4i.gmu.edu/dalnim/messageFlow/#Asset_MessageFlow_1';
		 * insert $rel (bpmnEntity: $bpmnEntity, conceptualModel: $concept) isa BPMN_hasConceptualModelElement;
		 * </pre>
		 */
		foundConcept = false;
		for (int i = 0; i < parsedList.size(); i++) {
			TypeQLQuery insertQuery = parsedList.get(i);
			if (insertQuery.toString().startsWith("insert $concept isa Asset")) {
				// the next element should be the "match" command
				TypeQLQuery matchQuery = parsedList.get(i + 1);
				// should be an insert command with a "match" block
				if (matchQuery.asInsert().match().get()
						// it should contain reference to this UID
						.toString().contains("MessageFlow_1")) {
					foundConcept = true;
					break;
				}
			}
		}
		assertTrue(foundConcept);

		/**
		 * <pre>
		 * insert $x isa BPMN_collaboration,
		 * 	has BPMNattrib_isClosed "false",
		 * 	has BPMNattrib_name "Collaboration 1",
		 * 	has BPMNattrib_id "Collaboration_1",
		 * 	has UID "http://www.c4i.gmu.edu/dalnim/messageFlow/#Collaboration_1";
		 * match
		 * 	$parent isa BPMN_Entity, has UID "http://www.c4i.gmu.edu/dalnim/messageFlow/#Definitions_1";
		 * 	$child isa BPMN_Entity, has UID "http://www.c4i.gmu.edu/dalnim/messageFlow/#Collaboration_1";
		 * insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
		 * </pre>
		 */
		foundConcept = false;
		for (int i = 0; i < parsedList.size(); i++) {
			TypeQLQuery insertQuery = parsedList.get(i);
			if (insertQuery.toString().startsWith("insert $x isa BPMN_collaboration")) {
				// the next element should be the "match" command
				TypeQLQuery matchQuery = parsedList.get(i + 1);
				// should be an insert command with a "match" block
				if (matchQuery.asInsert().match().get()
						// it should contain reference to the root
						.toString().contains("Definitions_1")) {
					foundConcept = true;
					break;
				}
			}
		}
		assertTrue(foundConcept);

		/**
		 * <pre>
		 * insert $concept isa Service, has UID "http://www.c4i.gmu.edu/dalnim/messageFlow/#Service_Collaboration_1";
		 * match
		 * 	$bpmnEntity isa BPMN_Entity, has UID 'http://www.c4i.gmu.edu/dalnim/messageFlow/#Collaboration_1';
		 * 	$concept isa entity, has UID 'http://www.c4i.gmu.edu/dalnim/messageFlow/#Service_Collaboration_1';
		 * insert $rel (bpmnEntity: $bpmnEntity, conceptualModel: $concept) isa BPMN_hasConceptualModelElement;
		 * </pre>
		 */
		foundConcept = false;
		for (int i = 0; i < parsedList.size(); i++) {
			TypeQLQuery insertQuery = parsedList.get(i);
			if (insertQuery.toString().startsWith("insert $concept isa Service")) {
				// the next element should be the "match" command
				TypeQLQuery matchQuery = parsedList.get(i + 1);
				// should be an insert command with a "match" block
				if (matchQuery.asInsert().match().get()
						// it should contain reference to this UID
						.toString().contains("Collaboration_1")) {
					foundConcept = true;
					break;
				}
			}
		}
		assertTrue(foundConcept);
	}

	/**
	 * @return the keywords (entities and relations) that are part of the concept
	 *         model.
	 * 
	 * @see #checkAbsenseOfConceptModelInData(List)
	 * @see #checkAbsenseOfConceptModelInSchema(String)
	 */
	public Collection<String> getConceptModelKeywords() {
		return conceptModelKeywords;
	}

	/**
	 * @param keywords : the keywords (entities and relations) that are part of the
	 *                 concept model.
	 * 
	 * @see #checkAbsenseOfConceptModelInData(List)
	 * @see #checkAbsenseOfConceptModelInSchema(String)
	 */
	public void setConceptModelKeywords(Collection<String> keywords) {
		this.conceptModelKeywords = keywords;
	}

}
