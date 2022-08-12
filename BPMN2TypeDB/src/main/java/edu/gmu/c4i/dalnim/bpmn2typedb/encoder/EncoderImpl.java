package edu.gmu.c4i.dalnim.bpmn2typedb.encoder;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Set;
import java.util.stream.Collectors;

import org.camunda.bpm.model.bpmn.Bpmn;
import org.camunda.bpm.model.bpmn.BpmnModelInstance;
import org.camunda.bpm.model.bpmn.impl.instance.FlowNodeRef;
import org.camunda.bpm.model.bpmn.impl.instance.Incoming;
import org.camunda.bpm.model.bpmn.impl.instance.Outgoing;
import org.camunda.bpm.model.bpmn.instance.BaseElement;
import org.camunda.bpm.model.bpmn.instance.BpmnModelElementInstance;
import org.camunda.bpm.model.bpmn.instance.bpmndi.BpmnDiagram;
import org.camunda.bpm.model.bpmn.instance.dc.Bounds;
import org.camunda.bpm.model.bpmn.instance.dc.Point;
import org.camunda.bpm.model.bpmn.instance.di.DiagramElement;
import org.camunda.bpm.model.xml.type.attribute.Attribute;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.vaticle.typeql.lang.TypeQL;
import com.vaticle.typeql.lang.common.exception.TypeQLException;
import com.vaticle.typeql.lang.pattern.constraint.TypeConstraint.Owns;
import com.vaticle.typeql.lang.pattern.constraint.TypeConstraint.Plays;
import com.vaticle.typeql.lang.pattern.constraint.TypeConstraint.Relates;
import com.vaticle.typeql.lang.pattern.variable.TypeVariable;
import com.vaticle.typeql.lang.query.TypeQLDefine;

import edu.gmu.c4i.dalnim.util.ApplicationProperties;

/**
 * Default implementation of {@link Encoder}
 * 
 * @author shou
 */
public class EncoderImpl implements Encoder {

	private static Logger logger = LoggerFactory.getLogger(EncoderImpl.class);

	private BpmnModelInstance bpmnModel;

	private String instanceNamespace = "http://c4i.gmu.edu/dalnim/#";

	private String schemaNamespace = "http://www.omg.org/spec/BPMN/20100524/MODEL";

	private boolean isRunSanityCheck = true;

	private boolean isAddImplementationSpecificSchemaAttributes = true;

	private String bpmnEntityNamePrefix = "BPMN_";

	private String bpmnEntityName = bpmnEntityNamePrefix + "Entity";

	private String textContentAttributeName = bpmnEntityNamePrefix + "textContent";

	private String bpmnConceptualModelMappingName = bpmnEntityNamePrefix + "hasConceptualModelElement";

	private String bpmnParentChildRelationName = bpmnEntityNamePrefix + "hasChildTag";

	private String commaSeparatedMappableConceptualModelEntities = "Mission,Task,Performer";

	/**
	 * Default constructor is protected to avoid public access. Use
	 * {@link #getInstance()} instead.
	 */
	protected EncoderImpl() {
		// Auto-generated constructor stub
	}

	/**
	 * Default instantiation method of {@link EncoderImpl}.
	 * 
	 * @return a new instance.
	 */
	public static Encoder getInstance() {

		EncoderImpl ret = new EncoderImpl();

		try {
			ApplicationProperties.getInstance().loadApplicationProperties(ret);
		} catch (Exception e) {
			logger.warn("Failed to load application.properties. Ignoring...", e);
		}

		return ret;
	}

	@Override
	public void loadInput(InputStream input) throws IOException {

		logger.info("Loading input...");
		bpmnModel = Bpmn.readModelFromStream(input);
		logger.info("Finished loading input");

		logger.debug("Extracting namespaces");
		setInstanceNamespace(bpmnModel.getDefinitions().getTargetNamespace());
		logger.debug("Extracted instance/target namespace: {}", instanceNamespace);
		setSchemaNamespace(bpmnModel.getDocument().getRootElement().getNamespaceURI());
		logger.debug("Extracted schema/base namespace: {}", schemaNamespace);

	}

