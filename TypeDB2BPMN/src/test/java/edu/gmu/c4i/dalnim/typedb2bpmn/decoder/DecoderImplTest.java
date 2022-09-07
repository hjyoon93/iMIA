package edu.gmu.c4i.dalnim.typedb2bpmn.decoder;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertTrue;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Collection;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import org.camunda.bpm.model.bpmn.Bpmn;
import org.camunda.bpm.model.bpmn.BpmnModelInstance;
import org.camunda.bpm.model.bpmn.impl.instance.Incoming;
import org.camunda.bpm.model.bpmn.impl.instance.Outgoing;
import org.camunda.bpm.model.bpmn.impl.instance.SourceRef;
import org.camunda.bpm.model.bpmn.instance.BaseElement;
import org.camunda.bpm.model.bpmn.instance.Collaboration;
import org.camunda.bpm.model.bpmn.instance.DataInputAssociation;
import org.camunda.bpm.model.bpmn.instance.DataObject;
import org.camunda.bpm.model.bpmn.instance.Definitions;
import org.camunda.bpm.model.bpmn.instance.EndEvent;
import org.camunda.bpm.model.bpmn.instance.ExclusiveGateway;
import org.camunda.bpm.model.bpmn.instance.IoSpecification;
import org.camunda.bpm.model.bpmn.instance.Lane;
import org.camunda.bpm.model.bpmn.instance.LaneSet;
import org.camunda.bpm.model.bpmn.instance.ManualTask;
import org.camunda.bpm.model.bpmn.instance.ParallelGateway;
import org.camunda.bpm.model.bpmn.instance.Participant;
import org.camunda.bpm.model.bpmn.instance.Performer;
import org.camunda.bpm.model.bpmn.instance.Process;
import org.camunda.bpm.model.bpmn.instance.ReceiveTask;
import org.camunda.bpm.model.bpmn.instance.SendTask;
import org.camunda.bpm.model.bpmn.instance.SequenceFlow;
import org.camunda.bpm.model.bpmn.instance.ServiceTask;
import org.camunda.bpm.model.bpmn.instance.StartEvent;
import org.camunda.bpm.model.bpmn.instance.UserTask;
import org.camunda.bpm.model.bpmn.instance.bpmndi.BpmnDiagram;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.vaticle.typedb.client.TypeDB;
import com.vaticle.typedb.client.api.TypeDBClient;
import com.vaticle.typedb.client.api.TypeDBSession;
import com.vaticle.typedb.client.api.TypeDBTransaction;
import com.vaticle.typedb.client.api.answer.ConceptMap;
import com.vaticle.typedb.client.api.query.QueryFuture;
import com.vaticle.typeql.lang.TypeQL;
import com.vaticle.typeql.lang.query.TypeQLQuery;

/**
 * Unit test for {@link DecoderImpl}. A TypeDB database must be available at
 * localhost 1729 to work.
 * 
 * @author shou
 */
//@Ignore("A TypeDB instance must be running in localhos:1729. Remove this annotation if TypeDB is running fine.")
public class DecoderImplTest {

	private static Logger logger = LoggerFactory.getLogger(DecoderImplTest.class);

	private static boolean isRunSimpleBPMN = true;
	private static boolean isRunDataObjectBPMN = true;
	private static boolean isRunGMUUAVBPMN = true;
	private static boolean isRunUavanetBPMN = true;

	private static String address = "localhost:1729";
	private static String databaseName = DecoderImplTest.class.getName();

