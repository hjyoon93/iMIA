package edu.gmu.c4i.dalnim.typedb2sbn;

import java.io.File;
import java.io.IOException;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Default implementation of {@link Decoder} that reads a BPMN project from
 * TypeDB database and saves the content to a BPMN2 file format.
 * 
 * @author shou
 */
public class DecoderImpl implements Decoder {

	private static Logger logger = LoggerFactory.getLogger(DecoderImpl.class);

	private String typeDBAddress = "localhost:1729";

	private String databaseName = "BPMN";

	private String rootUID = "https://camunda.org/examples/#.*";

	private String uidAttributeName = "UID";

	/**
	 * Default constructor is protected from public access. Use
	 * {@link #getInstance()} instead.
	 */
	protected DecoderImpl() {
		// Auto-generated constructor stub
	}

	/**
	 * Default constructor method.
	 * 
	 * @return a new instance of {@link DecoderImpl}
	 */
	public static Decoder getInstance() {

		// add any initialization code here
		return new DecoderImpl();
	}

	@Override
	public void saveSBNFile(File outputFile) throws IOException {

		logger.info("Start generating NET file: {}", outputFile);

		// TODO stub
		throw new UnsupportedOperationException("Not implemented yet");
	}

	/**
	 * @return address of TypeDB (e.g., "localhost:1729").
	 */
	public String getTypeDBAddress() {
		return typeDBAddress;
	}

	/**
	 * @param address : address of TypeDB (e.g., "localhost:1729").
	 */
	@Override
	public void setTypeDBAddress(String address) {
		this.typeDBAddress = address;
	}

	/**
	 * @return name of the database in TypeDB to access.
	 */
	public String getDatabaseName() {
		return databaseName;
	}

	/**
	 * @param databaseName : name of the database in TypeDB to access.
	 */
	@Override
	public void setDatabaseName(String databaseName) {
		this.databaseName = databaseName;
	}

	/**
	 * @return the uid attribute to query in the TypeDB database to retrieve the
	 *         root of the BPMN model. Regular expression is supported.
	 */
	public String getRootUID() {
		return rootUID;
	}

	/**
	 * @param uid : the uid attribute to query in the TypeDB database to retrieve
	 *            the root of the BPMN model. Regular expression is supported.
	 */
	@Override
	public void setRootUID(String uid) {
		this.rootUID = uid;
	}

	/**
	 * @return name of the universal identifier attribute.
	 */
	public String getUIDAttributeName() {
		return uidAttributeName;
	}

	/**
	 * @param name : name of the universal identifier attribute.
	 */
	public void setUIDAttributeName(String name) {
		this.uidAttributeName = name;
	}

}
