package edu.gmu.c4i.dalnim.typedb2sbn;

import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;

import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.stream.Collectors;
import java.util.stream.Stream;

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

import unbbayes.io.CountCompatibleNetIO;
import unbbayes.prs.Node;
import unbbayes.prs.bn.JunctionTreeAlgorithm;
import unbbayes.prs.bn.ProbabilisticNetwork;

/**
 * Unit test for {@link DecoderImpl}. A TypeDB database must be available at
 * localhost 1729 to work.
 * 
 * @author shou
 */
//@Ignore("A TypeDB instance must be running in localhos:1729. Remove this annotation if TypeDB is running fine.")
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

		// load the conceptual model schema
		try (TypeDBSession session = client.session(databaseName, TypeDBSession.Type.SCHEMA)) {
			try (TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.WRITE)) {
				Stream<TypeQLQuery> queries = TypeQL.parseQueries(Files.readString(
						// Load the concept model script from src/*/resources:
						// Path.of(DecoderImplTest.class.getResource("/concept_model.tql").toURI())
						// ... or load the concept model script from parent folder:
						new File("../concept_model.tql").toPath()));
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
		try (TypeDBSession session = client.session(databaseName, TypeDBSession.Type.SCHEMA)) {
			try (TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.WRITE)) {
				Stream<TypeQLQuery> queries = TypeQL.parseQueries(
						Files.readString(Path.of(DecoderImplTest.class.getResource("/schema.tql").toURI())));
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
						Files.readString(Path.of(DecoderImplTest.class.getResource("/data.tql").toURI())));
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
	 * Test method of {@link DecoderImpl#saveSBNFile(File)}.
	 */
	@Test
	public final void testSaveBPMNSimple() throws Exception {
		// where to save the net file
		File tempFile = File.createTempFile(getClass().getName(), ".net");
		tempFile.delete();
		assertFalse(tempFile.exists());

		// the object to test
		DecoderImpl decoder = (DecoderImpl) DecoderImpl.getInstance();

		// the address of TypeDB
		decoder.setTypeDBAddress(address);

		// name of the test database
		decoder.setDatabaseName(databaseName);

		// the UID of the TypeDB entity to query
		decoder.setRootUID(".*");

		// run the method to test
		decoder.saveSBNFile(tempFile);
		assertTrue(tempFile.exists());

		// load the network and check the structure
		ProbabilisticNetwork net = (ProbabilisticNetwork) new CountCompatibleNetIO().load(tempFile);

		// make sure multiple nodes were created
		assertTrue(net.getNodeCount() > 1);

		// make sure multiple edges were created
		assertTrue(net.getEdges().size() > 0);

		// make sure the mission node was created
		Node missionNode = net.getNode("Mission");
		assertFalse(missionNode.getParentNodes().isEmpty());

		// make sure the network can be compiled
		new JunctionTreeAlgorithm(net).run();

		// make sure the temp file is deleted
		Files.delete(tempFile.toPath());
	}

}
