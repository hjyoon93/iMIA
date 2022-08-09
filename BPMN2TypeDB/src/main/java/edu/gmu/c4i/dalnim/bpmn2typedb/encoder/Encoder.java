package edu.gmu.c4i.dalnim.bpmn2typedb.encoder;

import java.io.InputStream;
import java.io.OutputStream;

/**
 * Converts BPMN2 to TypeQL scripts.
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
	void loadInput(InputStream input);

	/**
	 * Writes the translated TypeQL schema script to the output stream.
	 * 
	 * @param schemaOutput : stream to write.
	 */
	void encodeSchema(OutputStream schemaOutput);

	/**
	 * Writes the translated TypeQL data script to the output stream.
	 * 
	 * @param schemaOutput : stream to write.
	 */
	void encodeData(OutputStream schemaOutput);

	/**
	 * @return default implementation of {@link Encoder}.
	 * @see EncoderImpl
	 */
	static Encoder getDefaultEncoder() {
		return EncoderImpl.getEncoder();
	}

}