	@Override
	public void encodeSchema(OutputStream outputStream) throws IOException {
		logger.info("Generating TypeQL schema definitions...");
		if (outputStream == null) {
			throw new NullPointerException("Invalid argument: the output stream was null");
		}

		logger.debug("Retrieving cached BPMN model...");
		BpmnModelInstance bpmn = getBPMNModel();
		logger.debug("Cached BPMN model: {}", bpmn);

		logger.debug("Retrieving the namespace to use...");
		String namespace = getSchemaNamespace();

		// namespace must be set
		if (namespace == null || namespace.trim().isEmpty()) {
			logger.warn("No namespace was set. Using default namespace for schema...");
			namespace = "http://www.omg.org/spec/BPMN/20100524/MODEL";
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

		// prepare writer for output stream
		try (PrintWriter writer = new PrintWriter(outputStream)) {

			logger.debug("Writing the header");

			// TypeQL schema must start with the keyword "define"
			writer.println("define");
			writer.println();

			writer.println("## =============== Header ===============");
			writer.println();

			writer.println(
					"## Note: attribute uid is required in DALNIM. Uncomment the following line if not declared yet.");
			writer.println("## uid sub attribute, value string;");
			writer.println();

			writer.println("## BPMN entities in general");
			writer.println(getBPMNEntityNamePrefix() + "id sub attribute, value string;");
			writer.println(getBPMNEntityNamePrefix() + "name sub attribute, value string;");
			writer.println(getTextContentAttributeName() + " sub attribute, value string;");
			writer.println(getBPMNEntityName() + " sub entity, owns " + getBPMNEntityNamePrefix() + "id, owns "
					+ getBPMNEntityNamePrefix() + "name, owns " + getTextContentAttributeName() + ", owns uid @key;");
			writer.println();

			writer.println("## Parent-child relationship of BPMN/XML tags");
			writer.println(getBPMNParentChildRelationName() + " sub relation, relates parent, relates child;");
			// A BPMN tag/entity can be a parent or child of another BPMN tag/entity
			writer.println(getBPMNEntityName() + " plays " + getBPMNParentChildRelationName() + ":child;");
			writer.println(getBPMNEntityName() + " plays " + getBPMNParentChildRelationName() + ":parent;");

			writer.println();

			// Some attributes are already declared in root "BPMN" entity,
			// so children do not have to re-declare
			Set<String> attributesInRootEntity = new HashSet<>();
			attributesInRootEntity.add("uid");
			attributesInRootEntity.add(getBPMNEntityNamePrefix() + "id");
			attributesInRootEntity.add(getBPMNEntityNamePrefix() + "name");
			attributesInRootEntity.add(getTextContentAttributeName());

			logger.debug("Writing the body...");
			writer.println("## =============== Body ===============");
			writer.println();

			// store what was already declared
			Set<String> declaredAttributes = new HashSet<>(attributesInRootEntity);

			Set<String> declaredRelations = new HashSet<>();
			declaredRelations.add(getBPMNParentChildRelationName());

			Set<String> visitedNodes = new HashSet<>();

			// recursively visit what's below "definitions" tag
			visitEntityRecursive(writer, bpmn.getDefinitions(), visitedNodes, attributesInRootEntity,
					declaredAttributes, declaredRelations);

			// declare some attributes specific to our implementation
			addImplementationSpecificSchemaEntries(writer, bpmn, visitedNodes, attributesInRootEntity,
					declaredAttributes, declaredRelations);

			// sanity check
			if (isRunSanityCheck()) {
				runSanityCheck(bpmn, visitedNodes, attributesInRootEntity, declaredAttributes, declaredRelations);
			} // end of sanity check

			writer.println("## =============== End ===============");
			logger.info("Finished TypeQL schema definitions.");

		} // this will close writer

	}

	/**
	 * Run basic sanity check on the structures generated in
	 * {@link #encodeSchema(OutputStream)}
	 * 
	 * @param bpmn                : reference to the BPMN object.
	 * @param visitedNodes        : names of BPMN tags that were already visited
	 *                            (attributes of these tags will be skipped)
	 * @param inheritedAttributes : these attributes will not be re-declared (it's
	 *                            supposed to inherit from root "BPMN" entity).
	 * @param declaredAttributes  : attributes that were already declared
	 *                            previously.
	 * @param declaredRelations   : relations that were already declared previously.
	 */
	protected void runSanityCheck(BpmnModelInstance bpmn, Set<String> visitedNodes, Set<String> attributesInRootEntity,
			Set<String> declaredAttributes, Set<String> declaredRelations) throws IOException {

		logger.debug("Running basic sanity check...");

		// sanity check on nodes
		if (!visitedNodes.contains(getBPMNEntityNamePrefix() + "definitions")) {
			throw new IOException("Sanity check failed: BPMN definitions was not created.");
		}
		if (!visitedNodes.contains(getBPMNEntityNamePrefix() + "process")) {
			throw new IOException("Sanity check failed: BPMN process was not created.");
		}
		if (!visitedNodes.contains(getBPMNEntityNamePrefix() + "startEvent")) {
			throw new IOException("Sanity check failed: BPMN startEvent was not created.");
		}
		if (!visitedNodes.contains(getBPMNEntityNamePrefix() + "endEvent")) {
			throw new IOException("Sanity check failed: BPMN endEvent was not created.");
		}

		if (!declaredAttributes.contains(getBPMNEntityNamePrefix() + "isExecutable")) {
			throw new IOException("Sanity check failed: attribute 'isExecutable' was not created.");
		}

		// sanity check on attributes
		if (visitedNodes.contains(getBPMNEntityNamePrefix() + "serviceTask")) {
			if (!declaredAttributes.contains(getBPMNEntityNamePrefix() + "implementation")) {
				throw new IOException("Sanity check failed: attribute 'implementation' was not created.");
			}
			if (!declaredAttributes.contains(getBPMNEntityNamePrefix() + "operationRef")) {
				throw new IOException("Sanity check failed: attribute 'operationRef' was not created.");
			}
		}
		if (visitedNodes.contains(getBPMNEntityNamePrefix() + "participant")
				&& !declaredAttributes.contains(getBPMNEntityNamePrefix() + "processRef")) {
			throw new IOException("Sanity check failed: attribute 'processRef' was not created.");
		}
		if (visitedNodes.contains(getBPMNEntityNamePrefix() + "messageFlow")
				|| visitedNodes.contains(getBPMNEntityNamePrefix() + "sequenceFlow")) {
			if (!declaredAttributes.contains(getBPMNEntityNamePrefix() + "sourceRef")) {
				throw new IOException("Sanity check failed: attribute 'sourceRef' was not created.");
			}
			if (!declaredAttributes.contains(getBPMNEntityNamePrefix() + "targetRef")) {
				throw new IOException("Sanity check failed: attribute 'targetRef' was not created.");
			}
		}

		// sanity check on relations
//		if (!declaredRelations.contains(getBPMNEntityNamePrefix() + "definitions_process")) {
//			throw new IOException(
//					"Sanity check failed: relation between BPMN definitions and BPMN process' was not created.");
//		}
//		if (visitedNodes.contains(getBPMNEntityNamePrefix() + "BPMNDiagram")
//				&& !declaredRelations.contains(getBPMNEntityNamePrefix() + "definitions_BPMNDiagram")) {
//			throw new IOException(
//					"Sanity check failed: relation between BPMN definitions and BPMN diagram' was not created.");
//		}
//		if (visitedNodes.contains(getBPMNEntityNamePrefix() + "collaboration")
//				&& !declaredRelations.contains(getBPMNEntityNamePrefix() + "definitions_collaboration")) {
//			throw new IOException(
//					"Sanity check failed: relation between BPMN definitions and BPMN collaboration' was not created.");
//		}

		// mapping from BPMN element to conceptual model should be declared
		if (!declaredRelations.contains(getBPMNConceptualModelMappingName())) {
			throw new IOException(
					"Sanity check failed: relation/mapping between BPMN entities and conceptual model was not created.");
		}
	}

	/**
	 * Recursively visits a BPMN node (and its children) to write the
	 * entity/attribute/relationship definitions. <br/>
	 * <br/>
	 * This should also create a mapping to elements in the DALNIM conceptual model.
	 * For instance:
	 * <ul>
	 * <li>BPMN task -> Task</li>
	 * <li>BPMN end event -> Mission</li>
	 * <li>collaboration.participant -> Performer</li>
	 * <li>lane -> Performer</li>
	 * <li>collaboration.messageFlow -> Resource (or Asset)</li>
	 * </ul>
	 * Also note that
	 * <ul>
	 * <li>Mission -> isCompoundBy -> Task</li>
	 * <li>Task -> isPerformedBy -> Performer</li>
	 * <li>Task -> requires -> Resource (or Asset)</li>
	 * </ul>
	 * 
	 * @param writer              : where to write the script block.
	 * @param currentNode         : current BPMN tag to handle
	 * @param visitedNodes        : names of BPMN tags that were already visited
	 *                            (attributes of these tags will be skipped)
	 * @param inheritedAttributes : these attributes will not be re-declared (it's
	 *                            supposed to inherit from root "BPMN" entity).
	 * @param declaredAttributes  : attributes that were already declared
	 *                            previously.
	 * @param declaredRelations   : relations that were already declared previously.
	 */
	protected void visitEntityRecursive(PrintWriter writer, BpmnModelElementInstance currentNode,
			Set<String> visitedNodes, Set<String> inheritedAttributes, Set<String> declaredAttributes,
			Set<String> declaredRelations) {

		logger.debug("Visiting BPMN tag/node {}", currentNode);

		if (currentNode == null) {
			logger.debug("BPMN node was null. Ignoring...");
			return;
		}
		if (writer == null) {
			logger.warn("Writer node was null. Returning...");
			return;
		}
		if (visitedNodes == null) {
			visitedNodes = new HashSet<>();
		}

		// Extract the entity name
		String currentEntityName = getBPMNEntityNamePrefix() + currentNode.getDomElement().getLocalName();
		logger.debug("Entity: {}", currentEntityName);

		// skip declaration if this node was already visited
		if (!visitedNodes.contains(currentEntityName)) {

			// declare the current entity
			writer.println("## BPMN '" + currentEntityName + "' tag/node");
			writer.println(currentEntityName + " sub " + getBPMNEntityName() + ";");
			writer.println();

			// declare all attributes
			for (Attribute<?> attrib : currentNode.getElementType().getAttributes()) {

				String attributeName = getBPMNEntityNamePrefix() + attrib.getAttributeName();

				// Skip attribute if it's already defined in root entity.
				if (inheritedAttributes.contains(attributeName)) {
					logger.debug("Skipped attribute {} in {}. It should be inherited from BPMN root entity.",
							attributeName, currentEntityName);
					continue;
				}

				// declare the attribute
				if (!declaredAttributes.contains(attributeName)) {
					writer.println(attributeName + " sub attribute, value string;");
					// mark attribute as declared
					declaredAttributes.add(attributeName);
				}

				// associate entity and attribute
				writer.println(currentEntityName + " owns " + attributeName + ";");
			}
			writer.println();

		} // else we visited this node already

//		// declare relationships from parent node to child
//		ModelElementInstance parentNode = currentNode.getParentElement();
//		if (parentNode != null) {
//			/**
//			 * <pre>
//			 * BPMN_definitions_collaboration sub relation,
//			 * 		relates BPMN_parent,
//			 * 		relates BPMN_child;
//			 * definitions plays BPMN_definitions_collaboration:definitions;
//			 * collaboration plays BPMN_definitions_collaboration:collaboration;
//			 * </pre>
//			 * 
//			 * Or an easier way would be to declare a parent-child relationship
//			 * for the top BPMN entity.
//			 * If it's the latter, then no need to declare relationships here
//			 */
//
//			// extract parent name
//			String parentEntityName = getBPMNEntityNamePrefix() + parentNode.getDomElement().getLocalName();
//
//			// Declare the relation.
//			// Avoid double-inserting "BPMN_" prefix
//			String relationName = getBPMNParentChildRelationName();
////			String relationName = getBPMNEntityNamePrefix() + parentNode.getDomElement().getLocalName() + "_"
////					+ currentNode.getDomElement().getLocalName();
//			if (!declaredRelations.contains(relationName)) {
//				writer.println(relationName + " sub relation, relates parent, relates child;");
//
//				// mark relation as declared
//				declaredRelations.add(relationName);
//				
//				// associate roles
//				writer.println(parentEntityName + " plays " + relationName + ":parent;");
//				writer.println(currentEntityName + " plays " + relationName + ":child;");
//				writer.println();
//			}
//
//		} // end of association between parent & child BPMN tags

		// Check if we have a child text
		String textContent = currentNode.getTextContent();
		if (textContent != null && !textContent.trim().isEmpty()
		// Skip attribute if it's already defined in root entity.
				&& !inheritedAttributes.contains(getTextContentAttributeName())) {
			// do not re-declare attribute
			if (!declaredAttributes.contains(getTextContentAttributeName())) {
				writer.println(getTextContentAttributeName() + " sub attribute, value string;");
				// mark attribute as declared
				declaredAttributes.add(getTextContentAttributeName());
			}

			// associate entity and attribute
			writer.println(currentEntityName + " owns " + getTextContentAttributeName() + ";");
		}

		// mark current node/tag as visited
		visitedNodes.add(currentEntityName);

		/*
		 * Recursively visit the child BPMN tags. We may have visited empty tag
		 * previously, so re-visit children to make sure new parent-child relations are
		 * built normally.
		 */
		Collection<BpmnModelElementInstance> childrenToVisit = new ArrayList<>();

		// iterate first on basic BPMN elements
		childrenToVisit.addAll(currentNode.getChildElementsByType(BaseElement.class));

		// The following are special tags in which
		// their "values" should be extracted from child text node instead
		childrenToVisit.addAll(currentNode.getChildElementsByType(FlowNodeRef.class));
		childrenToVisit.addAll(currentNode.getChildElementsByType(Incoming.class));
		childrenToVisit.addAll(currentNode.getChildElementsByType(Outgoing.class));

		// iterate on visual (GUI) elements
		childrenToVisit.addAll(currentNode.getChildElementsByType(BpmnDiagram.class));
		childrenToVisit.addAll(currentNode.getChildElementsByType(DiagramElement.class));
		childrenToVisit.addAll(currentNode.getChildElementsByType(Bounds.class));
		childrenToVisit.addAll(currentNode.getChildElementsByType(Point.class));

		// recursive call
		for (BpmnModelElementInstance child : childrenToVisit) {
			visitEntityRecursive(writer, child, visitedNodes, inheritedAttributes, declaredAttributes,
					declaredRelations);
		}
	}

	/**
	 * Includes some implementation-specific schema elements, such as the xmlns
	 * document namespace for BPMN tags.
	 * 
	 * @param writer              : where to write the script
	 * @param bpmn                : reference to the BPMN object.
	 * @param visitedNodes        : names of BPMN tags that were already visited
	 *                            (attributes of these tags will be skipped)
	 * @param inheritedAttributes : these attributes will not be re-declared (it's
	 *                            supposed to inherit from root "BPMN" entity).
	 * @param declaredAttributes  : attributes that were already declared
	 *                            previously.
	 * @param declaredRelations   : relations that were already declared previously.
	 */
	protected void addImplementationSpecificSchemaEntries(PrintWriter writer, BpmnModelInstance bpmn,
			Set<String> visitedNodes, Set<String> inheritedAttributes, Set<String> declaredAttributes,
			Set<String> declaredRelations) {

		if (!isAddImplementationSpecificSchemaAttributes()) {
			return;
		}

		logger.debug("Adding implementation-specific schema elements");

		writer.println("## =============== Implementation-specific schema elements ===============");

		// xmlns contains schema namespace
		if (!inheritedAttributes.contains(getBPMNEntityNamePrefix() + "xmlns")) {
			if (!declaredAttributes.contains(getBPMNEntityNamePrefix() + "xmlns")) {
				writer.println(getBPMNEntityNamePrefix() + "xmlns sub attribute, value string;");
				// mark as declared
				declaredAttributes.add(getBPMNEntityNamePrefix() + "xmlns");
			}
			writer.println(getBPMNEntityNamePrefix() + "definitions owns " + getBPMNEntityNamePrefix() + "xmlns;");
		}
		writer.println();

		// waypoint's x and y contains coordinates of edges,
		if (!visitedNodes.contains(getBPMNEntityNamePrefix() + "waypoint")) {
			// declare waypoint if it was not declared yet
			writer.println(getBPMNEntityNamePrefix() + "waypoint sub " + getBPMNEntityName() + ";");
			// mark as visited
			visitedNodes.add(getBPMNEntityNamePrefix() + "waypoint");
			writer.println();
		}
		// declare the waypoint's x and y coordinates
		if (!inheritedAttributes.contains(getBPMNEntityNamePrefix() + "x")) {
			if (!declaredAttributes.contains(getBPMNEntityNamePrefix() + "x")) {
				writer.println(getBPMNEntityNamePrefix() + "x sub attribute, value long;");
				// mark as declared
				declaredAttributes.add(getBPMNEntityNamePrefix() + "x");
			}
			writer.println(getBPMNEntityNamePrefix() + "waypoint owns " + getBPMNEntityNamePrefix() + "x;");
		}
		if (!inheritedAttributes.contains(getBPMNEntityNamePrefix() + "y")) {
			if (!declaredAttributes.contains(getBPMNEntityNamePrefix() + "y")) {
				writer.println(getBPMNEntityNamePrefix() + "y sub attribute, value long;");
				// mark as declared
				declaredAttributes.add(getBPMNEntityNamePrefix() + "y");
			}
			writer.println(getBPMNEntityNamePrefix() + "waypoint owns " + getBPMNEntityNamePrefix() + "y;");
		}
		writer.println();

		// We should be able to map an entity in the conceptual model to BPMN entity
		String mappingRelationName = getBPMNConceptualModelMappingName();
		if (!declaredRelations.contains(mappingRelationName)) {

			writer.println(mappingRelationName + " sub relation, relates bpmnEntity, relates conceptualModel;");

			// Specify the roles
			writer.println(getBPMNEntityName() + " plays " + mappingRelationName + ":bpmnEntity;");

			// TypeDB does not allow 'entity' to play a role.
			// Need to explicitly enumerate...
			for (String entityName : getCommaSeparatedMappableConceptualModelEntities().split(",")) {
				if (entityName == null || entityName.trim().isEmpty()) {
					// ignore nulls and blanks.
					continue;
				}

				logger.debug("'{}' will play some role in {}", entityName, mappingRelationName);

				writer.println(entityName + " plays " + mappingRelationName + ":conceptualModel;");
				// TODO create an abstract conceptual model entity instead
			}

			// mark relation as declared
			declaredRelations.add(mappingRelationName);
			writer.println();
		}
	}

	/**
	 * This should generate TypeQL inserts. For instance, simple.bpmn should result
	 * in something similar to the following TypeQL:
	 * 
	 * <pre>
	## Insert BPMN elements
	insert $def isa BPMN_definitions, 
	has BPMN_targetNamespace "https://camunda.org/examples", 
	has BPMN_xmlns "http://www.omg.org/spec/BPMN/20100524/MODEL", 
	has uid "https://camunda.org/examples#definitions123";
	
	insert $proc isa BPMN_process,
	has uid "https://camunda.org/examples#proc123";
	match
	$parent isa BPMN_definitions, has uid "https://camunda.org/examples#definitions123";
	$child isa BPMN_process, has uid "https://camunda.org/examples#proc123";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	insert $startEvent isa BPMN_startEvent,
	has BPMN_id "start",
	has uid "https://camunda.org/examples#start";
	match
	$parent isa entity, has uid "https://camunda.org/examples#proc123";
	$child isa entity, has uid "https://camunda.org/examples#start";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	insert $outgoing isa BPMN_outgoing,
	has BPMN_textContent "flow1",
	has uid "https://camunda.org/examples#outgoing1";
	match
	$parent isa entity, has uid "https://camunda.org/examples#start";
	$child isa entity, has uid "https://camunda.org/examples#outgoing1";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	insert $userTask isa BPMN_userTask,
	has BPMN_id "task",
	has BPMN_name "User Task",
	has uid "https://camunda.org/examples#task";
	match
	$parent isa entity, has uid "https://camunda.org/examples#proc123";
	$child isa entity, has uid "https://camunda.org/examples#task";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	insert $incoming isa BPMN_incoming,
	has BPMN_textContent "flow1",
	has uid "https://camunda.org/examples#taskincoming";
	match
	$parent isa entity, has uid "https://camunda.org/examples#task";
	$child isa entity, has uid "https://camunda.org/examples#taskincoming";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	insert $outgoing isa BPMN_outgoing,
	has BPMN_textContent "flow2",
	has uid "https://camunda.org/examples#taskoutgoing";
	match
	$parent isa entity, has uid "https://camunda.org/examples#task";
	$child isa entity, has uid "https://camunda.org/examples#taskoutgoing";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	insert $sequenceFlow isa BPMN_sequenceFlow,
	has BPMN_id "flow1",
	has BPMN_sourceRef "start",
	has BPMN_targetRef "task",
	has uid "https://camunda.org/examples#flow1";
	match
	$parent isa entity, has uid "https://camunda.org/examples#proc123";
	$child isa entity, has uid "https://camunda.org/examples#flow1";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	insert $endEvent isa BPMN_endEvent,
	has BPMN_id "end",
	has uid "https://camunda.org/examples#end";
	match
	$parent isa entity, has uid "https://camunda.org/examples#proc123";
	$child isa entity, has uid "https://camunda.org/examples#end";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	insert $incoming isa BPMN_incoming,
	has BPMN_textContent "flow2",
	has uid "https://camunda.org/examples#endincoming";
	match
	$parent isa entity, has uid "https://camunda.org/examples#end";
	$child isa entity, has uid "https://camunda.org/examples#endincoming";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	insert $sequenceFlow isa BPMN_sequenceFlow,
	has BPMN_id "flow2",
	has BPMN_sourceRef "task",
	has BPMN_targetRef "end",
	has uid "https://camunda.org/examples#flow2";
	match
	$parent isa entity, has uid "https://camunda.org/examples#proc123";
	$child isa entity, has uid "https://camunda.org/examples#flow2";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	## references to the conceptual model
	insert $mission isa Mission,
	has uid "https://camunda.org/examples#Mission_proc123";
	match
	$bpmnEntity isa BPMN_Entity, has uid 'https://camunda.org/examples#proc123';
	$conceptualModel isa entity, has uid 'https://camunda.org/examples#Mission_proc123';
	insert $rel (bpmnEntity: $bpmnEntity, conceptualModel: $conceptualModel) isa BPMN_hasConceptualModelElement;
	
	insert $task isa Task,
	has uid "https://camunda.org/examples#Task_task";
	match
	$bpmnEntity isa BPMN_Entity, has uid 'https://camunda.org/examples#task';
	$conceptualModel isa entity, has uid 'https://camunda.org/examples#Task_task';
	insert $rel (bpmnEntity: $bpmnEntity, conceptualModel: $conceptualModel) isa BPMN_hasConceptualModelElement;
	match
	$task isa Task, has uid 'https://camunda.org/examples#Task_task';
	$mission isa Mission, has uid 'https://camunda.org/examples#Mission_proc123';
	insert $rel (mission: $mission, task: $task) isa isCompoundBy;
	 * </pre>
	 */
	@Override
	public void encodeData(OutputStream outputStream) throws IOException {
		logger.info("Generating TypeQL data insertion...");
		if (outputStream == null) {
			throw new NullPointerException("Invalid argument: the output stream was null");
		}

		logger.debug("Retrieving cached BPMN model...");
		BpmnModelInstance bpmn = getBPMNModel();
		logger.debug("Cached BPMN model: {}", bpmn);

		logger.debug("Retrieving the namespace to use...");
		String namespace = getInstanceNamespace();

		// namespace must be set
		if (namespace == null || namespace.trim().isEmpty()) {
			logger.warn("No namespace was set. Using default namespace for data...");
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

		// prepare writer for output stream
		try (PrintWriter writer = new PrintWriter(outputStream)) {

			logger.debug("Writing the header");

			// TypeQL schema must start with the keyword "define"
			writer.println("define");
			writer.println();

			writer.println("## =============== Header ===============");
			writer.println();

			writer.println(
					"## Note: attribute uid is required in DALNIM. Uncomment the following line if not declared yet.");
			writer.println("## uid sub attribute, value string;");
			writer.println();

			writer.println("## BPMN entities in general");
			writer.println(getBPMNEntityNamePrefix() + "id sub attribute, value string;");
			writer.println(getBPMNEntityNamePrefix() + "name sub attribute, value string;");
			writer.println(getTextContentAttributeName() + " sub attribute, value string;");
			writer.println(getBPMNEntityName() + " sub entity, owns " + getBPMNEntityNamePrefix() + "id, owns "
					+ getBPMNEntityNamePrefix() + "name, owns " + getTextContentAttributeName() + ", owns uid @key;");
			writer.println();

			// Some attributes are already declared in root "BPMN" entity,
			// so children do not have to re-declare
			Set<String> attributesInRootEntity = new HashSet<>();
			attributesInRootEntity.add("uid");
			attributesInRootEntity.add(getBPMNEntityNamePrefix() + "id");
			attributesInRootEntity.add(getBPMNEntityNamePrefix() + "name");
			attributesInRootEntity.add(getTextContentAttributeName());

			logger.debug("Writing the body...");
			writer.println("## =============== Body ===============");
			writer.println();

			// recursively visit the tree below definitions
			Set<String> visitedNodes = new HashSet<>();
			Set<String> declaredRelations = new HashSet<>();
			Set<String> declaredAttributes = new HashSet<>(attributesInRootEntity);
			visitEntityRecursive(writer, bpmn.getDefinitions(), visitedNodes, attributesInRootEntity,
					declaredAttributes, declaredRelations);

			// declare some attributes specific to our implementation
			addImplementationSpecificSchemaEntries(writer, bpmn, visitedNodes, attributesInRootEntity,
					declaredAttributes, declaredRelations);

			// sanity check
			if (isRunSanityCheck()) {
				runSanityCheck(bpmn, visitedNodes, attributesInRootEntity, declaredAttributes, declaredRelations);
			} // end of sanity check

			writer.println("## =============== End ===============");
			logger.info("Finished TypeQL data insertion");

		} // this will close writer

	}

	/**
	 * 
	 * @param writer : where to write the header
	 * @param bpmn   : reference to the BPMN model.
	 */
	protected void writeDataHeader(PrintWriter writer, BpmnModelInstance bpmn) {
		// TODO Auto-generated method stub
		throw new UnsupportedOperationException("Not implemented yet...");
	}

	/**
	 * Parses a TypeQL script and verifies whether all referred entities/attributes
	 * are also declared.
	 * 
	 * @param typeql : a typeql schema script (which starts with 'define').
	 * @return true if the test passed. False otherwise.
	 */
	public boolean checkDefinitionReferences(String typeql) throws ParseException, TypeQLException {

		logger.debug("Parsing typeql schema:\n{}", typeql);

		TypeQLDefine define = TypeQL.parseQuery(typeql).asDefine();

		// make sure all entities and attributes are defined
		Set<String> declaredEntities = new HashSet<>();
		Set<String> referredEntities = new HashSet<>();
		Set<String> declaredAttributes = new HashSet<>();
		Set<String> referredAttributes = new HashSet<>();
		Map<String, Collection<String>> declaredRelationRoles = new HashMap<>();
		Map<String, Collection<String>> referredRelationRoles = new HashMap<>();

		// iterate on the definitions
		List<TypeVariable> definitions = define.variables();
		for (int definitionIndex = 0; definitionIndex < definitions.size(); definitionIndex++) {

			TypeVariable typeVar = definitions.get(definitionIndex);
			logger.debug("Checking type definition {}: {}", definitionIndex, typeVar);

			// check if this is an attribute
			// Note: we do not allow sub-attributes in our system.
			if (typeVar.sub().isPresent()
					&& "attribute".equals(typeVar.sub().orElseThrow().type().reference().asLabel().label())
					// ignore "uid" since it's part of conceptual model
					&& !typeVar.reference().asLabel().label().equals("uid")) {
				declaredAttributes.add(typeVar.reference().asLabel().label());
				// attributes must declare value type
				if (!typeVar.valueType().isPresent()) {
					throw new ParseException("Attributes must declare value type in '" + typeVar.toString() + "'",
							definitionIndex);
				}
			} else if (typeVar.sub().isPresent()
					&& "relation".equals(typeVar.sub().orElseThrow().type().reference().asLabel().label())) {
				// this should be a relation and roles
				String relationName = typeVar.reference().asLabel().label();
				Set<String> roles = new HashSet<>();
				// iterate on roles
				for (Relates relates : typeVar.relates()) {
					roles.addAll(relates.variables().stream()
							// extract the labels after 'relates'
							.map(ownVar -> ownVar.reference().asLabel().label()).collect(Collectors.toSet()));
				}
				declaredRelationRoles.put(relationName, roles);
			} else {
				// it's a sub-entity (we should avoid sub-attributes and sub-relationships in
				// this system)
				declaredEntities.add(typeVar.reference().asLabel().label());

				if (typeVar.sub().isPresent()
						&& !"entity".equals(typeVar.sub().orElseThrow().type().reference().asLabel().label())
						&& !"relation".equals(typeVar.sub().orElseThrow().type().reference().asLabel().label())) {
					// store references to entities in 'sub' declaration
					referredEntities.add(typeVar.sub().orElseThrow().type().reference().asLabel().label());
				} // else: no need to store references to the top entity
			}
			// store references to attributes in 'owns' declaration
			for (Owns owns : typeVar.owns()) {
				referredAttributes.addAll(owns.variables().stream()
						// extract the labels after 'owns'
						.map(ownVar -> ownVar.reference().asLabel().label())
						// ignore "uid" since it's part of conceptual model
						.filter(label -> (!label.equals("uid"))).collect(Collectors.toSet()));
			}
			// store references to relations/roles in 'plays' declaration
			for (Plays plays : typeVar.plays()) {
				// update map of referred relations and roles
				String roleLabel = plays.role().reference().asLabel().label();
				// role should be like reference:role
				String relationLabel = roleLabel.split(":")[0];
				// reuse the collection if present
				Collection<String> referredRoles = referredRelationRoles.get(relationLabel);
				if (referredRoles == null) {
					// This is 1st time this relation is used.
					referredRoles = new HashSet<>();
				}
				referredRoles.add(roleLabel);
				referredRelationRoles.put(relationLabel, referredRoles);
			}
		} // end of iteration on definitions

		// all referred entities must have a declaration
		if (!declaredEntities.containsAll(referredEntities)) {
			throw new ParseException("All entities must have a declaration. Declared = " + declaredEntities
					+ "; referenced = " + referredEntities, definitions.size());
		}

		// all referred attributes must have a declaration
		if (!declaredAttributes.containsAll(referredAttributes)) {
			throw new ParseException("All referred attributes must have a declaration. Declared = " + declaredAttributes
					+ "; referred = " + referredAttributes, definitions.size());
		}

		// all referred relations/roles should have a declaration
		for (Entry<String, Collection<String>> referredEntry : referredRelationRoles.entrySet()) {
			// the relation must be declared
			if (!declaredRelationRoles.containsKey(referredEntry.getKey())) {
				throw new ParseException("All referred relation must have a declaration. Relation was " + referredEntry,
						definitions.size());
			}
			// the roles must be declared
			Collection<String> declaredRoles = declaredRelationRoles.get(referredEntry.getKey());
			if (!declaredRoles.containsAll(referredEntry.getValue())) {
				throw new ParseException("All referred roles must have a declaration. Declared = "
						+ declaredRelationRoles + "; used = " + referredEntry, definitions.size());
			}
		}

		return true;
	}

	/**
	 * @return the {@link BpmnModelInstance} loaded in
	 *         {@link #loadInput(InputStream)}
	 */
	public BpmnModelInstance getBPMNModel() {
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

	/**
	 * @return name of the common root entity of BPMN elements.
	 */
	public String getBPMNEntityName() {
		return bpmnEntityName;
	}

	/**
	 * @param bPMNEntityName : name of the common root entity of BPMN elements.
	 */
	public void setBPMNEntityName(String bPMNEntityName) {
		bpmnEntityName = bPMNEntityName;
	}

	/**
	 * @return the isRunSanityCheck
	 */
	public boolean isRunSanityCheck() {
		return isRunSanityCheck;
	}

	/**
	 * @param isRunSanityCheck the isRunSanityCheck to set
	 */
	public void setRunSanityCheck(boolean isRunSanityCheck) {
		this.isRunSanityCheck = isRunSanityCheck;
	}

	/**
	 * @return the isAddImplementationSpecificSchemaAttributes
	 */
	public boolean isAddImplementationSpecificSchemaAttributes() {
		return isAddImplementationSpecificSchemaAttributes;
	}

	/**
	 * @param isAddSpecialAttributes the isAddSpecialAttributes to set
	 */
	public void setAddImplementationSpecificSchemaAttributes(boolean isAddSpecialAttributes) {
		this.isAddImplementationSpecificSchemaAttributes = isAddSpecialAttributes;
	}

	/**
	 * @return the textContentAttributeName
	 */
	public String getTextContentAttributeName() {
		return textContentAttributeName;
	}

	/**
	 * @param textContentAttributeName the textContentAttributeName to set
	 */
	public void setTextContentAttributeName(String textContentAttributeName) {
		this.textContentAttributeName = textContentAttributeName;
	}

	/**
	 * @return the prefix to be used in all entities/attributes/relations generated
	 *         by this class.
	 */
	public String getBPMNEntityNamePrefix() {
		return bpmnEntityNamePrefix;
	}

	/**
	 * @param bpmnEntityNamePrefix : the prefix to be used in all
	 *                             entities/attributes/relations generated by this
	 *                             class.
	 */
	public void setBPMNEntityNamePrefix(String bpmnEntityNamePrefix) {
		this.bpmnEntityNamePrefix = bpmnEntityNamePrefix;
	}

	/**
	 * @return the bPMNConceptualModelMappingName
	 */
	public String getBPMNConceptualModelMappingName() {
		return bpmnConceptualModelMappingName;
	}

	/**
	 * @param bPMNConceptualModelMappingName the bPMNConceptualModelMappingName to
	 *                                       set
	 */
	public void setBPMNConceptualModelMappingName(String bPMNConceptualModelMappingName) {
		bpmnConceptualModelMappingName = bPMNConceptualModelMappingName;
	}

	/**
	 * @return the bPMNParentChildRelationName
	 */
	public String getBPMNParentChildRelationName() {
		return bpmnParentChildRelationName;
	}

	/**
	 * @param bPMNParentChildRelationName the bPMNParentChildRelationName to set
	 */
	public void setBPMNParentChildRelationName(String bPMNParentChildRelationName) {
		bpmnParentChildRelationName = bPMNParentChildRelationName;
	}

	/**
	 * @return comma-separated string listing the names of entities in the
	 *         conceptual model that can be mapped to
	 *         {@link #getBPMNConceptualModelMappingName()} (i.e., those that can
	 *         play a role in this mapping relation).
	 */
	public synchronized String getCommaSeparatedMappableConceptualModelEntities() {
		if (commaSeparatedMappableConceptualModelEntities == null) {
			commaSeparatedMappableConceptualModelEntities = "";
		}
		return commaSeparatedMappableConceptualModelEntities;
	}

	/**
	 * @param commaSeparatedVal : comma-separated string listing the names of
	 *                          entities in the conceptual model that can be mapped
	 *                          to {@link #getBPMNConceptualModelMappingName()}
	 *                          (i.e., those that can play a role in this mapping
	 *                          relation).
	 */
	public synchronized void setCommaSeparatedMappableConceptualModelEntities(String commaSeparatedVal) {
		this.commaSeparatedMappableConceptualModelEntities = commaSeparatedVal;
	}

}
