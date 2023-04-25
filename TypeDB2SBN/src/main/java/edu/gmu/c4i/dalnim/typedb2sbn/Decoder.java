package edu.gmu.c4i.dalnim.typedb2sbn;

import java.io.File;
import java.io.IOException;

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
	 * Access a TypeDB database, queries the SBN objects, and saves them to a SBN
	 * stream.
	 * 
	 * @param sbnOutput : stream to save
	 * 
	 * @throws IOException
	 */
	void saveSBNFile(File sbnOutput) throws IOException;

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
	 *            the root of the concept model. Regular expression is supported.
	 */
	void setRootUID(String uid);

}
