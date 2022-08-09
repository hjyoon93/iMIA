package edu.gmu.c4i.dalnim.bpmn2typedb.encoder;

import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.util.Collection;

import org.camunda.bpm.model.bpmn.Bpmn;
import org.camunda.bpm.model.bpmn.BpmnModelInstance;
import org.camunda.bpm.model.bpmn.instance.BaseElement;
import org.camunda.bpm.model.bpmn.instance.FlowElement;
import org.camunda.bpm.model.bpmn.instance.FlowNode;
import org.camunda.bpm.model.bpmn.instance.Process;
import org.camunda.bpm.model.bpmn.instance.SequenceFlow;
import org.camunda.bpm.model.xml.instance.DomElement;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Default implementation of {@link Encoder}
 * 
 * @author shou
 */
public class EncoderImpl implements Encoder {

	private static Logger logger = LoggerFactory.getLogger(EncoderImpl.class);

	private BpmnModelInstance bpmnModel;

	private String instanceNamespace;

	private String schemaNamespace;

	/**
	 * Possible values for the mode of
	 * {@link EncoderImpl#encode(OutputStream, EncodingMode)}
	 * 
	 * @author shou
	 */
	public enum EncodingMode {
		SCHEMA, DATA, UNKNOWN
	}

	/**
	 * Default constructor is protected to avoid public access. Use
	 * {@link #getEncoder()} instead.
	 */
	protected EncoderImpl() {
		// Auto-generated constructor stub
	}

	/**
	 * Default instantiation method of {@link EncoderImpl}.
	 * 
	 * @return a new instance.
	 */
	public static Encoder getEncoder() {
		return new EncoderImpl();
	}

	@Override
	public void loadInput(InputStream input) {

		logger.info("Loading input...");
		bpmnModel = Bpmn.readModelFromStream(input);
		logger.info("Finished loading input");

		logger.debug("Extracting namespaces");
		instanceNamespace = bpmnModel.getDefinitions().getTargetNamespace();
		logger.debug("Extracted instance/target namespace: {}", instanceNamespace);
		schemaNamespace = bpmnModel.getDocument().getRootElement().getNamespaceURI();
		logger.debug("Extracted schema/base namespace: {}", schemaNamespace);

	}

	@Override
	public void encodeSchema(OutputStream schemaOutput) {
		logger.info("Generating TypeQL schema definitions...");
		this.encode(schemaOutput, EncodingMode.SCHEMA);
		logger.info("Finished TypeQL schema definitions");
	}

	@Override
	public void encodeData(OutputStream schemaOutput) {
		logger.info("Generating TypeQL data insertion...");
		this.encode(schemaOutput, EncodingMode.DATA);
		logger.info("Finished TypeQL data insertion");
	}

	/**
	 * Iterates on the processes in {@link #getBPMNModel()} and fills the output
	 * stream either with TypeQL schema definitions ({@link EncodingMode#SCHEMA}) or
	 * TypeQL data insertions ({@link EncodingMode#DATA})
	 * 
	 * @param outputStream : stream to write
	 * @param mode         : {@link EncodingMode#SCHEMA} (TypeQL schema definition)
	 *                     or {@link EncodingMode#DATA} (TypeQL data insertion).
	 * 
	 * @see #encodeData(OutputStream)
	 * @see #encodeSchema(OutputStream)
	 */
	protected void encode(OutputStream outputStream, EncodingMode mode) {

		logger.debug("Encoding mode: {}", mode);
		if (mode == null) {
			mode = EncodingMode.UNKNOWN;
		}
		if (outputStream == null) {
			throw new NullPointerException("Invalid argument: the output stream was null");
		}

		logger.debug("Retrieving cached BPMN model...");
		BpmnModelInstance bpmn = getBPMNModel();
		logger.debug("Cached BPMN model: {}", bpmn);

		logger.debug("Retrieving the namespace to use...");
		String namespace = null;
		switch (mode) {
		case SCHEMA:
			namespace = getSchemaNamespace();
			break;
		case DATA:
			namespace = getInstanceNamespace();
			break;
		default:
		}
		// namespace must be set
		if (namespace == null || namespace.trim().isEmpty()) {
			logger.warn("No namespace was set. Using default namespace...");
			namespace = "http://c4i.gmu.edu/dalnim/#";
		}
		// append "#" to the end of the namespace, if not already present
		if (!namespace.endsWith("#")) {
			// Make sure namespace ends with "/#"
			if (!namespace.endsWith("/")) {
				namespace += "/";
			}
			namespace += "#";
		}
		logger.debug("Namespace: {}", namespace);

		logger.debug("Retrieving processes declared in the BPMN model...");
		Collection<Process> processes = bpmn.getModelElementsByType(Process.class);
		logger.debug("Retrieved processes: {}", processes);

		// prepare writer for output stream
		try (PrintWriter writer = new PrintWriter(outputStream)) {
			logger.debug("Writing the headers...");
			switch (mode) {
			case SCHEMA:
				writeSchemaHeader(writer, bpmn);
				break;
			default:
			}

			// iterate on each process
			for (Process process : processes) {
				
				logger.debug("Encoding process {}", process);
				
				
				
				// Basically, all elements in the flow (except camunda-specific elements)
				// process.getChildElementsByType(BaseElement.class)
				
				// elements in the flow, with names and ids
				// process.getChildElementsByType(FlowElement.class)
				
				// Arcs in the diagram
				// process.getChildElementsByType(SequenceFlow.class).iterator().next()
				
				// Nodes in the diagram
				// process.getChildElementsByType(FlowNode.class).iterator().next()

			} // end of for each process
		} // this will close writer
	}

	private void writeSchemaHeader(PrintWriter writer, BpmnModelInstance bpmn) {
		// TODO Auto-generated method stub
		writer.println("define");
		
		writer.println("definitions");
	}

	/**
	 * @return the {@link BpmnModelInstance} loaded in
	 *         {@link #loadInput(InputStream)}
	 */
	protected BpmnModelInstance getBPMNModel() {
		return bpmnModel;
	}

	/**
	 * @param bpmnModel : the {@link BpmnModelInstance} loaded in
	 *                  {@link #loadInput(InputStream)}
	 */
	protected void setBPMNModel(BpmnModelInstance bpmnModel) {
		this.bpmnModel = bpmnModel;
	}

	/**
	 * @return the instanceNamespace
	 */
	public String getInstanceNamespace() {
		return instanceNamespace;
	}

	/**
	 * @param instanceNamespace the instanceNamespace to set
	 */
	public void setInstanceNamespace(String instanceNamespace) {
		this.instanceNamespace = instanceNamespace;
	}

	/**
	 * @return the schemaNamespace
	 */
	public String getSchemaNamespace() {
		return schemaNamespace;
	}

	/**
	 * @param schemaNamespace the schemaNamespace to set
	 */
	public void setSchemaNamespace(String schemaNamespace) {
		this.schemaNamespace = schemaNamespace;
	}

}
