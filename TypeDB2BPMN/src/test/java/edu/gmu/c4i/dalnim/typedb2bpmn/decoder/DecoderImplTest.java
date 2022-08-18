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
import org.camunda.bpm.model.bpmn.instance.BaseElement;
import org.camunda.bpm.model.bpmn.instance.Definitions;
import org.camunda.bpm.model.bpmn.instance.EndEvent;
import org.camunda.bpm.model.bpmn.instance.Process;
import org.camunda.bpm.model.bpmn.instance.SequenceFlow;
import org.camunda.bpm.model.bpmn.instance.StartEvent;
import org.camunda.bpm.model.bpmn.instance.UserTask;
import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Ignore;
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
public class DecoderImplTest {

	private static Logger logger = LoggerFactory.getLogger(DecoderImplTest.class);

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

		// set up schema from file
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
		// set up the data from file
		try (TypeDBSession session = client.session(databaseName, TypeDBSession.Type.DATA)) {
			try (TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.WRITE)) {
				Stream<TypeQLQuery> queries = TypeQL.parseQueries(
						Files.readString(Path.of(DecoderImplTest.class.getResource("/simple_BPMN_data.tql").toURI())));
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
	@Ignore("Not finished yet")
	public final void testSaveBPMN() throws Exception {

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

}
