package edu.gmu.c4i.dalnim.bpmn2typedb.encoder;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;

/**
 * Converts a script to another format. This is originally designed to read a
 * BPMN file and save a TypeQL script.
 * 
 * @author shou
 * 
 * @see EncoderImpl
 */
public interface Encoder {

	/**
	 * Loads the input BPMN2 to translate.
	 * 
	 * @param input : stream pointing to the BPMN2 XML file/stream.
	 */
	void loadInput(InputStream input) throws IOException;

	/**
	 * Writes the translated TypeQL schema script to the output stream.
	 * 
	 * @param schemaOutput : stream to write.
	 */
	void encodeSchema(OutputStream schemaOutput) throws IOException;

	/**
	 * Writes the translated TypeQL data script to the output stream.
	 * 
	 * @param schemaOutput : stream to write.
	 */
	void encodeData(OutputStream schemaOutput) throws IOException;

	/**
	 * @return default implementation of {@link Encoder}.
	 * @see EncoderImpl
	 */
	static Encoder getDefaultEncoder() {
		return EncoderImpl.getInstance();
	}

}