	@BeforeClass
	public static void setUpBeforeClass() throws Exception {

		TypeDBClient client = TypeDB.coreClient(address);

		// delete the database if it exists
		if (client.databases().contains(databaseName)) {
			client.databases().get(databaseName).delete();
		}
		// (re)create the database
		client.databases().create(databaseName);

		// populate the test database

		// load the conceptual model schema
		try (TypeDBSession session = client.session(databaseName, TypeDBSession.Type.SCHEMA)) {
			try (TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.WRITE)) {
				Stream<TypeQLQuery> queries = TypeQL.parseQueries(
						Files.readString(Path.of(DecoderImplTest.class.getResource("/concept_model.tql").toURI())));
				for (TypeQLQuery query : queries.collect(Collectors.toList())) {
					QueryFuture<Void> response = transaction.query().define(query.asDefine());
					// wait for the transaction to finish
					response.get();
					logger.debug("Processed query {}", query);
				}
				logger.debug("Committing transaction...");
				transaction.commit();
			}
			logger.debug("Loaded conceptual model.");
		}

		// set up schema from file
		if (isRunSimpleBPMN()) {
			try (TypeDBSession session = client.session(databaseName, TypeDBSession.Type.SCHEMA)) {
				try (TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.WRITE)) {
					Stream<TypeQLQuery> queries = TypeQL.parseQueries(Files
							.readString(Path.of(DecoderImplTest.class.getResource("/simple_BPMN_schema.tql").toURI())));
					for (TypeQLQuery query : queries.collect(Collectors.toList())) {
						QueryFuture<Void> response = transaction.query().define(query.asDefine());
						// wait for the transaction to finish
						response.get();
						logger.debug("Processed query {}", query);
					}
					logger.debug("Committing transaction...");
					transaction.commit();
				}
				logger.debug("Generated schema.");
			}
		}
		// set up 2nd schema from file
		if (isRunDataObjectBPMN()) {
			try (TypeDBSession session = client.session(databaseName, TypeDBSession.Type.SCHEMA)) {
				try (TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.WRITE)) {
					Stream<TypeQLQuery> queries = TypeQL.parseQueries(Files.readString(
							Path.of(DecoderImplTest.class.getResource("/DataObject_BPMN_Schema.tql").toURI())));
					for (TypeQLQuery query : queries.collect(Collectors.toList())) {
						QueryFuture<Void> response = transaction.query().define(query.asDefine());
						// wait for the transaction to finish
						response.get();
						logger.debug("Processed query {}", query);
					}
					logger.debug("Committing transaction...");
					transaction.commit();
				}
				logger.debug("Generated schema.");
			}
		}
		// set up 3rd schema from file
		if (isRunGMUUAVBPMN()) {
			try (TypeDBSession session = client.session(databaseName, TypeDBSession.Type.SCHEMA)) {
				try (TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.WRITE)) {
					Stream<TypeQLQuery> queries = TypeQL.parseQueries(Files
							.readString(Path.of(DecoderImplTest.class.getResource("/UAV_BPMN_schema.tql").toURI())));
					for (TypeQLQuery query : queries.collect(Collectors.toList())) {
						QueryFuture<Void> response = transaction.query().define(query.asDefine());
						// wait for the transaction to finish
						response.get();
						logger.debug("Processed query {}", query);
					}
					logger.debug("Committing transaction...");
					transaction.commit();
				}
				logger.debug("Generated schema.");
			}
		}
		// set up 4th schema from file
		if (isRunUavanetBPMN()) {
			try (TypeDBSession session = client.session(databaseName, TypeDBSession.Type.SCHEMA)) {
				try (TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.WRITE)) {
					Stream<TypeQLQuery> queries = TypeQL.parseQueries(Files.readString(
							Path.of(DecoderImplTest.class.getResource("/uavanet_BPMN_schema.tql").toURI())));
					for (TypeQLQuery query : queries.collect(Collectors.toList())) {
						QueryFuture<Void> response = transaction.query().define(query.asDefine());
						// wait for the transaction to finish
						response.get();
						logger.debug("Processed query {}", query);
					}
					logger.debug("Committing transaction...");
					transaction.commit();
				}
				logger.debug("Generated schema.");
			}
		}

		// set up the data from file
		if (isRunSimpleBPMN()) {
			try (TypeDBSession session = client.session(databaseName, TypeDBSession.Type.DATA)) {
				try (TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.WRITE)) {
					Stream<TypeQLQuery> queries = TypeQL.parseQueries(Files
							.readString(Path.of(DecoderImplTest.class.getResource("/simple_BPMN_data.tql").toURI())));
					for (TypeQLQuery query : queries.collect(Collectors.toList())) {
						Stream<ConceptMap> response = transaction.query().insert(query.asInsert());
						long count = response.count();
						assertTrue("Count = " + count, count > 0);
						logger.debug("Processed query {}", query);
					}
					logger.debug("Committing transaction...");
					transaction.commit();
				}
				logger.debug("Generated data.");
			}
		}
		// set up the 2nd data from file
		if (isRunDataObjectBPMN()) {
			try (TypeDBSession session = client.session(databaseName, TypeDBSession.Type.DATA)) {
				try (TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.WRITE)) {
					Stream<TypeQLQuery> queries = TypeQL.parseQueries(Files.readString(
							Path.of(DecoderImplTest.class.getResource("/DataObject_BPMN_Data.tql").toURI())));
					for (TypeQLQuery query : queries.collect(Collectors.toList())) {
						Stream<ConceptMap> response = transaction.query().insert(query.asInsert());
						long count = response.count();
						assertTrue("Count = " + count, count > 0);
						logger.debug("Processed query {}", query);
					}
					logger.debug("Committing transaction...");
					transaction.commit();
				}
				logger.debug("Generated data.");
			}
		}
		// set up the 3rd data from file
		if (isRunGMUUAVBPMN()) {
			try (TypeDBSession session = client.session(databaseName, TypeDBSession.Type.DATA)) {
				try (TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.WRITE)) {
					Stream<TypeQLQuery> queries = TypeQL.parseQueries(
							Files.readString(Path.of(DecoderImplTest.class.getResource("/UAV_BPMN_data.tql").toURI())));
					for (TypeQLQuery query : queries.collect(Collectors.toList())) {
						Stream<ConceptMap> response = transaction.query().insert(query.asInsert());
						long count = response.count();
						assertTrue("Count = " + count, count > 0);
						logger.debug("Processed query {}", query);
					}
					logger.debug("Committing transaction...");
					transaction.commit();
				}
				logger.debug("Generated data.");
			}
		}
		// set up the 4th data from file
		if (isRunUavanetBPMN()) {
			try (TypeDBSession session = client.session(databaseName, TypeDBSession.Type.DATA)) {
				try (TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.WRITE)) {
					Stream<TypeQLQuery> queries = TypeQL.parseQueries(Files
							.readString(Path.of(DecoderImplTest.class.getResource("/uavanet_BPMN_data.tql").toURI())));
					for (TypeQLQuery query : queries.collect(Collectors.toList())) {
						Stream<ConceptMap> response = transaction.query().insert(query.asInsert());
						long count = response.count();
						assertTrue("Count = " + count, count > 0);
						logger.debug("Processed query {}", query);
					}
					logger.debug("Committing transaction...");
					transaction.commit();
				}
				logger.debug("Generated data.");
			}
		}

		// make sure we close the connection
		client.close();
	}

	@AfterClass
	public static void tearDownAfterClass() throws Exception {
		// clean the database after execution
		TypeDBClient client = TypeDB.coreClient(address);
		if (client.databases().contains(databaseName)) {
			client.databases().get(databaseName).delete();
		}
	}

	@Before
	public void setUp() throws Exception {
	}

	@After
	public void tearDown() throws Exception {
	}

	/**
	 * Test method of {@link DecoderImpl#saveBPMN(java.io.OutputStream)} with a
	 * simple BPMN model.
	 */
	@Test
	public final void testSaveBPMNSimple() throws Exception {
		if (!isRunSimpleBPMN()) {
			logger.warn("Skipping testSaveBPMNSimple...");
			return;
		}

		// the object to test
		DecoderImpl decoder = (DecoderImpl) DecoderImpl.getInstance();

		// the address of TypeDB
		decoder.setTypeDBAddress(address);

		// name of the test database
		decoder.setDatabaseName(databaseName);

		// the UID of the BPMN node to query
		decoder.setRootUID("https://camunda.org/examples/#definitions");

		ByteArrayOutputStream stream = new ByteArrayOutputStream();
		decoder.saveBPMN(stream);
		stream.flush();
		stream.close();
		String result = stream.toString();

		logger.debug("Result: \n{}", result);

		assertFalse(result, result.trim().isEmpty());

		// parse result as BPMN
		BpmnModelInstance bpmn = Bpmn.readModelFromStream(new ByteArrayInputStream(result.getBytes()));
		assertNotNull(bpmn);

		// load the bpmn definitions (the root node)
		Definitions definitions = bpmn.getDefinitions();
		assertNotNull(definitions);

		// check namespaces
		assertEquals("http://www.omg.org/spec/BPMN/20100524/MODEL",
				bpmn.getDocument().getRootElement().getNamespaceURI());
		assertEquals("https://camunda.org/examples", definitions.getAttributeValue("targetNamespace"));

		// check process
		Collection<Process> processes = definitions.getChildElementsByType(Process.class);
		assertEquals(processes.toString(), 1, processes.size());
		Process process = processes.iterator().next();

		// content of process must be:
		// startEvent->sequenceFlow->userTask->sequenceFlow->endEvent

		Collection<BaseElement> processContent = process.getChildElementsByType(BaseElement.class);
		assertEquals(processContent.toString(), 5, processContent.size());

		// startEvent
		Collection<StartEvent> startEvents = process.getChildElementsByType(StartEvent.class);
		assertEquals(startEvents.toString(), 1, startEvents.size());
		assertEquals(startEvents.toString(), "start", startEvents.iterator().next().getId());
		Collection<Outgoing> outgoing = startEvents.iterator().next().getChildElementsByType(Outgoing.class);
		assertEquals(outgoing.toString(), 1, outgoing.size());
		assertEquals(outgoing.toString(), "flow1", outgoing.iterator().next().getTextContent());

		// endEvent
		Collection<EndEvent> endEvents = process.getChildElementsByType(EndEvent.class);
		assertEquals(endEvents.toString(), 1, endEvents.size());
		assertEquals(endEvents.toString(), "end", endEvents.iterator().next().getId());
		Collection<Incoming> incoming = endEvents.iterator().next().getChildElementsByType(Incoming.class);
		assertEquals(incoming.toString(), 1, incoming.size());
		assertEquals(incoming.toString(), "flow2", incoming.iterator().next().getTextContent());

		// userTask
		Collection<UserTask> userTasks = process.getChildElementsByType(UserTask.class);
		assertEquals(userTasks.toString(), 1, userTasks.size());
		assertEquals(userTasks.toString(), "task", userTasks.iterator().next().getId());
		assertEquals(userTasks.toString(), "User Task", userTasks.iterator().next().getName());
		incoming = userTasks.iterator().next().getChildElementsByType(Incoming.class);
		assertEquals(incoming.toString(), 1, incoming.size());
		assertEquals(incoming.toString(), "flow1", incoming.iterator().next().getTextContent());
		outgoing = userTasks.iterator().next().getChildElementsByType(Outgoing.class);
		assertEquals(outgoing.toString(), 1, outgoing.size());
		assertEquals(outgoing.toString(), "flow2", outgoing.iterator().next().getTextContent());

		// 2 x sequenceFlow
		Collection<SequenceFlow> flows = process.getChildElementsByType(SequenceFlow.class);
		assertEquals(flows.toString(), 2, flows.size());
		// find startEvent->sequenceFlow->userTask
		boolean foundFlowStartTask = false;
		// find userTask->sequenceFlow->endEvent
		boolean foundFlowTaskEnd = false;
		for (SequenceFlow sequenceFlow : flows) {
			if (sequenceFlow.getSource().getId().equals("start") && sequenceFlow.getTarget().getId().equals("task")) {
				assertEquals(sequenceFlow.toString(), "flow1", sequenceFlow.getId());
				foundFlowStartTask = true;
			}
			if (sequenceFlow.getSource().getId().equals("task") && sequenceFlow.getTarget().getId().equals("end")) {
				assertEquals(sequenceFlow.toString(), "flow2", sequenceFlow.getId());
				foundFlowTaskEnd = true;
			}
		}
		assertTrue(flows.toString(), foundFlowStartTask);
		assertTrue(flows.toString(), foundFlowTaskEnd);

	}

	/**
	 * Test method of {@link DecoderImpl#saveBPMN(java.io.OutputStream)} with the
	 * data object BPMN model.
	 */
	@Test
	public final void testSaveBPMNDataObject() throws Exception {
		if (!isRunDataObjectBPMN()) {
			logger.warn("Skipping testSaveBPMNDataObject...");
			return;
		}

		// the object to test
		DecoderImpl decoder = (DecoderImpl) DecoderImpl.getInstance();

		// the address of TypeDB
		decoder.setTypeDBAddress(address);

		// name of the test database
		decoder.setDatabaseName(databaseName);

		// the UID of the BPMN node to query
		decoder.setRootUID(
				// use the UID of Mission in concept model instead
				"http://c4i.gmu.edu/dalnim/examples/#Mission_Definitions_1");
		// make sure we can query from Mission UID
		decoder.setMapBPMNToConceptualModel(true);

		ByteArrayOutputStream stream = new ByteArrayOutputStream();
		decoder.saveBPMN(stream);
		stream.flush();
		stream.close();
		String result = stream.toString();

		logger.debug("Result: \n{}", result);

		assertFalse(result, result.trim().isEmpty());

		// parse result as BPMN
		BpmnModelInstance bpmn = Bpmn.readModelFromStream(new ByteArrayInputStream(result.getBytes()));
		assertNotNull(bpmn);

		// load the bpmn definitions (the root node)
		Definitions definitions = bpmn.getDefinitions();
		assertNotNull(definitions);

		// check namespaces
		assertEquals("http://www.omg.org/spec/BPMN/20100524/MODEL",
				bpmn.getDocument().getRootElement().getNamespaceURI());
		assertEquals("http://c4i.gmu.edu/dalnim/examples", definitions.getAttributeValue("targetNamespace"));

		// check process
		Collection<Process> processes = definitions.getChildElementsByType(Process.class);
		assertEquals(processes.toString(), 1, processes.size());
		Process process = processes.iterator().next();

		// content of process must be:
		// laneSet; dataObject;
		// startEvent->sequenceFlow->serviceTask->sequenceFlow->endEvent

		Collection<BaseElement> processContent = process.getChildElementsByType(BaseElement.class);
		assertEquals(processContent.toString(), 7, processContent.size());

		// startEvent
		Collection<StartEvent> startEvents = process.getChildElementsByType(StartEvent.class);
		assertEquals(startEvents.toString(), 1, startEvents.size());
		assertEquals(startEvents.toString(), "start", startEvents.iterator().next().getId());
		Collection<Outgoing> outgoing = startEvents.iterator().next().getChildElementsByType(Outgoing.class);
		assertEquals(outgoing.toString(), 1, outgoing.size());
		assertEquals(outgoing.toString(), "flow1", outgoing.iterator().next().getTextContent());

		// endEvent
		Collection<EndEvent> endEvents = process.getChildElementsByType(EndEvent.class);
		assertEquals(endEvents.toString(), 1, endEvents.size());
		assertEquals(endEvents.toString(), "end", endEvents.iterator().next().getId());
		Collection<Incoming> incoming = endEvents.iterator().next().getChildElementsByType(Incoming.class);
		assertEquals(incoming.toString(), 1, incoming.size());
		assertEquals(incoming.toString(), "flow2", incoming.iterator().next().getTextContent());

		// ServiceTask
		Collection<ServiceTask> tasks = process.getChildElementsByType(ServiceTask.class);
		assertEquals(tasks.toString(), 1, tasks.size());
		assertEquals(tasks.toString(), "ServiceTask_1", tasks.iterator().next().getId());
		assertEquals(tasks.toString(), "ServiceTask", tasks.iterator().next().getName());
		incoming = tasks.iterator().next().getChildElementsByType(Incoming.class);
		assertEquals(incoming.toString(), 1, incoming.size());
		assertEquals(incoming.toString(), "flow1", incoming.iterator().next().getTextContent());
		outgoing = tasks.iterator().next().getChildElementsByType(Outgoing.class);
		assertEquals(outgoing.toString(), 1, outgoing.size());
		assertEquals(outgoing.toString(), "flow2", outgoing.iterator().next().getTextContent());
		Collection<IoSpecification> ioSpecification = tasks.iterator().next()
				.getChildElementsByType(IoSpecification.class);
		assertEquals(ioSpecification.toString(), 1, ioSpecification.size());
		Collection<Performer> performer = tasks.iterator().next().getChildElementsByType(Performer.class);
		assertEquals(performer.toString(), 1, performer.size());
		Collection<DataInputAssociation> dataInputAssociation = tasks.iterator().next()
				.getChildElementsByType(DataInputAssociation.class);
		assertEquals(dataInputAssociation.toString(), 1, dataInputAssociation.size());
		assertEquals(dataInputAssociation.toString(), "DataObject_2", dataInputAssociation.iterator().next()
				.getChildElementsByType(SourceRef.class).iterator().next().getTextContent());

		// 2 x sequenceFlow
		Collection<SequenceFlow> flows = process.getChildElementsByType(SequenceFlow.class);
		assertEquals(flows.toString(), 2, flows.size());
		// find startEvent->sequenceFlow->userTask
		boolean foundFlowStartTask = false;
		// find userTask->sequenceFlow->endEvent
		boolean foundFlowTaskEnd = false;
		for (SequenceFlow sequenceFlow : flows) {
			if (sequenceFlow.getSource().getId().equals("start")
					&& sequenceFlow.getTarget().getId().equals("ServiceTask_1")) {
				assertEquals(sequenceFlow.toString(), "flow1", sequenceFlow.getId());
				foundFlowStartTask = true;
			}
			if (sequenceFlow.getSource().getId().equals("ServiceTask_1")
					&& sequenceFlow.getTarget().getId().equals("end")) {
				assertEquals(sequenceFlow.toString(), "flow2", sequenceFlow.getId());
				foundFlowTaskEnd = true;
			}
		}
		assertTrue(flows.toString(), foundFlowStartTask);
		assertTrue(flows.toString(), foundFlowTaskEnd);

		// lane set
		Collection<LaneSet> laneSet = process.getChildElementsByType(LaneSet.class);
		assertEquals(laneSet.toString(), 1, laneSet.size());
		assertEquals(laneSet.iterator().next().getChildElementsByType(Lane.class).toString(), 1,
				laneSet.iterator().next().getChildElementsByType(Lane.class).size());
		assertEquals(laneSet.iterator().next().getChildElementsByType(Lane.class).toString(), "Someone",
				laneSet.iterator().next().getChildElementsByType(Lane.class).iterator().next().getName());

		// BPMN diagram
		assertEquals(definitions.getChildElementsByType(BpmnDiagram.class).toString(), 1,
				definitions.getChildElementsByType(BpmnDiagram.class).size());

	}

	/**
	 * Test method of {@link DecoderImpl#saveBPMN(java.io.OutputStream)} with the
	 * UAV test BPMN model.
	 */
	@Test
	public final void testSaveBPMNUAV() throws Exception {
		if (!isRunGMUUAVBPMN()) {
			logger.warn("Skipping testSaveBPMNUAV...");
			return;
		}

		// the object to test
		DecoderImpl decoder = (DecoderImpl) DecoderImpl.getInstance();

		// the address of TypeDB
		decoder.setTypeDBAddress(address);

		// name of the test database
		decoder.setDatabaseName(databaseName);

		// the UID of the BPMN node to query
		decoder.setRootUID(
				// use the UID of Mission in concept model instead
				"http://bpmn.io/schema/bpmn/#Mission_Definitions_0buvjxg");
		// make sure we can query from Mission UID
		decoder.setMapBPMNToConceptualModel(true);

		ByteArrayOutputStream stream = new ByteArrayOutputStream();
		decoder.saveBPMN(stream);
		stream.flush();
		stream.close();
		String result = stream.toString();

		logger.debug("Result: \n{}", result);

		assertFalse(result, result.trim().isEmpty());

		// parse result as BPMN
		BpmnModelInstance bpmn = Bpmn.readModelFromStream(new ByteArrayInputStream(result.getBytes()));
		assertNotNull(bpmn);

		// load the bpmn definitions (the root node)
		Definitions definitions = bpmn.getDefinitions();
		assertNotNull(definitions);

		// check namespaces
		assertEquals("http://www.omg.org/spec/BPMN/20100524/MODEL",
				bpmn.getDocument().getRootElement().getNamespaceURI());
		assertEquals("http://bpmn.io/schema/bpmn", definitions.getAttributeValue("targetNamespace"));

		// check collaboration
		Collection<Collaboration> collaborations = definitions.getChildElementsByType(Collaboration.class);
		assertEquals(collaborations.toString(), 1, collaborations.size());
		Collaboration collaboration = collaborations.iterator().next();
		// must have 4 participants: UAV provider, Sender hospital, Receiver hospital,
		// and UTM.
		assertEquals(collaboration.getChildElementsByType(Participant.class).toString(), 4,
				collaboration.getChildElementsByType(Participant.class).size());

		// check process
		Collection<Process> processes = definitions.getChildElementsByType(Process.class);
		// there are 4 processes: 1 main + 3 collaborations.
		assertEquals(processes.toString(), 4, processes.size());

		// get the main process
		Process process = processes.stream().filter(p -> p.getId().equals("Process_176ykgu")).findAny().get();
		assertNotNull(process);

		// 3 receive tasks,
		assertEquals(3, process.getChildElementsByType(ReceiveTask.class).size());

		// 3 manual tasks,
		assertEquals(3, process.getChildElementsByType(ManualTask.class).size());

		// 6 service tasks,
		assertEquals(6, process.getChildElementsByType(ServiceTask.class).size());

		// 1 send task,
		assertEquals(1, process.getChildElementsByType(SendTask.class).size());

		// 4 parallel gateways,
		assertEquals(4, process.getChildElementsByType(ParallelGateway.class).size());

		// 1 start and 1 end events
		assertEquals(1, process.getChildElementsByType(StartEvent.class).size());
		assertEquals(1, process.getChildElementsByType(EndEvent.class).size());

		// BPMN diagram
		assertEquals(definitions.getChildElementsByType(BpmnDiagram.class).toString(), 1,
				definitions.getChildElementsByType(BpmnDiagram.class).size());

	}

	/**
	 * Test method of {@link DecoderImpl#saveBPMN(java.io.OutputStream)} with the
	 * VATech uavanet model.
	 */
	@Test
	public final void testSaveBPMNuavanet() throws Exception {
		if (!isRunUavanetBPMN()) {
			logger.warn("Skipping testSaveBPMNuavanet...");
			return;
		}

		// the object to test
		DecoderImpl decoder = (DecoderImpl) DecoderImpl.getInstance();

		// the address of TypeDB
		decoder.setTypeDBAddress(address);

		// name of the test database
		decoder.setDatabaseName(databaseName);

		// the UID of the BPMN node to query
		decoder.setRootUID("http://vt.edu/dalnim/uavanet.*");

		ByteArrayOutputStream stream = new ByteArrayOutputStream();
		decoder.saveBPMN(stream);
		stream.flush();
		stream.close();
		String result = stream.toString();

		logger.debug("Result: \n{}", result);

		assertFalse(result, result.trim().isEmpty());

		// parse result as BPMN
		BpmnModelInstance bpmn = Bpmn.readModelFromStream(new ByteArrayInputStream(result.getBytes()));
		assertNotNull(bpmn);

		// load the bpmn definitions (the root node)
		Definitions definitions = bpmn.getDefinitions();
		assertNotNull(definitions);

		// check namespaces
		assertEquals("http://www.omg.org/spec/BPMN/20100524/MODEL",
				bpmn.getDocument().getRootElement().getNamespaceURI());
		assertEquals("http://vt.edu/dalnim/uavanet", definitions.getAttributeValue("targetNamespace"));

		// check collaboration
		Collection<Collaboration> collaborations = definitions.getChildElementsByType(Collaboration.class);
		assertEquals(collaborations.toString(), 1, collaborations.size());
		Collaboration collaboration = collaborations.iterator().next();
		// must have 1 participant: Mission (Image Classification) Process
		assertEquals(collaboration.getChildElementsByType(Participant.class).toString(), 1,
				collaboration.getChildElementsByType(Participant.class).size());

		// check process
		Collection<Process> processes = definitions.getChildElementsByType(Process.class);
		// there is only 1 process
		assertEquals(processes.toString(), 1, processes.size());

		// get the main process
		Process process = processes.stream().filter(p -> p.getId().equals("Process_0vkxjoy")).findAny().get();
		assertNotNull(process);

		// 5 service tasks,
		assertEquals(5, process.getChildElementsByType(ServiceTask.class).size());

		// 5 send tasks,
		assertEquals(5, process.getChildElementsByType(SendTask.class).size());

		// 4 exclusive gateways,
		assertEquals(4, process.getChildElementsByType(ExclusiveGateway.class).size());

		// 1 start and 1 end events
		assertEquals(1, process.getChildElementsByType(StartEvent.class).size());
		assertEquals(1, process.getChildElementsByType(EndEvent.class).size());

		// 2 data objects
		assertEquals(2, process.getChildElementsByType(DataObject.class).size());

		// 18 sequence flows
		assertEquals(18, process.getChildElementsByType(SequenceFlow.class).size());

		// the visual elements: BPMN diagram
		assertEquals(definitions.getChildElementsByType(BpmnDiagram.class).toString(), 1,
				definitions.getChildElementsByType(BpmnDiagram.class).size());

	}

	/**
	 * @return the isRunSimpleBPMN
	 */
	public static boolean isRunSimpleBPMN() {
		return isRunSimpleBPMN;
	}

	/**
	 * @param isRunSimpleBPMN the isRunSimpleBPMN to set
	 */
	public static void setRunSimpleBPMN(boolean isRunSimpleBPMN) {
		DecoderImplTest.isRunSimpleBPMN = isRunSimpleBPMN;
	}

	/**
	 * @return the isRunDataObjectBPMN
	 */
	public static boolean isRunDataObjectBPMN() {
		return isRunDataObjectBPMN;
	}

	/**
	 * @param isRunDataObjectBPMN the isRunDataObjectBPMN to set
	 */
	public static void setRunDataObjectBPMN(boolean isRunDataObjectBPMN) {
		DecoderImplTest.isRunDataObjectBPMN = isRunDataObjectBPMN;
	}

	/**
	 * @return the isRunGMUUAVBPMN
	 */
	public static boolean isRunGMUUAVBPMN() {
		return isRunGMUUAVBPMN;
	}

	/**
	 * @param isRunGMUUAVBPMN the isRunGMUUAVBPMN to set
	 */
	public static void setRunGMUUAVBPMN(boolean isRunGMUUAVBPMN) {
		DecoderImplTest.isRunGMUUAVBPMN = isRunGMUUAVBPMN;
	}

	/**
	 * @return the isRunUavanetBPMN
	 */
	public static boolean isRunUavanetBPMN() {
		return isRunUavanetBPMN;
	}

	/**
	 * @param isRunUavanetBPMN the isRunUavanetBPMN to set
	 */
	public static void setRunUavanetBPMN(boolean isRunUavanetBPMN) {
		DecoderImplTest.isRunUavanetBPMN = isRunUavanetBPMN;
	}

}
