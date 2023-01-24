package edu.gmu.c4i.dalnim.typedb2sbn.decoder;

import java.io.IOException;
import java.io.OutputStream;

/**
 * 
 * Common interface for classes that reads TypeDB and saves SBN.
 * 
 * @author shou
 * 
 * @see DecoderImpl
 */
public interface Decoder {

	/**
	 * Access a TypeDB database, queries the mission model, and saves the translated
	 * SBN structure model to a stream.
	 * 
	 * @param outputStream : stream to save
	 * 
	 * @throws IOException
	 */
	public void save(OutputStream outputStream) throws IOException;

	/**
	 * @param address : address of TypeDB (e.g., "localhost:1729").
	 */
	public void setTypeDBAddress(String address);

	/**
	 * @param name : name of the database in TypeDB to access.
	 */
	public void setDatabaseName(String name);

	/**
	 * @param uid : the uid attribute to query in the TypeDB database to retrieve
	 *            the root of the mission model. Regular expression is supported.
	 */
	public void setRootUID(String uid);

}
