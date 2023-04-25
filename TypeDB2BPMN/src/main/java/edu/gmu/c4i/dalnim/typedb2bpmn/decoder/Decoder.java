package edu.gmu.c4i.dalnim.typedb2bpmn.decoder;

import java.io.IOException;
import java.io.OutputStream;

/**
 * 
 * Common interface for classes that reads TypeDB and saves BPMN.
 * 
 * @author shou
 * 
 * @see DecoderImpl
 */
public interface Decoder {

	/**
	 * Access a TypeDB database, queries the BPMN objects, and saves them to a BPMN
	 * stream.
	 * 
	 * @param bpmnOutput : stream to save
	 * 
	 * @throws IOException
	 */
	void saveBPMN(OutputStream bpmnOutput) throws IOException;

	/**
	 * @return default implementation of {@link Decoder}
	 * @see DecoderImpl
	 */
	static Decoder getDefaultDecoder() {
		return DecoderImpl.getInstance();
	}

	/**
	 * @param address : address of TypeDB (e.g., "localhost:1729").
	 */
	void setTypeDBAddress(String address);

	/**
	 * @param name : name of the database in TypeDB to access.
	 */
	void setDatabaseName(String name);

	/**
	 * @param uid : the uid attribute to query in the TypeDB database to retrieve
	 *            the root of the BPMN model. Regular expression is supported.
	 */
	void setRootUID(String uid);

}
