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
import java.util.Objects;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

import org.camunda.bpm.model.bpmn.Bpmn;
import org.camunda.bpm.model.bpmn.BpmnModelInstance;
import org.camunda.bpm.model.bpmn.instance.BpmnModelElementInstance;
import org.camunda.bpm.model.xml.impl.instance.DomElementWrapper;
import org.camunda.bpm.model.xml.instance.ModelElementInstance;
import org.camunda.bpm.model.xml.type.ModelElementType;
import org.camunda.bpm.model.xml.type.attribute.Attribute;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.w3c.dom.Element;
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import com.vaticle.typeql.lang.TypeQL;
import com.vaticle.typeql.lang.common.exception.TypeQLException;
import com.vaticle.typeql.lang.pattern.constraint.TypeConstraint.Owns;
import com.vaticle.typeql.lang.pattern.constraint.TypeConstraint.Plays;
import com.vaticle.typeql.lang.pattern.constraint.TypeConstraint.Relates;
import com.vaticle.typeql.lang.pattern.variable.TypeVariable;
import com.vaticle.typeql.lang.query.TypeQLDefine;

import edu.gmu.c4i.dalnim.util.ApplicationProperties;

/**
 * <p>
 * Default implementation of {@link Encoder} to parse BPMN files with Camunda
 * libraries and save TypeQL scripts.
 * </p>
 * <p>
 * This class expects that a TypeDB schema like the following is already set up.
 * </p>
 * 
 * <pre>
 * define
 * 
 * uid sub attribute, value string;
 * Mission sub entity, owns uid @key;
 * Task sub entity, owns uid @key;
 * Performer sub entity, owns uid @key;
 * Resource sub entity, owns uid @key;
 * 
 * isCompoundBy sub relation, relates mission, relates task;
 * Mission plays isCompoundBy:mission;
 * Task plays isCompoundBy:task;
 * 
 * requires sub relation, relates task, relates resource;
 * Task plays requires:task;
 * Resource plays requires:resource;
 * 
 * isPerformedBy sub relation, relates task, relates performer;
 * Task plays isPerformedBy:task;
 * Performer plays isPerformedBy:performer;
 * </pre>
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

	private String bpmnAttributeNamePrefix = "BPMNattrib_";

	private String bpmnEntityName = bpmnEntityNamePrefix + "Entity";

	private String bpmnTextContentAttributeName = bpmnEntityNamePrefix + "textContent";

	private String bpmnConceptualModelMappingName = bpmnEntityNamePrefix + "hasConceptualModelElement";

	private String bpmnParentChildRelationName = bpmnEntityNamePrefix + "hasChildTag";

	private String jsonBPMNConceptualModelMap = "{'definitions':'Mission','@org.camunda.bpm.model.bpmn.instance.Task':'Task'}";

	private boolean ignoreInvalidAttributeName = true;

	private boolean mapBPMNToConceptualModel;

	private String isCompoundByRelationName = "isCompoundBy";

	private String isPerformedByRelationName = "isPerformedBy";

	private String requiresRelationName = "requires";

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

			writer.println("## =============== Begin ===============");

			// TypeQL schema must start with the keyword "define"
			logger.debug("Writing the header");
			writer.println("define");
			writer.println();

			if (isMapBPMNToConceptualModel()) {
				writer.println(
						"## Note: attribute uid is required in DALNIM. Uncomment the following line if not declared yet.");
				writer.println("## uid sub attribute, value string;");
			} else {
				writer.println("uid sub attribute, value string;");
			}
			writer.println();

			writer.println("## BPMN entities in general");
			writer.println(getBPMNAttributeNamePrefix() + "id sub attribute, value string;");
			writer.println(getBPMNAttributeNamePrefix() + "name sub attribute, value string;");
			writer.println(getBPMNTextContentAttributeName() + " sub attribute, value string;");
			writer.println(getBPMNEntityName() + " sub entity, owns " + getBPMNAttributeNamePrefix() + "id, owns "
					+ getBPMNAttributeNamePrefix() + "name, owns " + getBPMNTextContentAttributeName()
					+ ", owns uid @key;");
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
			attributesInRootEntity.add(getBPMNAttributeNamePrefix() + "id");
			attributesInRootEntity.add(getBPMNAttributeNamePrefix() + "name");
			attributesInRootEntity.add(getBPMNTextContentAttributeName());

			logger.debug("Writing the body...");
			writer.println("## =============== Body ===============");
			writer.println();

			// store what was already declared
			Set<String> declaredAttributes = new HashSet<>(attributesInRootEntity);

			Set<String> declaredRelations = new HashSet<>();
			declaredRelations.add(getBPMNParentChildRelationName());

			Set<String> visitedNodes = new HashSet<>();

			// recursively visit what's below "definitions" tag
			visitBPMNSchemaRecursive(writer, bpmn.getDefinitions(), visitedNodes, attributesInRootEntity,
					declaredAttributes, declaredRelations);

			// declare some attributes specific to our implementation
			addImplementationSpecificSchemaEntries(writer, bpmn, visitedNodes, attributesInRootEntity,
					declaredAttributes, declaredRelations);

			// sanity check
			if (isRunSanityCheck()) {
				runSanityCheck(bpmn, visitedNodes, declaredAttributes, declaredRelations);
			} // end of sanity check

			writer.println("## =============== End ===============");
			logger.info("Finished TypeQL schema definitions.");

		} // this will close writer

	}

	/**
	 * Run basic sanity check on the structures generated in
	 * {@link #encodeSchema(OutputStream)}
	 * 
	 * @param bpmn               : reference to the BPMN object.
	 * @param visitedNodes       : names of BPMN tags that were already visited
	 *                           (attributes of these tags will be skipped)
	 * @param declaredAttributes : attributes that were already declared previously.
	 * @param declaredRelations  : relations that were already declared previously.
	 */
	protected void runSanityCheck(BpmnModelInstance bpmn, Set<String> visitedNodes, Set<String> declaredAttributes,
			Set<String> declaredRelations) throws IOException {

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

		if (!declaredAttributes.contains(getBPMNAttributeNamePrefix() + "isExecutable")) {
			throw new IOException("Sanity check failed: attribute 'isExecutable' was not created.");
		}

		// sanity check on attributes
		if (visitedNodes.contains(getBPMNEntityNamePrefix() + "serviceTask")) {
			if (!declaredAttributes.contains(getBPMNAttributeNamePrefix() + "implementation")) {
				throw new IOException("Sanity check failed: attribute 'implementation' was not created.");
			}
			if (!declaredAttributes.contains(getBPMNAttributeNamePrefix() + "operationRef")) {
				throw new IOException("Sanity check failed: attribute 'operationRef' was not created.");
			}
		}
		if (visitedNodes.contains(getBPMNEntityNamePrefix() + "participant")
				&& !declaredAttributes.contains(getBPMNAttributeNamePrefix() + "processRef")) {
			throw new IOException("Sanity check failed: attribute 'processRef' was not created.");
		}
		if (visitedNodes.contains(getBPMNEntityNamePrefix() + "messageFlow")
				|| visitedNodes.contains(getBPMNEntityNamePrefix() + "sequenceFlow")) {
			if (!declaredAttributes.contains(getBPMNAttributeNamePrefix() + "sourceRef")) {
				throw new IOException("Sanity check failed: attribute 'sourceRef' was not created.");
			}
			if (!declaredAttributes.contains(getBPMNAttributeNamePrefix() + "targetRef")) {
				throw new IOException("Sanity check failed: attribute 'targetRef' was not created.");
			}
		}

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
	protected void visitBPMNSchemaRecursive(PrintWriter writer, ModelElementInstance currentNode,
			Set<String> visitedNodes, Set<String> inheritedAttributes, Set<String> declaredAttributes,
			Set<String> declaredRelations) throws IOException {

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
			for (Entry<String, String> attrib : getAllAttributes(currentNode,
					// true = include those defined in the BPMN element type
					// (because not all BPMN files uses all attributes)
					true).entrySet()) {

				String attributeName = getBPMNAttributeNamePrefix() + attrib.getKey();

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

			} // end of iteration on attributes

			writer.println();

		} // else we visited this node already

		// Check if we have a child text
		String textContent = currentNode.getTextContent();
		if (textContent != null && !textContent.trim().isEmpty()
		// Skip attribute if it's already defined in root entity.
				&& !inheritedAttributes.contains(getBPMNTextContentAttributeName())) {
			// do not re-declare attribute
			if (!declaredAttributes.contains(getBPMNTextContentAttributeName())) {
				writer.println(getBPMNTextContentAttributeName() + " sub attribute, value string;");
				// mark attribute as declared
				declaredAttributes.add(getBPMNTextContentAttributeName());
			}

			// associate entity and attribute
			writer.println(currentEntityName + " owns " + getBPMNTextContentAttributeName() + ";");
		}

		// mark current node/tag as visited
		visitedNodes.add(currentEntityName);

		/*
		 * Recursively visit the child BPMN tags. We may have visited empty tag
		 * previously, so re-visit children to make sure new parent-child relations are
		 * built normally.
		 */
		Collection<ModelElementInstance> childrenToVisit = new ArrayList<>();

		// iterate on known elements only
		for (ModelElementType childType : currentNode.getElementType().getAllChildElementTypes()) {
			childrenToVisit.addAll(currentNode.getChildElementsByType(childType));
		}

		// recursive call
		for (ModelElementInstance child : childrenToVisit) {
			visitBPMNSchemaRecursive(writer, child, visitedNodes, inheritedAttributes, declaredAttributes,
					declaredRelations);
		}
	}

	/**
	 * <p>
	 * Includes some implementation-specific schema elements, such as the xmlns
	 * document namespace for BPMN tags.
	 * </p>
	 * <p>
	 * Rules will be also created. Examples of TypeQL queries involving these rules
	 * can be:
	 * </p>
	 * 
	 * <pre>
	 * ## query isCompoundBy
	 * match 
	 * $r isa isCompoundBy; 
	 * $m isa Mission, has uid $muid; 
	 * $t isa Task, has uid $tuid; 
	 * (bpmnEntity: $bpmntask, conceptualModel: $t) isa BPMN_hasConceptualModelElement;
	 * $bpmntask isa BPMN_Entity, has uid $buid;
	 * get $m,$t,$r,$bpmntask,$muid,$tuid,$buid;
	 * 
	 * ## query isPerformedBy
	 * match
	 * $task isa Task, has uid $uid1;
	 * $performer isa Performer, has uid $uid2;
	 * $bpmntask isa BPMN_Entity, has uid $uid3;
	 * $bpmnlane isa BPMN_lane, has uid $uid4;
	 * $rel (task: $task, performer: $performer) isa isPerformedBy;
	 * (bpmnEntity: $bpmntask, conceptualModel: $task) isa BPMN_hasConceptualModelElement;
	 * (bpmnEntity: $bpmnlane, conceptualModel: $performer) isa BPMN_hasConceptualModelElement;
	 * get $rel, $uid1, $uid2, $uid3, $uid4, $bpmntask, $bpmnlane;
	 * 
	 * ## query requires
	 * match
	 * $dataObject isa BPMN_dataObject, has uid $uid1;
	 * $resource isa Resource, has uid $uid2;
	 * $bpmntask isa BPMN_Entity, has uid $uid3;
	 * $task isa Task, has uid $uid4;
	 * $rel (task: $task, resource: $resource) isa requires;
	 * (bpmnEntity: $bpmntask, conceptualModel: $task) isa BPMN_hasConceptualModelElement;
	 * (bpmnEntity: $dataObject, conceptualModel: $resource) isa BPMN_hasConceptualModelElement;
	 * get $rel, $dataObject, $resource, $bpmntask, $task , $uid1, $uid2, $uid3, $uid4;
	 * </pre>
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
		if (!inheritedAttributes.contains(getBPMNAttributeNamePrefix() + "xmlns")) {
			if (!declaredAttributes.contains(getBPMNAttributeNamePrefix() + "xmlns")) {
				writer.println(getBPMNAttributeNamePrefix() + "xmlns sub attribute, value string;");
				// mark as declared
				declaredAttributes.add(getBPMNAttributeNamePrefix() + "xmlns");
			}
			writer.println(getBPMNEntityNamePrefix() + "definitions owns " + getBPMNAttributeNamePrefix() + "xmlns;");
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
		if (!inheritedAttributes.contains(getBPMNAttributeNamePrefix() + "x")) {
			if (!declaredAttributes.contains(getBPMNAttributeNamePrefix() + "x")) {
				writer.println(getBPMNAttributeNamePrefix() + "x sub attribute, value string;");
				// mark as declared
				declaredAttributes.add(getBPMNAttributeNamePrefix() + "x");
			}
			writer.println(getBPMNEntityNamePrefix() + "waypoint owns " + getBPMNAttributeNamePrefix() + "x;");
		}
		if (!inheritedAttributes.contains(getBPMNAttributeNamePrefix() + "y")) {
			if (!declaredAttributes.contains(getBPMNAttributeNamePrefix() + "y")) {
				writer.println(getBPMNAttributeNamePrefix() + "y sub attribute, value string;");
				// mark as declared
				declaredAttributes.add(getBPMNAttributeNamePrefix() + "y");
			}
			writer.println(getBPMNEntityNamePrefix() + "waypoint owns " + getBPMNAttributeNamePrefix() + "y;");
		}
		writer.println();

		// We should be able to map an entity in the conceptual model to BPMN entity
		if (isMapBPMNToConceptualModel()) {
			String mappingRelationName = getBPMNConceptualModelMappingName();
			if (!declaredRelations.contains(mappingRelationName)) {
				writer.println("## =============== Mapping to conceptual model ===============");

				writer.println(mappingRelationName + " sub relation, relates bpmnEntity, relates conceptualModel;");

				// Specify the roles
				writer.println(getBPMNEntityName() + " plays " + mappingRelationName + ":bpmnEntity;");

				// TypeDB does not allow 'entity' to play a role.
				// Need to explicitly enumerate...
				// TODO create an abstract conceptual model entity instead of enumerating each
				parseBPMNtoConceptualModelJSONMap()
						// get all values (values are entities in conceptual model)
						.values().stream()
						// remove repetitions
						.distinct()
						// ignore nulls and blanks.
						.filter(Objects::nonNull).filter(name -> !name.trim().isEmpty())
						// add entry: <entityName> plays BPMN_hasConceptualModelElement:conceptualModel
						.forEach(entityName -> {
							logger.debug("'{}' will play some role in {}", entityName, mappingRelationName);
							writer.println(entityName + " plays " + mappingRelationName + ":conceptualModel;");
						});

				// mark relation as declared
				declaredRelations.add(mappingRelationName);
				writer.println();

			} else {
				// the relation was already declared...
				logger.warn("The relation '{}' (BPMN -> conceptual model) was already declared. Skipping...",
						mappingRelationName);
			}

			// add rules

			writer.println("## Rules that inject BPMN semantics to entities in the conceptual model");
			writer.println();

			writer.println("## Task isCompoundBy Mission");
			writer.println("rule rule_misson_isCompoundBy_task:\n" + "when {\n" + "\t $bpmndefinitions isa "
					+ getBPMNEntityNamePrefix() + "definitions;\n" + "\t $bpmnprocess isa " + getBPMNEntityNamePrefix()
					+ "process;\n" + "\t $mission isa Mission;\n" + "\t $task isa Task;\n"
					+ "\t (parent: $bpmndefinitions, child: $bpmnprocess) isa " + getBPMNParentChildRelationName()
					+ ";\n" + "\t (parent: $bpmnprocess, child: $bpmntask) isa " + getBPMNParentChildRelationName()
					+ ";\n" + "\t (bpmnEntity: $bpmndefinitions, conceptualModel: $mission) isa "
					+ getBPMNConceptualModelMappingName() + ";\n"
					+ "\t (bpmnEntity: $bpmntask, conceptualModel: $task) isa " + getBPMNConceptualModelMappingName()
					+ ";\n" + "} then {\n" + "\t (mission: $mission, task: $task) isa " + getIsCompoundByRelationName()
					+ ";\n" + "};");
			writer.println();

			writer.println("## Task isPerformedBy Performer");
			writer.println("rule rule_task_isperformedBy_performer:\n" + "when {\n" + "\t $bpmnflowNodeRef isa "
					+ getBPMNEntityNamePrefix() + "flowNodeRef, has " + getBPMNTextContentAttributeName()
					+ " $id-ref;\n" + "\t $bpmntask isa " + getBPMNEntityName() + ", has "
					+ getBPMNAttributeNamePrefix() + "id $id;\n" + "\t $id = $id-ref;\n" + "\t $task isa Task;\n"
					+ "\t $performer isa Performer;\n" + "\t (bpmnEntity: $bpmntask, conceptualModel: $task) isa "
					+ getBPMNConceptualModelMappingName() + ";\n"
					+ "\t (parent: $bpmnlane, child: $bpmnflowNodeRef) isa BPMN_hasChildTag;\n"
					+ "\t (bpmnEntity: $bpmnlane, conceptualModel: $performer) isa "
					+ getBPMNConceptualModelMappingName() + ";\n" + "} then {\n"
					+ "\t (task: $task, performer: $performer) isa " + getIsPerformedByRelationName() + ";\n" + "};");
			writer.println();

			writer.println("## Task requires Resource");
			writer.println("rule rule_task_requries_resource:\n" + "when {\n" + "\t $dataObject isa "
					+ getBPMNEntityNamePrefix() + "dataObject, has " + getBPMNAttributeNamePrefix() + "id $data_id;\n"
					+ "\t $resource isa Resource;\n" + "\t $bpmntask isa " + getBPMNEntityName() + ";\n"
					+ "\t $task isa Task;\n" + "\t $dataInputAssociation isa " + getBPMNEntityNamePrefix()
					+ "dataInputAssociation;\n" + "\t $sourceRef isa " + getBPMNEntityNamePrefix() + "sourceRef, has "
					+ getBPMNTextContentAttributeName() + " $source;\n" + "\t $source = $data_id;\n"
					+ "\t (bpmnEntity: $dataObject, conceptualModel: $resource) isa "
					+ getBPMNConceptualModelMappingName() + ";\n"
					+ "\t (bpmnEntity: $bpmntask, conceptualModel: $task) isa " + getBPMNConceptualModelMappingName()
					+ ";\n" + "\t (parent: $bpmntask, child: $dataInputAssociation) isa "
					+ getBPMNParentChildRelationName() + ";\n"
					+ "\t (parent: $dataInputAssociation, child: $sourceRef) isa " + getBPMNParentChildRelationName() + ";\n"
					+ "} then {\n" + "\t (task: $task, resource: $resource) isa requires;\n" + "};");
			writer.println();

			// Show sample queries
			writer.println("## Sample queries for the above rules");
			writer.println();

			writer.println("## query isCompoundBy");
			writer.println("# match \n" + "# $r isa isCompoundBy; \n" + "# $m isa Mission, has uid $muid; \n"
					+ "# $t isa Task, has uid $tuid; \n"
					+ "# (bpmnEntity: $bpmntask, conceptualModel: $t) isa BPMN_hasConceptualModelElement;\n"
					+ "# $bpmntask isa BPMN_Entity, has uid $buid;\n" + "# get $m,$t,$r,$bpmntask,$muid,$tuid,$buid;");
			writer.println();

			writer.println("## query isPerformedBy");
			writer.println("# match\n" + "# $task isa Task, has uid $uid1;\n"
					+ "# $performer isa Performer, has uid $uid2;\n" + "# $bpmntask isa BPMN_Entity, has uid $uid3;\n"
					+ "# $bpmnlane isa BPMN_lane, has uid $uid4;\n"
					+ "# $rel (task: $task, performer: $performer) isa isPerformedBy;\n"
					+ "# (bpmnEntity: $bpmntask, conceptualModel: $task) isa BPMN_hasConceptualModelElement;\n"
					+ "# (bpmnEntity: $bpmnlane, conceptualModel: $performer) isa BPMN_hasConceptualModelElement;\n"
					+ "# get $rel, $uid1, $uid2, $uid3, $uid4, $bpmntask, $bpmnlane;");
			writer.println();

			writer.println("## query requires");
			writer.println("# match\n" + "# $dataObject isa BPMN_dataObject, has uid $uid1;\n"
					+ "# $resource isa Resource, has uid $uid2;\n" + "# $bpmntask isa BPMN_Entity, has uid $uid3;\n"
					+ "# $task isa Task, has uid $uid4;\n" + "# $rel (task: $task, resource: $resource) isa requires;\n"
					+ "# (bpmnEntity: $bpmntask, conceptualModel: $task) isa BPMN_hasConceptualModelElement;\n"
					+ "# (bpmnEntity: $dataObject, conceptualModel: $resource) isa BPMN_hasConceptualModelElement;\n"
					+ "# get $rel, $dataObject, $resource, $bpmntask, $task , $uid1, $uid2, $uid3, $uid4;");
			writer.println();

		} // else ignore mappings to conceptual model

	}

	/**
	 * @return parsed {@link #getJSONBPMNConceptualModelMap()}
	 */
	protected Map<String, String> parseBPMNtoConceptualModelJSONMap() {

		Map<String, String> ret = new HashMap<>();

		// parse the JSON
		JSONObject json = new JSONObject(getJSONBPMNConceptualModelMap());

		// keys are names of BPMN entities,
		// values are entities in the concept model.
		for (String bpmnEntity : json.keySet()) {
			ret.put(bpmnEntity, json.getString(bpmnEntity));
		}

		return ret;
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

			logger.debug("Writing the data");

			writer.println("## =============== Begin ===============");
			writer.println("## Insert BPMN elements");
			writer.println();

			// Recursively visit BPMN nodes to write data.
			visitBPMNDataRecursive(writer,
					// consider <definitions> as the root tag in BPMN
					// (although in practice we have the <XML> root tag above.
					bpmn.getDefinitions(),
					// Namespace will be used as prefix of UID.
					namespace,
					// There is no parent UID
					null,
					// UIDs should be unique, so keep track of them with a set
					new HashSet<>(),
					// specify a map from BPMN element to entity in conceptual model
					parseBPMNtoConceptualModelJSONMap());

			writer.println("## =============== End ===============");

			logger.info("Finished TypeQL data insertion");

		} // this will close writer

	}

	/**
	 * Recursively visit BPMN nodes to write data.
	 * 
	 * @param writer                   : where to write the script block.
	 * @param currentNode              : current BPMN tag to handle
	 * @param namespace                : the namespace to use in UIDs.
	 * @param parentUID                : the UID of parent XML tag, if any.
	 * @param usedUIDs                 : keeps track of UIDs that were used
	 * @param bpmnToConceptualModelMap : map from BPMN elements to Conceptual Model.
	 *                                 See
	 *                                 {@link #parseBPMNtoConceptualModelJSONMap()},
	 *                                 {@link #getJSONBPMNConceptualModelMap()}, and
	 *                                 {@link #getBPMNConceptualModelMappingName()}.
	 */
	protected void visitBPMNDataRecursive(PrintWriter writer, ModelElementInstance currentNode, String namespace,
			String parentUID, Set<String> usedUIDs, Map<String, String> bpmnToConceptualModelMap) throws IOException {

		logger.debug("Visiting BPMN tag/node {}", currentNode);

		if (currentNode == null) {
			logger.debug("BPMN node was null. Ignoring...");
			return;
		}
		if (writer == null) {
			logger.warn("Writer node was null. Returning...");
			return;
		}
		if (usedUIDs == null) {
			usedUIDs = new HashSet<>();
		}

		// Extract the entity name
		String currentEntityOriginalName = currentNode.getDomElement().getLocalName();
		String currentEntityName = getBPMNEntityNamePrefix() + currentEntityOriginalName;
		logger.debug("Entity: {}", currentEntityName);

		/**
		 * Insert the current element as follows
		 * 
		 * <pre>
		 * insert $x isa BPMN_definitions, 
		 * 		has BPMN_targetNamespace "https://camunda.org/examples", 
		 * 		has BPMN_xmlns "http://www.omg.org/spec/BPMN/20100524/MODEL", 
		 * 		has BPMN_textContent "flow2",
		 * 		has uid "https://camunda.org/examples#definitions123";
		 * </pre>
		 */

		writer.println("## " + currentEntityOriginalName);
		writer.println("insert $x isa " + currentEntityName + ",");

		// If there's an attribute called "id",
		// we should use it as the radical/base of uid.
		String currentID =
				// if not found, use entity name as base
				currentEntityOriginalName;
		// Iterate on all attributes.
		for (Entry<String, String> attrib : getAllAttributes(currentNode,
				// false = only iterate on attributes that
				// were actually "used" in this BPMN project
				false).entrySet()) {

			// Extract the attribute name and values...
			// The original name
			String attributeOriginalName = attrib.getKey();
			// The name to use when saving to TypeQL
			String attributeNameToSave = getBPMNAttributeNamePrefix() + attributeOriginalName;
			// The value of this attribute
			String attributeValue = attrib.getValue();

			// Ignore null or blank values.
			if (attributeValue == null || attributeValue.trim().isEmpty()) {
				logger.debug("Attribute '{}' in {} was blank.", attributeOriginalName, currentEntityOriginalName);
				continue;
			}

			// If this is the "id", remember its value.
			if (attributeOriginalName.equalsIgnoreCase("id")) {
				currentID = attributeValue;
			}

			// has BPMN_xmlns "http://www.omg.org/spec/BPMN/20100524/MODEL",
			writer.println("\t has " + attributeNameToSave + " \"" + attributeValue + "\",");

		} // end of iteration on attributes

		// Also check if we have a child text,
		// because child texts will be saved as attributes in TypeDB.

		// currentNode.getTextContent() is returning the text of all descendants,
		// so use a special method to obtain the immediate text child.
		Optional<String> optText = getTextContent(currentNode);
		if (!optText.isEmpty()) {
			// has BPMN_textContent "flow2",
			writer.println("\t has " + getBPMNTextContentAttributeName() + " \"" + optText.get() + "\",");
		}

		// All entities must have an UID.
		// Obtain a unique ID with namespace.
		// Use the current ID as base prefix.
		String currentUID = getNewUID(namespace, currentID, usedUIDs);

		// mark this ID as "used"
		usedUIDs.add(currentUID);

		// has uid "<UID>"
		writer.println("\t has uid \"" + currentUID + "\";");

		// Connect the current BPMN/XML tag to its parent tag.
		ModelElementInstance parentNode = currentNode.getParentElement();
		if (parentNode != null) {
			// The parent UID must be specified.
			if (parentUID != null && !parentUID.trim().isEmpty()) {
				/**
				 * Insert the XML parent-child tag relationship as follows:
				 * 
				 * <pre>
				 * match
				 * 		$parent isa BPMN_Entity, has uid "https://camunda.org/examples#definitions123";
				 * 		$child isa BPMN_Entity, has uid "https://camunda.org/examples#proc123";
				 * insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
				 * </pre>
				 */
				writer.println("match");
				writer.println("\t $parent isa " + getBPMNEntityName() + ", has uid \"" + parentUID + "\";");
				writer.println("\t $child isa " + getBPMNEntityName() + ", has uid \"" + currentUID + "\";");
				writer.println(
						"insert $rel (parent: $parent, child: $child) isa " + getBPMNParentChildRelationName() + ";");
			} else {
				throw new IOException("No BPMN element with UID '" + parentUID + "' was found in the parent of '"
						+ currentEntityOriginalName + "'.");
			}
		} // else no parent XML/BPMN tag was found
		writer.println();

		// handle the mapping to conceptual model entities.
		if (isMapBPMNToConceptualModel()) {
			// Extract the entity in the conceptual model
			// which is mapped with current BPMN element.
			String conceptModelEntity = bpmnToConceptualModelMap.get(currentEntityOriginalName);
			if (conceptModelEntity == null) {
				// We didn't find an exact match.
				// However, keys starting with '@' (i.e., '@class' key) represent Java classes.
				// Find a compatible class...
				for (String key : bpmnToConceptualModelMap.keySet().stream()
						// get all keys that starts with "@"
						.filter(key -> key.startsWith("@")).collect(Collectors.toSet())) {
					// Obtain the class name, which is after '@'.
					String className = key.substring(1);
					// load the class and check if its compatible with current BPMN node.
					try {
						Class<?> clz = Class.forName(className);
						if (clz.isAssignableFrom(currentNode.getClass())) {
							// Current node is compatible (it's equal or a subclass of the specified class).
							conceptModelEntity = bpmnToConceptualModelMap.get(key);
							logger.debug(
									"Found matching class {} for current BPMN entity {}. Only the 1st match will be used...",
									key, currentEntityOriginalName);
							// just use the 1st one we found
							break;
						}
					} catch (ClassNotFoundException e) {
						logger.warn("Invalid '@class' found in mapping from BPMN to conceptual model. Key = {}", key,
								e);
					}
				} // end of iteration on '@class' keys
			} else {
				// We found an exact match
				logger.debug("Found exact mapping: {} -> {}", currentEntityOriginalName, conceptModelEntity);
			}

			// Add references/mappings to the conceptual model, if any.
			if (conceptModelEntity != null && !conceptModelEntity.trim().isEmpty()) {
				logger.debug("Mapping: {} -> {}", currentEntityOriginalName, conceptModelEntity);

				// Create an UID for the mapped instance in the conceptual model.
				// The UID will look like "https://camunda.org/examples#Mission_proc123"
				String conceptUID = getNewUID(
						// https://camunda.org/examples#
						namespace,
						// Mission
						conceptModelEntity
								// _proc123
								+ "_" + currentID,
						// avoid duplicates
						usedUIDs);

				// Mark this UID as used.
				usedUIDs.add(conceptUID);

				/**
				 * The mapping should look like:
				 * 
				 * <pre>
				 * insert $concept isa Mission, has uid "https://camunda.org/examples#Mission_proc123";
				 * match
				 * 		$bpmnEntity isa BPMN_Entity, has uid 'https://camunda.org/examples#proc123';
				 * 		$concept isa entity, has uid 'https://camunda.org/examples#Mission_proc123';
				 * insert $rel (bpmnEntity: $bpmnEntity, conceptualModel: $concept) isa BPMN_hasConceptualModelElement;
				 * </pre>
				 */
				writer.println("## Mapping to the conceptual model");
				// Add the new concept instance
				writer.println("insert $concept isa " + conceptModelEntity + ", has uid \"" + conceptUID + "\";");
				// Add the relation to the above instance
				writer.println("match");
				writer.println("\t $bpmnEntity isa " + getBPMNEntityName() + ", has uid '" + currentUID + "';");
				writer.println("\t $concept isa entity, has uid '" + conceptUID + "';");
				writer.println("insert $rel (bpmnEntity: $bpmnEntity, conceptualModel: $concept) isa "
						+ getBPMNConceptualModelMappingName() + ";");
				writer.println();
			} // else this BPMN entity does not map to any entity in the conceptual model

		} // else skip mapping to conceptual model

		/*
		 * Recursively visit the child BPMN tags. We may have visited empty tag
		 * previously, so re-visit children to make sure new parent-child relations are
		 * built normally.
		 */
		Collection<ModelElementInstance> childrenToVisit = new ArrayList<>();

		for (ModelElementType childType : currentNode.getElementType().getAllChildElementTypes()) {
			// Consider only known child elements
			childrenToVisit.addAll(currentNode.getChildElementsByType(childType));
		}

		// Do recursive call
		for (ModelElementInstance child : childrenToVisit) {
			visitBPMNDataRecursive(writer,
					// visit the child XML tag
					child,
					// the namespace (prefix of new UID) should be the same for all tags
					namespace,
					// make sure the child knows the UID of its parent
					currentUID,
					// always avoid duplicate UIDs
					usedUIDs,
					// reuse same mapping from BPMN to conceptual model
					bpmnToConceptualModelMap);
		}

	}

	/**
	 * {@link BpmnModelElementInstance#getTextContent()} seems to return all text
	 * content of all its descendants. This method returns the text content of its
	 * immediate text XML child instead. This method assumes that BPMN tags/nodes
	 * can have only 0 or 1 text content.
	 * 
	 * @param bpmnElement : the element to extract text content
	 * @return the text content of its immediate text XML child instead.
	 */
	protected Optional<String> getTextContent(ModelElementInstance bpmnElement) {

		logger.debug("Searching for text content of node {}", bpmnElement);

		if (bpmnElement == null) {
			return Optional.empty();
		}

		// extract the original DOM element so that we can obtain its raw children
		Optional<Element> optElement = DomElementWrapper.wrap(bpmnElement.getDomElement()).getOriginalElement();
		if (!optElement.isPresent()) {
			return Optional.empty();
		}

		// extract the immediate DOM/XML children
		NodeList immediateChildren = optElement.get().getChildNodes();

		// iterate on children and search for text content.
		int length = immediateChildren.getLength();
		for (int childIndex = 0; childIndex < length; childIndex++) {
			Node node = immediateChildren.item(childIndex);
			if (node.getNodeType() == Node.TEXT_NODE) {
				// this is a textual node
				String text = node.getTextContent();
				if (text != null && !text.trim().isEmpty()) {
					// we assume BPMN nodes can have 0 or 1 text content
					// so just return the 1st match
					logger.debug("Text content '{}' found in node '{}'.", text, bpmnElement);
					return Optional.of(text);
				}
			}
		}

		// no text node was found
		logger.debug("No text content found in node '{}'.", bpmnElement);
		return Optional.empty();
	}

	/**
	 * Extracts all "used" attributes in current BPMN tag. This can be different
	 * from {@link ModelElementType#getAttributes()} (at
	 * {@link BpmnModelElementInstance#getElementType()} ), which is the collection
	 * of attributes in the BPMN dictionary.
	 * 
	 * @param element         : the BPMN element.
	 * @param includeFromType : if true, those from
	 *                        {@link ModelElementType#getAttributes()} (at
	 *                        {@link BpmnModelElementInstance#getElementType()})
	 *                        will also be included.
	 * 
	 * @return a map whose key is the name of the attribute and value is its value.
	 */
	protected Map<String, String> getAllAttributes(ModelElementInstance element, boolean includeFromType) {

		Map<String, String> ret = new HashMap<>();

		// check if we should also include those unused attributes
		// inherited from BPMN element type
		if (includeFromType) {
			for (Attribute<?> attribute : element.getElementType().getAttributes()) {
				ret.put(attribute.getAttributeName(), null);
			}
		}

		// extract the DOM object
		// so that we can literally iterate on all used attributes
		Optional<Element> opt = DomElementWrapper.wrap(element.getDomElement()).getOriginalElement();
		if (opt.isPresent()) {
			Element dom = opt.get();

			// extract the attribute mapping
			NamedNodeMap nodeMap = dom.getAttributes();

			// iterate on the attributes to convert to Map<String,String>
			for (int index = 0; index < nodeMap.getLength(); index++) {
				Node node = nodeMap.item(index);
				String attribName = node.getNodeName();
				// check validity of attribute name
				if (isIgnoreInvalidAttributeName() && !attribName.matches("^[_a-zA-Z_]\\w*$")) {
					// invalid attribute name
					logger.warn("{} has an invalid pattern for attribute names. Ignoring/Skipping...", attribName);
					continue;
				}
				ret.put(attribName, node.getNodeValue());
			}
		}

		return ret;
	}

	/**
	 * Appends a numeric suffix to UIDs to keep UIDs unique.
	 * 
	 * @param base      : where to append the suffix
	 * @param namespace : prefix to be appended at the end
	 * @param usedUIDs  : UIDs that were used already.
	 * 
	 * @return new string with a numeric suffix appended. If namespace + base is not
	 *         in usedUID, then this method will simply return the base. Special
	 *         characters in base will be converted to underscore ('_').
	 */
	public String getNewUID(String namespace, String base, Collection<String> usedUIDs)
			throws IndexOutOfBoundsException {

		if (base == null) {
			base = "";
		}
		if (namespace == null) {
			namespace = "";
		}
		if (usedUIDs == null) {
			usedUIDs = new HashSet<>();
		}

		// Replace all special characters with '_'
		base = base.replaceAll("\\W+", "_");

		// UID is namespace + base
		// or namespace + base + [NUMBER]
		String uid = namespace + base;

		if (!usedUIDs.contains(uid)) {
			return uid;
		}

		// append a number at the end of string until we find something not in usedUIDs
		for (int numberSuffix = 1; numberSuffix < Integer.MAX_VALUE; numberSuffix++) {
			if (!usedUIDs.contains(uid + numberSuffix)) {
				return uid + numberSuffix;
			}
		}

		// if failed, try uid<n>_<m>
		logger.warn("Could not generate unique ID by appending integer suffixes. Retrying 'uid<n>_<m>'");
		for (int n = 1; n < Integer.MAX_VALUE; n++) {
			for (int m = 1; m < Integer.MAX_VALUE; m++) {
				if (!usedUIDs.contains(uid + n + "_" + m)) {
					return uid + n + "_" + m;
				}
			}
		}

		logger.warn("Could not generate unique ID. Exceeded {} x {} possibilities...", Integer.MAX_VALUE,
				Integer.MAX_VALUE);
		throw new IndexOutOfBoundsException("Coud not generate id by appending a numeric suffix to " + uid
				+ ". Maximum allowed number is " + Integer.MAX_VALUE);

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
	 * @return name of the artificial attribute that will store text XML child.
	 */
	public String getBPMNTextContentAttributeName() {
		return bpmnTextContentAttributeName;
	}

	/**
	 * @param attributeName : name of the artificial attribute that will store text
	 *                      XML child.
	 */
	public void setBPMNTextContentAttributeName(String attributeName) {
		this.bpmnTextContentAttributeName = attributeName;
	}

	/**
	 * @return the prefix to be used in all entities/relations generated by this
	 *         class.
	 */
	public String getBPMNEntityNamePrefix() {
		return bpmnEntityNamePrefix;
	}

	/**
	 * @param bpmnEntityNamePrefix : the prefix to be used in all entities/relations
	 *                             generated by this class.
	 */
	public void setBPMNEntityNamePrefix(String bpmnEntityNamePrefix) {
		this.bpmnEntityNamePrefix = bpmnEntityNamePrefix;
	}

	/**
	 * @return : the prefix to be used in all attributes generated by this class.
	 */
	public String getBPMNAttributeNamePrefix() {
		return bpmnAttributeNamePrefix;
	}

	/**
	 * @param bpmnAttributeNamePrefix : the prefix to be used in all attributes
	 *                                generated by this class.
	 */
	public void setBPMNAttributeNamePrefix(String bpmnAttributeNamePrefix) {
		this.bpmnAttributeNamePrefix = bpmnAttributeNamePrefix;
	}

	/**
	 * @return name of the relation that associates an entity in the conceptual
	 *         model to BPMN entity.
	 */
	public String getBPMNConceptualModelMappingName() {
		return bpmnConceptualModelMappingName;
	}

	/**
	 * @param bPMNConceptualModelMappingName : name of the relation that associates
	 *                                       an entity in the conceptual model to
	 *                                       BPMN entity.
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
	 * Expected format:
	 * 
	 * <pre>
	 * {
	 * 		'definitions':'Mission', 
	 * 		'@org.camunda.bpm.model.bpmn.instance.Task':'Task',
	 * 		'lane':'Performer',
	 * 		'participant':'Performer'  
	 * }
	 * </pre>
	 * 
	 * <p>
	 * The attribute name (left-hand side) should be either the name of the entity
	 * in BPMN or a java class (identified with '@'). The value (right hand side)
	 * should be the name of the entity in the conceptual model.
	 * </p>
	 * 
	 * <p>
	 * The '@' indicates that the program should search for sub-classes of the
	 * specified java class.
	 * </p>
	 * 
	 * @return JSON that specifies a mapping from sub-entities of
	 *         {@link #getBPMNConceptualModelMappingName()} to conceptual model
	 *         entities.
	 */
	public synchronized String getJSONBPMNConceptualModelMap() {
		if (jsonBPMNConceptualModelMap == null) {
			jsonBPMNConceptualModelMap = "";
		}
		return jsonBPMNConceptualModelMap;
	}

	/**
	 * 
	 * Expected format:
	 * 
	 * <pre>
	 * {
	 * 		'definitions':'Mission', 
	 * 		'@org.camunda.bpm.model.bpmn.instance.Task':'Task',
	 * 		'lane':'Performer',
	 * 		'participant':'Performer'  
	 * }
	 * </pre>
	 * 
	 * <p>
	 * The attribute name (left-hand side) should be either the name of the entity
	 * in BPMN or a java class (identified with '@'). The value (right hand side)
	 * should be the name of the entity in the conceptual model.
	 * </p>
	 * 
	 * <p>
	 * The '@' indicates that the program should search for sub-classes of the
	 * specified java class.
	 * </p>
	 * 
	 * @param json : JSON that specifies a mapping from sub-entities of
	 *             {@link #getBPMNConceptualModelMappingName()} to conceptual model
	 *             entities.
	 */
	public synchronized void setJSONBPMNConceptualModelMap(String json) {
		this.jsonBPMNConceptualModelMap = json;
	}

	/**
	 * @return if true, {@link #getAllAttributes(BpmnModelElementInstance, boolean)}
	 *         will ignore/skip attributes with invalid names.
	 */
	public boolean isIgnoreInvalidAttributeName() {
		return ignoreInvalidAttributeName;
	}

	/**
	 * @param ignoreInvalidAttributeName : if true,
	 *                                   {@link #getAllAttributes(BpmnModelElementInstance, boolean)}
	 *                                   will ignore/skip attributes with invalid
	 *                                   names.
	 */
	public void setIgnoreInvalidAttributeName(boolean ignoreInvalidAttributeName) {
		this.ignoreInvalidAttributeName = ignoreInvalidAttributeName;
	}

	/**
	 * @return if true, BPMN entities and entities in conceptual model will have
	 *         mappings.
	 */
	public boolean isMapBPMNToConceptualModel() {
		return mapBPMNToConceptualModel;
	}

	/**
	 * @param mapBPMNToConceptualModel : if true, BPMN entities and entities in
	 *                                 conceptual model will have mappings.
	 */
	public void setMapBPMNToConceptualModel(boolean mapBPMNToConceptualModel) {
		this.mapBPMNToConceptualModel = mapBPMNToConceptualModel;
	}

	/**
	 * @return the isCompoundByRelationName
	 */
	public String getIsCompoundByRelationName() {
		return isCompoundByRelationName;
	}

	/**
	 * @param isCompoundByRelationName the isCompoundByRelationName to set
	 */
	public void setIsCompoundByRelationName(String isCompoundByRelationName) {
		this.isCompoundByRelationName = isCompoundByRelationName;
	}

	/**
	 * @return the isPerformedByRelationName
	 */
	public String getIsPerformedByRelationName() {
		return isPerformedByRelationName;
	}

	/**
	 * @param isPerformedByRelationName the isPerformedByRelationName to set
	 */
	public void setIsPerformedByRelationName(String isPerformedByRelationName) {
		this.isPerformedByRelationName = isPerformedByRelationName;
	}

	/**
	 * @return the requiresRelationName
	 */
	public String getRequiresRelationName() {
		return requiresRelationName;
	}

	/**
	 * @param requiresRelationName the requiresRelationName to set
	 */
	public void setRequiresRelationName(String requiresRelationName) {
		this.requiresRelationName = requiresRelationName;
	}

}
