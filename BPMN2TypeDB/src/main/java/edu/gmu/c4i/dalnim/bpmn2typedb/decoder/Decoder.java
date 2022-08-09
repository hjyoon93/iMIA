package edu.gmu.c4i.dalnim.bpmn2typedb.decoder;

import java.io.OutputStream;
import java.net.URI;

/**
 * Reads a TypeDB database and extracts a BPMN2 process model.
 * 
 * @author shou
 */
public interface Decoder {

	/**
	 * @param location : location of the TypeDB database.
	 */
	void setDBLocation(URI location);
	
	/**
	 * Reads data from the location specified in {@link #setDBLocation(URI)}
	 * and writes a BPMN2 XML file to the specified location.
	 * 
	 * @param output : file/stream to write.
	 */
	void decodeProcessModel(OutputStream output);
}
