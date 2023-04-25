package edu.gmu.c4i.dalnim.bpmn2typedb.encoder;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
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
import org.json.JSONArray;
import org.json.JSONObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.w3c.dom.Element;
import org.w3c.dom.NamedNodeMap;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;

import com.vaticle.typeql.lang.TypeQL;
import com.vaticle.typeql.lang.common.exception.TypeQLException;
import com.vaticle.typeql.lang.pattern.Pattern;
import com.vaticle.typeql.lang.pattern.constraint.ThingConstraint.Has;
import com.vaticle.typeql.lang.pattern.constraint.ThingConstraint.Isa;
import com.vaticle.typeql.lang.pattern.constraint.ThingConstraint.Relation;
import com.vaticle.typeql.lang.pattern.constraint.TypeConstraint.Owns;
import com.vaticle.typeql.lang.pattern.constraint.TypeConstraint.Plays;
import com.vaticle.typeql.lang.pattern.constraint.TypeConstraint.Relates;
import com.vaticle.typeql.lang.pattern.schema.Rule;
import com.vaticle.typeql.lang.pattern.variable.BoundVariable;
import com.vaticle.typeql.lang.pattern.variable.ThingVariable;
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

	private String jsonBPMNConceptualModelMap = "{" + "'definitions':'Mission',"
			+ "'@org.camunda.bpm.model.bpmn.instance.Activity':'Task'," + "'lane':'Performer',"
			+ "'participant':'Performer'," + "'@org.camunda.bpm.model.bpmn.instance.ItemAwareElement':'Asset',"
			+ "'@org.camunda.bpm.model.bpmn.instance.DataAssociation':'Service',"
			+ "'parallelGateway':'ANDPrecedenceTaskList'," + "'exclusiveGateway':'ORPrecedenceTaskList',"
			+ "'complexGateway':'ORPrecedenceTaskList'," + "'inclusiveGateway':'ORPrecedenceTaskList',"
			+ "'sequenceFlow':'PrecedenceTask'," + "'collaboration':'Service'," + "'messageFlow':'Asset'" + "}";

	private String jsonConceptsNotToAddRole = "['Service']";

	private boolean ignoreInvalidAttributeName = true;

	private boolean mapBPMNToConceptualModel = true;

	private String isCompoundByRelationName = "isCompoundBy";

	private String isPerformedByRelationName = "isPerformedBy";

	private String providesRelationName = "provides";

	private String jsonSortableEntities = "['waypoint']";

	private String sortAttributeName = "sort";

	private String rootConceptualModelEntityName = "MIAEntity";

	private String uidAttributeName = "UID";

	private String jsonCommonBPMNSuperEntityMap = "{ " + "'@org.camunda.bpm.model.bpmn.instance.Activity' : 'Activity',"
			+ "'@org.camunda.bpm.model.bpmn.instance.Gateway' : 'Gateway'" + " }";

	private String bpmnGatewayTransitiveChainRelationName = bpmnEntityNamePrefix + "gatewayTransitiveChain";

	private String jsonNamesToIgnoreInSanityCheck = "['isCompoundBySetOfTask','isPrecededBySetOfTask','provides']";

	private String bpmnTransitiveAncestorRelationName = bpmnEntityNamePrefix + "hasChildTagTransitive";

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
						"## Note: conceptual model is required in DALNIM. Uncomment the following if not declared yet.");
				writer.println("# " + getUIDAttributeName() + " sub attribute, value string;");
				writer.println("# MIAEntity sub entity, owns " + getUIDAttributeName() + " @key;");
				writer.println("# Mission sub MIAEntity;");
				writer.println("# Task sub MIAEntity;");
				writer.println("# Performer sub MIAEntity;");
				writer.println("# Service sub Performer;");
				writer.println("# Asset sub MIAEntity;");
				writer.println("# PrecedenceTask sub MIAEntity;");
				writer.println("# ORPrecedenceTaskList sub PrecedenceTask;");
				writer.println("# ANDPrecedenceTaskList sub PrecedenceTask;");
				writer.println("# isCompoundBy sub relation, relates mission, relates task;");
				writer.println("# Mission plays isCompoundBy:mission;");
				writer.println("# Task plays isCompoundBy:task;");
				writer.println("# isPerformedBy sub relation, relates task, relates performer;");
				writer.println("# Task plays isPerformedBy:task;");
				writer.println("# Performer plays isPerformedBy:performer;");
				writer.println("# provides sub relation, relates asset, relates service;");
				writer.println("# Asset plays provides:asset;");
				writer.println("# Service plays provides:service;");
				writer.println("# isCompoundBySetOfTask sub relation, relates precedence_task, relates task;");
				writer.println("# PrecedenceTask plays isCompoundBySetOfTask:precedence_task;");
				writer.println("# Task plays isCompoundBySetOfTask:task;");
				writer.println("# isPrecededBySetOfTask sub relation, relates precedence_task, relates task;");
				writer.println("# PrecedenceTask plays isPrecededBySetOfTask:precedence_task;");
				writer.println("# Task plays isPrecededBySetOfTask:task;");
			} else {
				writer.println(getUIDAttributeName() + " sub attribute, value string;");
			}
			writer.println();

			writer.println("## BPMN entities in general");
			writer.println(getBPMNAttributeNamePrefix() + "id sub attribute, value string;");
			writer.println(getBPMNAttributeNamePrefix() + "name sub attribute, value string;");
			writer.println(getBPMNTextContentAttributeName() + " sub attribute, value string;");
			writer.println(getBPMNEntityName() + " sub entity, owns " + getBPMNAttributeNamePrefix() + "id, owns "
					+ getBPMNAttributeNamePrefix() + "name, owns " + getBPMNTextContentAttributeName() + ", owns "
					+ getUIDAttributeName() + " @key;");
			writer.println();

			// store the nodes which were already declared
			Set<String> visitedNodes = new HashSet<>();

			// extract the names of common super-entities
			Map<String, String> commonBPMNSuperEntityMap = parseJSONMap(getJSONCommonBPMNSuperEntityMap());
			if (commonBPMNSuperEntityMap == null) {
				// avoid nulls
				commonBPMNSuperEntityMap = new HashMap<>();
			}
			if (!commonBPMNSuperEntityMap.isEmpty()) {
				writer.println("## Common BPMN super-entities");
				// Common super entities are values in the above map.
				// Avoid duplicates
				for (String superEntityName : new HashSet<>(commonBPMNSuperEntityMap.values())) {
					// the entity name should have a common prefix
					String nameWithPrefix = getBPMNEntityNamePrefix() + superEntityName;
					writer.println(nameWithPrefix + " sub " + getBPMNEntityName() + ";");
					writer.println();
					// also indicate that the common super-entity was already visited.
					visitedNodes.add(nameWithPrefix);
				}
				writer.println();
			}

			writer.println("## Parent-child relationship of BPMN/XML tags");
			writer.println(getBPMNParentChildRelationName() + " sub relation, relates parent, relates child;");
			// A BPMN tag/entity can be a parent or child of another BPMN tag/entity
			writer.println(getBPMNEntityName() + " plays " + getBPMNParentChildRelationName() + ":child;");
			writer.println(getBPMNEntityName() + " plays " + getBPMNParentChildRelationName() + ":parent;");

			writer.println();

			// transitive chain of gateways
			// (useful when retrieving previous tasks regardless of gateways
			// when generating rules for PrecedenceTask)
			if (isMapBPMNToConceptualModel()) {
				writer.println("## relation about chain of gateways");
				writer.println(
						getBPMNGatewayTransitiveChainRelationName() + " sub relation, relates previous, relates next;");
				writer.println("BPMN_Gateway plays " + getBPMNGatewayTransitiveChainRelationName() + ":previous;");
				writer.println("BPMN_Gateway plays " + getBPMNGatewayTransitiveChainRelationName() + ":next;");

				writer.println();
			}

			// Some attributes are already declared in root "BPMN" entity,
			// so children do not have to re-declare
			Set<String> attributesInRootEntity = new HashSet<>();
			attributesInRootEntity.add(getUIDAttributeName());
			attributesInRootEntity.add(getBPMNAttributeNamePrefix() + "id");
			attributesInRootEntity.add(getBPMNAttributeNamePrefix() + "name");
			attributesInRootEntity.add(getBPMNTextContentAttributeName());

			logger.debug("Writing the body...");
			writer.println("## =============== Body ===============");
			writer.println();

			// store the attributes that were already declared
			Set<String> declaredAttributes = new HashSet<>(attributesInRootEntity);

			// store the relations that were already declared
			Set<String> declaredRelations = new HashSet<>();
			declaredRelations.add(getBPMNParentChildRelationName());
			declaredRelations.add(getBPMNGatewayTransitiveChainRelationName());

			// recursively visit what's below "definitions" tag
			visitBPMNSchemaRecursive(writer, bpmn.getDefinitions(), visitedNodes, attributesInRootEntity,
					declaredAttributes, declaredRelations, commonBPMNSuperEntityMap);

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
	 * Parses a JSON string to a map.
	 * 
	 * @param jsonText : text in JSON format.
	 * @return JSON object parsed to a map
	 */
	protected Map<String, String> parseJSONMap(String jsonText) {

		Map<String, String> ret = new HashMap<>();

		// parse the JSON
		JSONObject json = new JSONObject(jsonText);

		// keys are names of BPMN entities (or camunda classes),
		// values are entities in the concept model.
		for (String bpmnEntity : json.keySet()) {
			ret.put(bpmnEntity, json.getString(bpmnEntity));
		}

		return ret;

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
		if (isMapBPMNToConceptualModel() && !declaredRelations.contains(getBPMNConceptualModelMappingName())) {
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
	 * @param writer                   : where to write the script block.
	 * @param currentNode              : current BPMN tag to handle
	 * @param visitedNodes             : names of BPMN tags that were already
	 *                                 visited (attributes of these tags will be
	 *                                 skipped)
	 * @param inheritedAttributes      : these attributes will not be re-declared
	 *                                 (it's supposed to inherit from root "BPMN"
	 *                                 entity).
	 * @param declaredAttributes       : attributes that were already declared
	 *                                 previously.
	 * @param declaredRelations        : relations that were already declared
	 *                                 previously.
	 * @param commonBPMNSuperEntityMap : mapping of BPMN entities to their common
	 *                                 super-entities (the names will not come with
	 *                                 prefixes). If an entity is not found here,
	 *                                 then it will be added as a sub-entity of the
	 *                                 top BPMN entity
	 *                                 ({@link #getBPMNEntityName()}).
	 */
	protected void visitBPMNSchemaRecursive(PrintWriter writer, ModelElementInstance currentNode,
			Set<String> visitedNodes, Set<String> inheritedAttributes, Set<String> declaredAttributes,
			Set<String> declaredRelations, Map<String, String> commonBPMNSuperEntityMap) throws IOException {

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
		String originalEntityName = currentNode.getDomElement().getLocalName();
		String currentEntityName = getBPMNEntityNamePrefix() + originalEntityName;
		logger.debug("Entity: {}", currentEntityName);

		// skip declaration if this node was already visited
		if (!visitedNodes.contains(currentEntityName)) {

			// declare the current entity
			writer.println("## BPMN '" + currentEntityName + "' tag/node");
			String resolvedSuperEntityName = resolveName(commonBPMNSuperEntityMap, originalEntityName,
					currentNode.getClass());
			if (resolvedSuperEntityName != null) {
				writer.println(currentEntityName + " sub " + getBPMNEntityNamePrefix() + resolvedSuperEntityName + ";");
			} else {
				// use the top BPMN entity by default
				writer.println(currentEntityName + " sub " + getBPMNEntityName() + ";");
			}
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
					declaredRelations, commonBPMNSuperEntityMap);
		}
	}

	/**
	 * Resolves the keys in a name/class mapping and retrieve the associated value.
	 * 
	 * @param nameClassMapping   : a map from entity name or camunda class to entity
	 *                           name.
	 * @param entityNameNoPrefix : name to find in the key of the map.
	 * @param entityClass        : class to find in the key of the map.
	 * 
	 * @return the value respective to the key (entity name or entity class).
	 */
	protected String resolveName(Map<String, String> nameClassMapping, String entityNameNoPrefix,
			Class<? extends ModelElementInstance> entityClass) {

		String value = null;
		if (entityNameNoPrefix != null) {
			value = nameClassMapping.get(entityNameNoPrefix);
		}
		// just return the value if we found it.
		if (value != null) {
			// We found an exact match
			logger.debug("Found exact mapping: {} -> {}", entityNameNoPrefix, value);
			return value;
		}

		// We didn't find an exact match.
		// Keys may also start with '@' (i.e., '@class' key).
		// Such keys represent Java camunda classes.
		// Search for them if value was not found yet.
		if (entityClass != null) {
			// Find a compatible class...
			for (String key : nameClassMapping.keySet().stream()
					// get all keys that starts with "@"
					.filter(key -> key.startsWith("@")).collect(Collectors.toSet())) {
				// Obtain the class name, which is after '@'.
				String className = key.substring(1);
				// load the class and check if its compatible with current BPMN node.
				try {
					Class<?> clz = Class.forName(className);
					if (clz.isAssignableFrom(entityClass)) {
						// Current node is compatible (it's equal or a subclass of the specified class).
						value = nameClassMapping.get(key);
						logger.debug(
								"Found matching class {} for current BPMN entity {}. Only the 1st match will be used...",
								key, entityClass);
						// just use the 1st one we found
						break;
					}
				} catch (ClassNotFoundException e) {
					logger.warn("Invalid '@class' found in mapping from BPMN to conceptual model. Key = {}", key, e);
				}
			} // end of iteration on '@class' keys

		} // else cannot search for the class because it was not specified

		return value;
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
	 * $m isa Mission, has UID $muid; 
	 * $t isa Task, has UID $tuid; 
	 * (bpmnEntity: $bpmntask, conceptualModel: $t) isa BPMN_hasConceptualModelElement;
	 * $bpmntask isa BPMN_Entity, has UID $buid;
	 * get $m,$t,$r,$bpmntask,$muid,$tuid,$buid;
	 * 
	 * ## query isPerformedBy
	 * match
	 * $task isa Task, has UID $uid1;
	 * $performer isa Performer, has UID $uid2;
	 * $bpmntask isa BPMN_Entity, has UID $uid3;
	 * $bpmnlane isa BPMN_lane, has UID $uid4;
	 * $rel (task: $task, performer: $performer) isa isPerformedBy;
	 * (bpmnEntity: $bpmntask, conceptualModel: $task) isa BPMN_hasConceptualModelElement;
	 * (bpmnEntity: $bpmnlane, conceptualModel: $performer) isa BPMN_hasConceptualModelElement;
	 * get $rel, $uid1, $uid2, $uid3, $uid4, $bpmntask, $bpmnlane;
	 * 
	 * ## query requires
	 * match
	 * $dataObject isa BPMN_dataObject, has UID $uid1;
	 * $resource isa Resource, has UID $uid2;
	 * $bpmntask isa BPMN_Entity, has UID $uid3;
	 * $task isa Task, has UID $uid4;
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

		// declare the "sort" special attribute for sorting order-sensitive entities
		if (!inheritedAttributes.contains(getBPMNAttributeNamePrefix() + getSortAttributeName())) {
			if (!declaredAttributes.contains(getBPMNAttributeNamePrefix() + getSortAttributeName())) {
				// it's a number, but use a string type for compatibility with other attributes
				writer.println(getBPMNAttributeNamePrefix() + getSortAttributeName() + " sub attribute, value string;");
				// mark as declared
				declaredAttributes.add(getBPMNAttributeNamePrefix() + getSortAttributeName());
			}
			for (String sortableEntity : parseJSONSortableEntities()) {
				if (visitedNodes.contains(getBPMNEntityNamePrefix() + sortableEntity)) {
					writer.println(getBPMNEntityNamePrefix() + sortableEntity + " owns " + getBPMNAttributeNamePrefix()
							+ getSortAttributeName() + ";");
				}
			}
			writer.println();
		}

		// Define a new XML tag ancestor-descendant transitive relationship,
		// regardless of the mapping to conceptual model.
		// This would be useful to delete all BPMN_Entity below some BPMN_definitions
		writer.println(
				"## Transitive parent-child relationship of BPMN/XML tags (useful when deleting everything below "
						+ getBPMNEntityNamePrefix() + "definitions)");
		writer.println(
				getBPMNTransitiveAncestorRelationName() + " sub relation, relates ancestor, relates descendant;");
		writer.println(getBPMNEntityName() + " plays " + getBPMNTransitiveAncestorRelationName() + ":ancestor;");
		writer.println(getBPMNEntityName() + " plays " + getBPMNTransitiveAncestorRelationName() + ":descendant;");
		writer.println();

		// Rules that ensure the above ancestor-descendant relation is transitive

		// A parent tag should be an ancestor of its child
		writer.println("## Transitive parent-child rule, direct");
		writer.println("rule rule_BPMN_hasChildTagTransitive_direct:");
		writer.println("when {");
		writer.println(" $parent isa " + getBPMNEntityName() + ";");
		writer.println(" $child isa " + getBPMNEntityName() + ";");
		writer.println(" (parent: $parent, child: $child) isa " + getBPMNParentChildRelationName() + ";");
		writer.println("} then {");
		writer.println(" (ancestor: $parent, descendant: $child) isa " + getBPMNTransitiveAncestorRelationName() + ";");
		writer.println("};");
		writer.println();

		// a grandparent tag should be an ancestor of its grand children
		writer.println("## Transitive parent-child rule, transitive");
		writer.println("rule rule_BPMN_hasChildTagTransitive_transitive:");
		writer.println("when {");
		writer.println(" $grandparent isa " + getBPMNEntityName() + ";");
		writer.println(" $parent isa " + getBPMNEntityName() + ";");
		writer.println(" $child isa " + getBPMNEntityName() + ";");
		writer.println(
				" (ancestor: $grandparent, descendant: $parent) isa " + getBPMNTransitiveAncestorRelationName() + ";");
		writer.println(" (ancestor: $parent, descendant: $child) isa " + getBPMNTransitiveAncestorRelationName() + ";");
		writer.println("} then {");
		writer.println(
				" (ancestor: $grandparent, descendant: $child) isa " + getBPMNTransitiveAncestorRelationName() + ";");
		writer.println("};");
		writer.println();

		// We should be able to map an entity in the conceptual model to BPMN entity
		if (isMapBPMNToConceptualModel()) {
			String mappingRelationName = getBPMNConceptualModelMappingName();
			if (!declaredRelations.contains(mappingRelationName)) {
				writer.println("## =============== Mapping to conceptual model ===============");

				writer.println(mappingRelationName + " sub relation, relates bpmnEntity, relates conceptualModel;");

				// Specify the roles
				writer.println(getBPMNEntityName() + " plays " + mappingRelationName + ":bpmnEntity;");
				writer.println(
						getRootConceptualModelEntityName() + " plays " + mappingRelationName + ":conceptualModel;");

//				// obtain names of concepts not to include in roles.
//				Collection<String> conceptsNotToAddRole = parseJSONConceptsNotToAddRole();
//
//				// TypeDB does not allow 'entity' to play a role.
//				// Need to explicitly enumerate...
//				parseBPMNtoConceptualModelJSONMap()
//						// get all values (values are entities in conceptual model)
//						.values().stream()
//						// remove repetitions
//						.distinct()
//						// ignore nulls and blanks.
//						.filter(Objects::nonNull).filter(name -> !name.trim().isEmpty())
//						// do not re-declare roles if super-entity already declared it
//						.filter(name -> !conceptsNotToAddRole.contains(name))
//						// add entry: <entityName> plays BPMN_hasConceptualModelElement:conceptualModel
//						.forEach(entityName -> {
//							logger.debug("'{}' will play some role in {}", entityName, mappingRelationName);
//							writer.println(entityName + " plays " + mappingRelationName + ":conceptualModel;");
//						});

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

			// Rule to connect Mission-Task
			writer.println("## Mission isCompoundBy Task");
			writer.println("rule rule_misson_isCompoundBy_task:");
			writer.println("when {");
			writer.println("\t $bpmndefinitions isa " + getBPMNEntityNamePrefix() + "definitions;");
			writer.println("\t $bpmnprocess isa " + getBPMNEntityNamePrefix() + "process;");
			writer.println("\t $mission isa Mission;");
			writer.println("\t $task isa Task;");
			writer.println(
					"\t (parent: $bpmndefinitions, child: $bpmnprocess) isa " + getBPMNParentChildRelationName() + ";");
			writer.println("\t (parent: $bpmnprocess, child: $bpmntask) isa " + getBPMNParentChildRelationName() + ";");
			writer.println("\t (bpmnEntity: $bpmndefinitions, conceptualModel: $mission) isa "
					+ getBPMNConceptualModelMappingName() + ";");
			writer.println("\t (bpmnEntity: $bpmntask, conceptualModel: $task) isa "
					+ getBPMNConceptualModelMappingName() + ";");
			writer.println("} then {");
			writer.println("\t (mission: $mission, task: $task) isa " + getIsCompoundByRelationName() + ";");
			writer.println("};");
			writer.println();

			// Rule to connect Task-Performer
			if (visitedNodes.contains(getBPMNEntityNamePrefix() + "flowNodeRef")
					&& declaredAttributes.contains(getBPMNTextContentAttributeName())) {
				writer.println("## Task isPerformedBy Performer");
				writer.println("rule rule_task_isperformedBy_performer:");
				writer.println("when {");
				writer.println("\t $bpmnflowNodeRef isa " + getBPMNEntityNamePrefix() + "flowNodeRef, has "
						+ getBPMNTextContentAttributeName() + " $id-ref;");
				writer.println("\t $bpmntask isa " + getBPMNEntityName() + ", has " + getBPMNAttributeNamePrefix()
						+ "id $id;");
				writer.println("\t $id = $id-ref;");
				writer.println("\t $task isa Task;");
				writer.println("\t $performer isa Performer;");
				writer.println("\t (bpmnEntity: $bpmntask, conceptualModel: $task) isa "
						+ getBPMNConceptualModelMappingName() + ";");
				writer.println("\t (parent: $bpmnlane, child: $bpmnflowNodeRef) isa " + getBPMNParentChildRelationName()
						+ ";");
				writer.println("\t (bpmnEntity: $bpmnlane, conceptualModel: $performer) isa "
						+ getBPMNConceptualModelMappingName() + ";");
				writer.println("} then {");
				writer.println("\t (task: $task, performer: $performer) isa " + getIsPerformedByRelationName() + ";");
				writer.println("};");
				writer.println();
			}
			// Another rule to connect Task-Performer when Performer == Service
			// when there is input data
			if (visitedNodes.contains(getBPMNEntityNamePrefix() + "dataInputAssociation")) {
				writer.println("## Task isPerformedBy Service if Asset provides Service input");
				writer.println("rule rule_task_isPerformedBy_service_if_asset_provides_service_input:");
				writer.println("when {");
				writer.println("$bpmntask isa " + getBPMNEntityName() + ";");
				writer.println("\t $bpmntask isa " + getBPMNEntityName() + ";");
				writer.println("\t $dataInputAssociation isa " + getBPMNEntityNamePrefix() + "dataInputAssociation;");
				writer.println("\t $task isa Task; ");
				writer.println("\t $service isa Service;");
				writer.println("\t (parent: $bpmntask, child: $dataInputAssociation) isa "
						+ getBPMNParentChildRelationName() + ";");
				writer.println("\t (bpmnEntity: $bpmntask, conceptualModel: $task) isa "
						+ getBPMNConceptualModelMappingName() + ";");
				writer.println("\t (bpmnEntity: $dataInputAssociation, conceptualModel: $service) isa "
						+ getBPMNConceptualModelMappingName() + ";");
				writer.println("} then {");
				writer.println("\t (task: $task, performer: $service) isa " + getIsPerformedByRelationName() + ";");
				writer.println("};");
				writer.println();
			}
			// Another rule to connect Task-Performer when Performer == Service
			// when there is output data
			if (visitedNodes.contains(getBPMNEntityNamePrefix() + "dataOutputAssociation")) {
				writer.println("## Task isPerformedBy Service if Asset provides Service output");
				writer.println("rule rule_task_isPerformedBy_service_if_asset_provides_service_output:");
				writer.println("when {");
				writer.println("$bpmntask isa " + getBPMNEntityName() + ";");
				writer.println("\t $bpmntask isa " + getBPMNEntityName() + ";");
				writer.println("\t $dataOutputAssociation isa " + getBPMNEntityNamePrefix() + "dataOutputAssociation;");
				writer.println("\t $task isa Task; ");
				writer.println("\t $service isa Service;");
				writer.println("\t (parent: $bpmntask, child: $dataOutputAssociation) isa "
						+ getBPMNParentChildRelationName() + ";");
				writer.println("\t (bpmnEntity: $bpmntask, conceptualModel: $task) isa "
						+ getBPMNConceptualModelMappingName() + ";");
				writer.println("\t (bpmnEntity: $dataOutputAssociation, conceptualModel: $service) isa "
						+ getBPMNConceptualModelMappingName() + ";");
				writer.println("} then {");
				writer.println("\t (task: $task, performer: $service) isa " + getIsPerformedByRelationName() + ";");
				writer.println("};");
				writer.println();
			}
			// Another rule to connect Task-Performer when Performer == Service
			// when there are messageFlows in collaboration
			if (visitedNodes.contains(getBPMNEntityNamePrefix() + "messageFlow")
					&& visitedNodes.contains(getBPMNEntityNamePrefix() + "Activity")
					&& declaredAttributes.contains(getBPMNAttributeNamePrefix() + "id")) {
				// Task can be source or target of message flow,
				// but rules should not contain disjunction,
				// so simply write 2 rules.

				// Prepare the common suffix:
				StringWriter commonSuffix = new StringWriter();
				try (PrintWriter suffixWriter = new PrintWriter(commonSuffix);) {
					suffixWriter.println("\t $activity isa " + getBPMNEntityNamePrefix() + "Activity, has "
							+ getBPMNAttributeNamePrefix() + "id $id;");
					suffixWriter.println("\t $task isa Task;");
					suffixWriter.println("\t $asset isa Asset;");
					suffixWriter.println("\t $service isa Service;");
					suffixWriter.println("\t $ref = $id;");
					suffixWriter.println("\t (bpmnEntity: $message, conceptualModel: $asset) isa "
							+ getBPMNConceptualModelMappingName() + ";");
					suffixWriter.println("\t (bpmnEntity: $activity, conceptualModel: $task) isa "
							+ getBPMNConceptualModelMappingName() + ";");
					suffixWriter
							.println("\t (asset: $asset, service: $service) isa " + getProvidesRelationName() + ";");
					suffixWriter.println("} then {");
					suffixWriter.println(
							"\t (task: $task, performer: $service) isa " + getIsPerformedByRelationName() + ";");
					suffixWriter.println("};");
				}

				// If task is source of message flow
				if (declaredAttributes.contains(getBPMNAttributeNamePrefix() + "sourceRef")) {
					// write the specific prefix
					writer.println(
							"## If BPMN has messageFlow *from* some Activity: Asset->provides->Service<-isPerformedBy<-Task ");
					writer.println(
							"rule rule_asset_provides_service_and_task_isPerformedBy_service_messageFlow_source:");
					writer.println("when {\n\t $message isa " + getBPMNEntityNamePrefix() + "messageFlow, has "
							+ getBPMNAttributeNamePrefix() + "sourceRef $ref;");
					// write the common suffix
					writer.println(commonSuffix.toString());
				}

				// If task is target of message flow
				if (declaredAttributes.contains(getBPMNAttributeNamePrefix() + "targetRef")) {
					// write the specific prefix
					writer.println(
							"## If BPMN has messageFlow *to* some Activity: Asset->provides->Service<-isPerformedBy<-Task ");
					writer.println(
							"rule rule_asset_provides_service_and_task_isPerformedBy_service_messageFlow_target:");
					writer.println("when {\n\t $message isa " + getBPMNEntityNamePrefix() + "messageFlow, has "
							+ getBPMNAttributeNamePrefix() + "targetRef $ref;");
					// write the common suffix
					writer.println(commonSuffix.toString());
				}
			}

			// Rule to connect Asset-Service via data input association
			if (visitedNodes.contains(getBPMNEntityNamePrefix() + "dataInputAssociation")
					&& visitedNodes.contains(getBPMNEntityNamePrefix() + "dataObject")
					&& declaredAttributes.contains(getBPMNTextContentAttributeName())
					&& declaredAttributes.contains(getBPMNAttributeNamePrefix() + "id")
					&& visitedNodes.contains(getBPMNEntityNamePrefix() + "sourceRef")) {
				writer.println("## Asset provides Service (from input data)");
				writer.println("rule rule_source_asset_provides_service:");
				writer.println("when {");
				writer.println("\t $dataInputAssociation isa " + getBPMNEntityNamePrefix() + "dataInputAssociation;");
				writer.println("\t $ref isa " + getBPMNEntityNamePrefix() + "sourceRef, has "
						+ getBPMNTextContentAttributeName() + " $ref_id;");
				writer.println("\t $dataObject isa " + getBPMNEntityNamePrefix() + "dataObject, has "
						+ getBPMNAttributeNamePrefix() + "id $data_id;");
				writer.println("\t $bpmntask isa " + getBPMNEntityName() + ";");
				writer.println("\t $service isa Service;");
				writer.println("\t $asset isa Asset; ");
				writer.println("\t $data_id = $ref_id;");
				writer.println("\t (parent: $bpmntask, child: $dataInputAssociation) isa "
						+ getBPMNParentChildRelationName() + ";");
				writer.println("\t (parent: $dataInputAssociation, child: $ref) isa " + getBPMNParentChildRelationName()
						+ ";");
				writer.println("\t (bpmnEntity: $dataObject, conceptualModel: $asset) isa "
						+ getBPMNConceptualModelMappingName() + ";");
				writer.println("\t (bpmnEntity: $dataInputAssociation, conceptualModel: $service) isa "
						+ getBPMNConceptualModelMappingName() + ";");
				writer.println("} then {");
				writer.println("\t (asset: $asset, service: $service) isa " + getProvidesRelationName() + ";");
				writer.println("};");
				writer.println();

				// also support data object reference
				if (visitedNodes.contains(getBPMNEntityNamePrefix() + "dataObjectReference")) {
					writer.println("## Asset provides Service (from reference to input data)");
					writer.println("rule rule_source_asset_reference_provides_service:");
					writer.println("when {");
					writer.println(
							"\t $dataInputAssociation isa " + getBPMNEntityNamePrefix() + "dataInputAssociation;");
					writer.println("\t $ref isa " + getBPMNEntityNamePrefix() + "sourceRef, has "
							+ getBPMNTextContentAttributeName() + " $association_ref;");
					writer.println("\t $dataObject isa " + getBPMNEntityNamePrefix() + "dataObject, has "
							+ getBPMNAttributeNamePrefix() + "id $data_id;");
					writer.println("\t $dataObjectReference isa " + getBPMNEntityNamePrefix()
							+ "dataObjectReference, has " + getBPMNAttributeNamePrefix()
							+ "dataObjectRef $data_ref, has " + getBPMNAttributeNamePrefix() + "id $ref_id;");
					writer.println("\t $bpmntask isa " + getBPMNEntityName() + ";");
					writer.println("\t $service isa Service;");
					writer.println("\t $asset isa Asset; ");
					writer.println("\t $ref_id = $association_ref;");
					writer.println("\t $data_id = $data_ref;");
					writer.println("\t (parent: $bpmntask, child: $dataInputAssociation) isa "
							+ getBPMNParentChildRelationName() + ";");
					writer.println("\t (parent: $dataInputAssociation, child: $ref) isa "
							+ getBPMNParentChildRelationName() + ";");
					writer.println("\t (bpmnEntity: $dataObject, conceptualModel: $asset) isa "
							+ getBPMNConceptualModelMappingName() + ";");
					writer.println("\t (bpmnEntity: $dataInputAssociation, conceptualModel: $service) isa "
							+ getBPMNConceptualModelMappingName() + ";");
					writer.println("} then {");
					writer.println("\t (asset: $asset, service: $service) isa " + getProvidesRelationName() + ";");
					writer.println("};");
					writer.println();

				} // end of support for data object reference

			} // end of input rule to connect Asset-Service

			// Another rule to connect Asset-Service via data output association
			if (visitedNodes.contains(getBPMNEntityNamePrefix() + "dataOutputAssociation")
					&& visitedNodes.contains(getBPMNEntityNamePrefix() + "dataObject")
					&& declaredAttributes.contains(getBPMNTextContentAttributeName())
					&& declaredAttributes.contains(getBPMNAttributeNamePrefix() + "id")
					&& visitedNodes.contains(getBPMNEntityNamePrefix() + "targetRef")) {
				writer.println("## Asset provides Service (from output data)");
				writer.println("rule rule_target_asset_reference_provides_service:");
				writer.println("when {");
				writer.println("\t $dataOutputAssociation isa " + getBPMNEntityNamePrefix() + "dataOutputAssociation;");
				writer.println("\t $ref isa " + getBPMNEntityNamePrefix() + "targetRef, has "
						+ getBPMNTextContentAttributeName() + " $ref_id;");
				writer.println("\t $dataObject isa " + getBPMNEntityNamePrefix() + "dataObject, has "
						+ getBPMNAttributeNamePrefix() + "id $data_id;");
				writer.println("\t $bpmntask isa " + getBPMNEntityName() + ";");
				writer.println("\t $service isa Service;");
				writer.println("\t $asset isa Asset; ");
				writer.println("\t $data_id = $ref_id;");
				writer.println("\t (parent: $bpmntask, child: $dataOutputAssociation) isa "
						+ getBPMNParentChildRelationName() + ";");
				writer.println("\t (parent: $dataOutputAssociation, child: $ref) isa "
						+ getBPMNParentChildRelationName() + ";");
				writer.println("\t (bpmnEntity: $dataObject, conceptualModel: $asset) isa "
						+ getBPMNConceptualModelMappingName() + ";");
				writer.println("\t (bpmnEntity: $dataOutputAssociation, conceptualModel: $service) isa "
						+ getBPMNConceptualModelMappingName() + ";");
				writer.println("} then {");
				writer.println("\t (asset: $asset, service: $service) isa " + getProvidesRelationName() + ";");
				writer.println("};");
				writer.println();

				// support data object reference
				if (visitedNodes.contains(getBPMNEntityNamePrefix() + "dataObjectReference")) {
					writer.println("## Asset provides Service (from reference to output data)");
					writer.println("rule rule_target_asset_provides_service:");
					writer.println("when {");
					writer.println(
							"\t $dataOutputAssociation isa " + getBPMNEntityNamePrefix() + "dataOutputAssociation;");
					writer.println("\t $ref isa " + getBPMNEntityNamePrefix() + "targetRef, has "
							+ getBPMNTextContentAttributeName() + " $association_ref;");
					writer.println("\t $dataObject isa " + getBPMNEntityNamePrefix() + "dataObject, has "
							+ getBPMNAttributeNamePrefix() + "id $data_id;");
					writer.println("\t $dataObjectReference isa " + getBPMNEntityNamePrefix()
							+ "dataObjectReference, has " + getBPMNAttributeNamePrefix()
							+ "dataObjectRef $data_ref, has " + getBPMNAttributeNamePrefix() + "id $ref_id;");
					writer.println("\t $bpmntask isa " + getBPMNEntityName() + ";");
					writer.println("\t $service isa Service;");
					writer.println("\t $asset isa Asset; ");
					writer.println("\t $ref_id = $association_ref;");
					writer.println("\t $data_id = $data_ref;");
					writer.println("\t (parent: $bpmntask, child: $dataOutputAssociation) isa "
							+ getBPMNParentChildRelationName() + ";");
					writer.println("\t (parent: $dataOutputAssociation, child: $ref) isa "
							+ getBPMNParentChildRelationName() + ";");
					writer.println("\t (bpmnEntity: $dataObject, conceptualModel: $asset) isa "
							+ getBPMNConceptualModelMappingName() + ";");
					writer.println("\t (bpmnEntity: $dataOutputAssociation, conceptualModel: $service) isa "
							+ getBPMNConceptualModelMappingName() + ";");
					writer.println("} then {");
					writer.println("\t (asset: $asset, service: $service) isa " + getProvidesRelationName() + ";");
					writer.println("};");
					writer.println();

				} // end of data object reference

			} // end of output rule to connect Asset-Service

			// Another rule to connect Asset-Service when there are messageFlows in
			// collaboration
			if (visitedNodes.contains(getBPMNEntityNamePrefix() + "messageFlow")
					&& visitedNodes.contains(getBPMNEntityNamePrefix() + "collaboration")) {
				writer.println("## If BPMN has messageFlow, Asset->provides->Service via collaboration");
				writer.println("rule rule_asset_provides_service_messageFlow:");
				writer.println("when {");
				writer.println("\t $message isa " + getBPMNEntityNamePrefix() + "messageFlow;");
				writer.println("\t $collab isa " + getBPMNEntityNamePrefix() + "collaboration;");
				writer.println("\t $asset isa Asset;");
				writer.println("\t $service isa Service;");
				writer.println("\t (parent: $collab, child: $message) isa " + getBPMNParentChildRelationName() + ";");
				writer.println("\t (bpmnEntity: $message, conceptualModel: $asset) isa "
						+ getBPMNConceptualModelMappingName() + ";");
				writer.println("\t (bpmnEntity: $collab, conceptualModel: $service) isa "
						+ getBPMNConceptualModelMappingName() + ";");
				writer.println("} then {");
				writer.println("\t  (asset: $asset, service: $service) isa " + getProvidesRelationName() + ";");
				writer.println("};");
				writer.println();
			}

			// Rules of PrecedenceTask related to sequenceFlow
			if (visitedNodes.contains(getBPMNEntityNamePrefix() + "sequenceFlow")
					&& declaredAttributes.contains(getBPMNAttributeNamePrefix() + "sourceRef")
					&& declaredAttributes.contains(getBPMNAttributeNamePrefix() + "targetRef")
					&& declaredAttributes.contains(getBPMNAttributeNamePrefix() + "id")) {

				// We have 2 rules: one for isPrecededBySetOfTask, another for
				// isCompoundBySetOfTask
				// The two rules are only different in the "then" block,
				// so save the "when" block as common portion.
				StringBuilder commonPart = new StringBuilder();

				// the 1st rule is about isPrecededBySetOfTask
				writer.println("## Task isPrecededBySetOfTask precedence tasks (sequence flow)");
				writer.println("rule rule_task_isPrecededBySetOfTask_precedenceTask_sequenceFlow:");
				// the common "when" part
				commonPart.append("when {\n");
				commonPart.append("\t $precedenceTask isa PrecedenceTask;\n");
				commonPart.append("\t $task1 isa Task;\n");
				commonPart.append("\t $task2 isa Task;\n");
				commonPart.append("\t $sequenceFlow isa " + getBPMNEntityNamePrefix() + "sequenceFlow, has "
						+ getBPMNAttributeNamePrefix() + "sourceRef $sourceRef, has " + getBPMNAttributeNamePrefix()
						+ "targetRef $targetRef;\n");
				commonPart.append("\t $bpmntask1 isa " + getBPMNEntityName() + ", has " + getBPMNAttributeNamePrefix()
						+ "id $taskID1;\n");
				commonPart.append("\t $bpmntask2 isa " + getBPMNEntityName() + ", has " + getBPMNAttributeNamePrefix()
						+ "id $taskID2;\n");
				commonPart.append("\t $taskID1 = $sourceRef;\n");
				commonPart.append("\t $taskID2 = $targetRef;\n");
				commonPart.append("\t (bpmnEntity: $sequenceFlow, conceptualModel: $precedenceTask) isa "
						+ getBPMNConceptualModelMappingName() + ";\n");
				commonPart.append("\t (bpmnEntity: $bpmntask1, conceptualModel: $task1) isa "
						+ getBPMNConceptualModelMappingName() + ";\n");
				commonPart.append("\t (bpmnEntity: $bpmntask2, conceptualModel: $task2) isa "
						+ getBPMNConceptualModelMappingName() + ";\n");
				commonPart.append("} then {");
				writer.println(commonPart.toString());
				// content of "then" is different
				writer.println("\t (precedence_task: $precedenceTask, task: $task2) isa isPrecededBySetOfTask;");
				writer.println("};");
				writer.println();

				// the 2nd rule is about isCompoundBySetOfTask
				writer.println("## Precedence task isCompoundBySetOfTask tasks (sequence flow)");
				writer.println("rule rule_precedenceTask_isCompoundBySetOfTask_task_sequenceFlow:");
				// the common "when" part
				writer.println(commonPart.toString());
				// content of "then" is different
				writer.println("\t (precedence_task: $precedenceTask, task: $task1) isa isCompoundBySetOfTask;");
				writer.println("};");
				writer.println();

			} // end of rules of PrecedenceTask related to sequenceFlow

			// rules for transitive closure of gateway precedence
			if (declaredRelations.contains(getBPMNGatewayTransitiveChainRelationName())
					&& visitedNodes.contains(getBPMNEntityNamePrefix() + "sequenceFlow")
					&& visitedNodes.contains(getBPMNEntityNamePrefix() + "Gateway")
					&& declaredAttributes.contains(getBPMNAttributeNamePrefix() + "sourceRef")
					&& declaredAttributes.contains(getBPMNAttributeNamePrefix() + "targetRef")
					&& declaredAttributes.contains(getBPMNAttributeNamePrefix() + "id")) {

				// direct connection
				writer.println("## chain of gateways, direct");
				writer.println("rule rule_gateway_chain_direct:");
				writer.println("when {");
				writer.println("\t $sequenceFlow isa " + getBPMNEntityNamePrefix() + "sequenceFlow, has "
						+ getBPMNAttributeNamePrefix() + "sourceRef $source, has " + getBPMNAttributeNamePrefix()
						+ "targetRef $target;");
				writer.println("\t $gateway1 isa " + getBPMNEntityNamePrefix() + "Gateway, has "
						+ getBPMNAttributeNamePrefix() + "id $id1;");
				writer.println("\t $gateway2 isa " + getBPMNEntityNamePrefix() + "Gateway, has "
						+ getBPMNAttributeNamePrefix() + "id $id2;");
				writer.println("\t $id1 = $source;");
				writer.println("\t $id2 = $target;");
				writer.println("} then {");
				writer.println("\t (previous: $gateway1, next: $gateway2) isa "
						+ getBPMNGatewayTransitiveChainRelationName() + ";");
				writer.println("};");

				// transitive connection
				writer.println("## chain of gateways, transitive");
				writer.println("rule rule_gateway_chain_transitive:");
				writer.println("when {");
				writer.println("\t $sequenceFlow isa " + getBPMNEntityNamePrefix() + "sequenceFlow, has "
						+ getBPMNAttributeNamePrefix() + "sourceRef $source, has " + getBPMNAttributeNamePrefix()
						+ "targetRef $target;");
				writer.println("\t $gateway1 isa " + getBPMNEntityNamePrefix() + "Gateway, has "
						+ getBPMNAttributeNamePrefix() + "id $id1;");
				writer.println("\t $gateway2 isa " + getBPMNEntityNamePrefix() + "Gateway, has "
						+ getBPMNAttributeNamePrefix() + "id $id2;");
				writer.println("\t $gateway3 isa " + getBPMNEntityNamePrefix() + "Gateway;");
				writer.println("\t $id1 = $source;");
				writer.println("\t $id2 = $target;");
				writer.println("\t (previous: $gateway2, next: $gateway3) isa "
						+ getBPMNGatewayTransitiveChainRelationName() + ";");
				writer.println("} then {");
				writer.println("\t (previous: $gateway1, next: $gateway3) isa "
						+ getBPMNGatewayTransitiveChainRelationName() + ";");
				writer.println("};");

				writer.println();
			}

			// Task isPrecededBySetOfTask AND/ORPrecedenceTaskList,
			// AND/ORPrecedenceTaskList isCompoundBySetOfTask Task:
			if (visitedNodes.contains(getBPMNEntityNamePrefix() + "Activity")
					&& visitedNodes.contains(getBPMNEntityNamePrefix() + "Gateway")
					&& visitedNodes.contains(getBPMNEntityNamePrefix() + "sequenceFlow")
					&& declaredAttributes.contains(getBPMNAttributeNamePrefix() + "sourceRef")
					&& declaredAttributes.contains(getBPMNAttributeNamePrefix() + "targetRef")
					&& declaredAttributes.contains(getBPMNAttributeNamePrefix() + "id")) {

				// Task isPrecededBySetOfTask ANDPrecedenceTaskList, direct connection.
				// Task isPrecededBySetOfTask ORPrecedenceTaskList, direct connection.
				// These rules have a common prefix and suffix.

				// Prepare the common prefix, direct connection.
				StringWriter commonPrefixWhen = new StringWriter();
				try (PrintWriter prefixWriter = new PrintWriter(commonPrefixWhen);) {
					prefixWriter.println("when {");
					prefixWriter.println(" $bpmngate isa " + getBPMNEntityNamePrefix() + "Gateway, has "
							+ getBPMNAttributeNamePrefix() + "id $gateId;");
					prefixWriter.println(" $bpmntaskFrom isa " + getBPMNEntityNamePrefix() + "Activity, has "
							+ getBPMNAttributeNamePrefix() + "id $taskFromId;");
					prefixWriter.println(" $flowFrom isa " + getBPMNEntityNamePrefix() + "sequenceFlow, has "
							+ getBPMNAttributeNamePrefix() + "sourceRef $fromSource, has "
							+ getBPMNAttributeNamePrefix() + "targetRef $fromTarget;");
					prefixWriter.println(" $fromTarget = $gateId;");
					prefixWriter.println(" $fromSource = $taskFromId;");
					prefixWriter.println(" $bpmntaskTo isa " + getBPMNEntityNamePrefix() + "Activity, has "
							+ getBPMNAttributeNamePrefix() + "id $taskToId;");
					prefixWriter.println(" $flowTo isa " + getBPMNEntityNamePrefix() + "sequenceFlow, has "
							+ getBPMNAttributeNamePrefix() + "sourceRef $toSource, has " + getBPMNAttributeNamePrefix()
							+ "targetRef $toTarget;");
					prefixWriter.println(" $toTarget = $taskToId;");
					prefixWriter.println(" $toSource = $gateId;");
					prefixWriter.println(" $taskTo isa Task;");
					prefixWriter.println(" (bpmnEntity: $bpmntaskTo, conceptualModel: $taskTo) isa "
							+ getBPMNConceptualModelMappingName() + ";");
					prefixWriter.println(" (bpmnEntity: $bpmngate, conceptualModel: $prec) isa "
							+ getBPMNConceptualModelMappingName() + ";");
				} // end of common prefix, direct connection.

				// Prepare the common suffix.
				// This common suffix can be reused for the transitive rule.
				StringWriter commonSuffixThen = new StringWriter();
				try (PrintWriter suffixWriter = new PrintWriter(commonSuffixThen);) {
					suffixWriter.println("} then {");
					suffixWriter.println("     (task: $taskTo, precedence_task: $prec) isa isPrecededBySetOfTask;");
					suffixWriter.println("};");
				}

				// Task isPrecededBySetOfTask ORPrecedenceTaskList, direct
				writer.println("## Task isPrecededBySetOfTask ORPrecedenceTaskList, direct");
				writer.println("rule rule_task_isPrecededBySetOfTask_ORPrecedenceTaskList_direct:");
				// append the common prefix
				writer.print(commonPrefixWhen.toString());
				// force ORPrecedenceTask
				writer.println(" $prec isa ORPrecedenceTaskList;");
				// append the common suffix
				writer.print(commonSuffixThen.toString());
				writer.println();

				// Task isPrecededBySetOfTask ANDPrecedenceTaskList, direct
				writer.println("## Task isPrecededBySetOfTask ANDPrecedenceTaskList, direct");
				writer.println("rule rule_task_isPrecededBySetOfTask_ANDPrecedenceTaskList_direct:");
				// append the common prefix
				writer.print(commonPrefixWhen.toString());
				// force ANDPrecedenceTask
				writer.println(" $prec isa ANDPrecedenceTaskList;");
				// append the common suffix
				writer.print(commonSuffixThen.toString());
				writer.println();

				// Task isPrecededBySetOfTask ORPrecedenceTaskList,
				// indirect (transitive) connection
				if (declaredRelations.contains(getBPMNGatewayTransitiveChainRelationName())) {

					// prepare the common prefix
					commonPrefixWhen = new StringWriter();
					try (PrintWriter prefixWriter = new PrintWriter(commonPrefixWhen);) {
						prefixWriter.println("when {");
						prefixWriter.println(" $bpmngateFrom isa " + getBPMNEntityNamePrefix() + "Gateway, has "
								+ getBPMNAttributeNamePrefix() + "id $gateFromId;");
						prefixWriter.println(" $bpmngateTo isa " + getBPMNEntityNamePrefix() + "Gateway, has "
								+ getBPMNAttributeNamePrefix() + "id $gateToId;");
						prefixWriter.println(" (previous: $bpmngateFrom, next: $bpmngateTo) isa "
								+ getBPMNGatewayTransitiveChainRelationName() + ";");
						prefixWriter.println(" $bpmntaskFrom isa " + getBPMNEntityNamePrefix() + "Activity, has "
								+ getBPMNAttributeNamePrefix() + "id $taskFromId;");
						prefixWriter.println(" $flowFrom isa " + getBPMNEntityNamePrefix() + "sequenceFlow, has "
								+ getBPMNAttributeNamePrefix() + "sourceRef $fromSource, has "
								+ getBPMNAttributeNamePrefix() + "targetRef $fromTarget;");
						prefixWriter.println(" $fromTarget = $gateFromId;");
						prefixWriter.println(" $fromSource = $taskFromId;");
						prefixWriter.println(" $bpmntaskTo isa " + getBPMNEntityNamePrefix() + "Activity, has "
								+ getBPMNAttributeNamePrefix() + "id $taskToId;");
						prefixWriter.println(" $flowTo isa " + getBPMNEntityNamePrefix() + "sequenceFlow, has "
								+ getBPMNAttributeNamePrefix() + "sourceRef $toSource, has "
								+ getBPMNAttributeNamePrefix() + "targetRef $toTarget;");
						prefixWriter.println(" $toTarget = $taskToId;");
						prefixWriter.println(" $toSource = $gateToId;");
						prefixWriter.println(" $taskTo isa Task;");
						prefixWriter.println(" (bpmnEntity: $bpmntaskTo, conceptualModel: $taskTo) isa "
								+ getBPMNConceptualModelMappingName() + ";");
						prefixWriter.println(" (bpmnEntity: $bpmngateTo, conceptualModel: $prec) isa "
								+ getBPMNConceptualModelMappingName() + ";");
					}

					// Task isPrecededBySetOfTask ORPrecedenceTaskList, transitive
					writer.println("## Task isPrecededBySetOfTask ORPrecedenceTaskList, transitive");
					writer.println("rule rule_task_isPrecededBySetOfTask_ORPrecedenceTaskList_transitive:");
					// write the common prefix
					writer.print(commonPrefixWhen.toString());
					// force ORPrecedenceTaskList
					writer.println(" $prec isa ORPrecedenceTaskList;");
					// reuse the same common suffix
					writer.print(commonSuffixThen.toString());
					writer.println();

					// Task isPrecededBySetOfTask ANDPrecedenceTaskList, transitive
					writer.println("## Task isPrecededBySetOfTask ANDPrecedenceTaskList, transitive");
					writer.println("rule rule_task_isPrecededBySetOfTask_ANDPrecedenceTaskList_transitive:");
					writer.print(commonPrefixWhen.toString());
					// force ANDPrecedenceTaskList
					writer.println(" $prec isa ANDPrecedenceTaskList;");
					// reuse the same common suffix
					writer.print(commonSuffixThen.toString());
					writer.println();

				} // end of Task isPrecededBySetOfTask ORPrecedenceTaskList, transitive

				// End Task isPrecededBySetOfTask AND/ORPrecedenceTaskList,

				// Begin AND/ORPrecedenceTaskList isCompoundBySetOfTask Task

				// AND/ORPrecedenceTaskList isCompoundBySetOfTask Task, direct
				writer.println("## AND/ORPrecedenceTaskList isCompoundBySetOfTask Task, direct");
				writer.println("rule rule_ANDORPrecedenceTaskList_isCompoundBySetOfTask_task_direct:");
				writer.println("when {");
				writer.println(" $prec isa PrecedenceTask;");
				writer.println(" $taskTo isa Task;");
				writer.println(" $taskFrom isa Task;");
				writer.println(" (task: $taskTo, precedence_task: $prec) isa isPrecededBySetOfTask;");
				writer.println(" (bpmnEntity: $bpmngate, conceptualModel: $prec) isa "
						+ getBPMNConceptualModelMappingName() + ";");
				writer.println(" $bpmngate isa " + getBPMNEntityNamePrefix() + "Gateway, has "
						+ getBPMNAttributeNamePrefix() + "id $gateId;");
				writer.println(" $bpmntaskFrom isa " + getBPMNEntityNamePrefix() + "Activity, has "
						+ getBPMNAttributeNamePrefix() + "id $taskFromId;");
				writer.println(" $flowFrom isa " + getBPMNEntityNamePrefix() + "sequenceFlow, has "
						+ getBPMNAttributeNamePrefix() + "sourceRef $fromSource, has " + getBPMNAttributeNamePrefix()
						+ "targetRef $fromTarget;");
				writer.println(" $fromTarget = $gateId;");
				writer.println(" $fromSource = $taskFromId;");
				writer.println(" (bpmnEntity: $bpmntaskFrom, conceptualModel: $taskFrom) isa "
						+ getBPMNConceptualModelMappingName() + ";");
				writer.println("} then {");
				writer.println("     (task: $taskFrom, precedence_task: $prec) isa isCompoundBySetOfTask;");
				writer.println("};");
				writer.println();

				// AND/ORPrecedenceTaskList isCompoundBySetOfTask Task, Transitive
				if (declaredRelations.contains(getBPMNGatewayTransitiveChainRelationName())) {
					writer.println("## AND/ORPrecedenceTaskList isCompoundBySetOfTask Task, transitive");
					writer.println("rule rule_ANDORPrecedenceTaskList_isCompoundBySetOfTask_task_transitive:");
					writer.println("when {");
					writer.println(" $prec isa PrecedenceTask;");
					writer.println(" $taskTo isa Task;");
					writer.println(" $taskFrom isa Task;");
					writer.println(" (task: $taskTo, precedence_task: $prec) isa isPrecededBySetOfTask;");
					writer.println(" (bpmnEntity: $bpmngateTo, conceptualModel: $prec) isa "
							+ getBPMNConceptualModelMappingName() + ";");
					writer.println(" $bpmngateTo isa " + getBPMNEntityNamePrefix() + "Gateway;");
					writer.println(" (previous: $bpmngateFrom, next: $bpmngateTo) isa "
							+ getBPMNGatewayTransitiveChainRelationName() + ";");
					writer.println(" $bpmngateFrom isa " + getBPMNEntityNamePrefix() + "Gateway, has "
							+ getBPMNAttributeNamePrefix() + "id $gateId;");
					writer.println(" $bpmntaskFrom isa " + getBPMNEntityNamePrefix() + "Activity, has "
							+ getBPMNAttributeNamePrefix() + "id $taskFromId;");
					writer.println(" $flowFrom isa " + getBPMNEntityNamePrefix() + "sequenceFlow, has "
							+ getBPMNAttributeNamePrefix() + "sourceRef $fromSource, has "
							+ getBPMNAttributeNamePrefix() + "targetRef $fromTarget;");
					writer.println(" $fromTarget = $gateId;");
					writer.println(" $fromSource = $taskFromId;");
					writer.println(" (bpmnEntity: $bpmntaskFrom, conceptualModel: $taskFrom) isa "
							+ getBPMNConceptualModelMappingName() + ";");
					writer.println("} then {");
					writer.println("     (task: $taskFrom, precedence_task: $prec) isa isCompoundBySetOfTask;");
					writer.println("};");
					writer.println();
				} // end of AND/ORPrecedenceTaskList isCompoundBySetOfTask Task, Transitive

			} // end of isPrecededBySetOfTask/isCompoundBySetOfTask

			// Show sample queries
			writer.println("## Sample queries for the above rules");
			writer.println();

			writer.println("## query " + getIsCompoundByRelationName());
			writer.println("# match ");
			writer.println("# $r isa " + getIsCompoundByRelationName() + "; ");
			writer.println("# $m isa Mission, has " + getUIDAttributeName() + " $muid; ");
			writer.println("# $t isa Task, has " + getUIDAttributeName() + " $tuid; ");
			writer.println("# $bpmntask isa " + getBPMNEntityName() + ", has " + getUIDAttributeName() + " $buid;");
			writer.println(
					"# (bpmnEntity: $bpmntask, conceptualModel: $t) isa " + getBPMNConceptualModelMappingName() + ";");
			writer.println("# get $m,$t,$r,$bpmntask,$muid,$tuid,$buid;");
			writer.println();

			writer.println("## query " + getIsPerformedByRelationName());
			writer.println("# match");
			writer.println("# $bpmntask isa " + getBPMNEntityName() + ", has " + getUIDAttributeName() + " $uid1;");
			writer.println("# $bpmnperfomer isa " + getBPMNEntityName() + ", has " + getUIDAttributeName() + " $uid2;");
			writer.println("# $rel1 (task: $task, performer: $performer) isa " + getIsPerformedByRelationName() + ";");
			writer.println("# $rel2 (bpmnEntity: $bpmntask, conceptualModel: $task) isa "
					+ getBPMNConceptualModelMappingName() + ";");
			writer.println("# $rel3 (bpmnEntity: $bpmnperfomer, conceptualModel: $performer) isa "
					+ getBPMNConceptualModelMappingName() + ";");
			writer.println("# get $rel1, $rel2, $rel3, $uid1, $uid2;");
			writer.println();

			writer.println("## query " + getProvidesRelationName());
			writer.println("# match");
			writer.println("# $asset isa Asset, has " + getUIDAttributeName() + " $uid1;");
			writer.println("# $service isa Service, has " + getUIDAttributeName() + " $uid2;");
			writer.println("# $bpmnasset isa " + getBPMNEntityName() + ", has " + getUIDAttributeName() + " $uid3;");
			writer.println("# $bpmnservice isa " + getBPMNEntityName() + ", has " + getUIDAttributeName() + " $uid4;");
			writer.println("# $rel1 (asset: $asset, service: $service) isa " + getProvidesRelationName() + ";");
			writer.println("# $rel2 (bpmnEntity: $bpmnasset, conceptualModel: $asset) isa "
					+ getBPMNConceptualModelMappingName() + ";");
			writer.println("# $rel3 (bpmnEntity: $bpmnservice, conceptualModel: $service) isa "
					+ getBPMNConceptualModelMappingName() + ";");
			writer.println("# get $rel1, $rel2, $rel3, $uid1, $uid2, $uid3, $uid4;");
			writer.println();

			writer.println("## query isPrecededBySetOfTask and isCompoundBySetOfTask associated with sequenceFlow");
			writer.println("# match");
			writer.println("# $p isa PrecedenceTask;");
			writer.println("# $t1 isa Task;");
			writer.println("# $t2 isa Task;");
			writer.println("# $r1  (precedence_task: $p, task: $t2) isa isPrecededBySetOfTask; ");
			writer.println("# $r2  (precedence_task: $p, task: $t1) isa isCompoundBySetOfTask; ");
			writer.println("# $bpmntask1 isa " + getBPMNEntityName() + ";");
			writer.println("# $bpmntask2 isa " + getBPMNEntityName() + ";");
			writer.println("# $seq isa " + getBPMNEntityNamePrefix() + "sequenceFlow;");
			writer.println("# $rel1 (bpmnEntity: $bpmntask1, conceptualModel: $t1) isa "
					+ getBPMNConceptualModelMappingName() + ";");
			writer.println("# $rel2 (bpmnEntity: $bpmntask2, conceptualModel: $t2) isa "
					+ getBPMNConceptualModelMappingName() + ";");
			writer.println("# $rel3  (bpmnEntity: $seq, conceptualModel: $p) isa " + getBPMNConceptualModelMappingName()
					+ ";");
			writer.println();

			writer.println("## Query AND/ORPrecedenceTaskList");
			writer.println("# match");
			writer.println("# $taskFrom isa Task;");
			writer.println("# $taskTo isa Task;");
			writer.println("# {$prec isa ANDPrecedenceTaskList;} or {$prec isa ORPrecedenceTaskList;};");
			writer.println("# $relFrom (task: $taskFrom, precedence_task: $prec) isa isCompoundBySetOfTask;");
			writer.println("# $relTo (task: $taskTo, precedence_task: $prec) isa isPrecededBySetOfTask;");
			writer.println("# $bpmntaskFrom isa " + getBPMNEntityNamePrefix() + "Activity, has "
					+ getBPMNAttributeNamePrefix() + "name $attribFrom;");
			writer.println("# $bpmntaskTo isa " + getBPMNEntityNamePrefix() + "Activity, has "
					+ getBPMNAttributeNamePrefix() + "name $attribTo;");
			writer.println("# $mapFrom (bpmnEntity: $bpmntaskFrom, conceptualModel: $taskFrom) isa "
					+ getBPMNConceptualModelMappingName() + ";");
			writer.println("# $mapTo (bpmnEntity: $bpmntaskTo, conceptualModel: $taskTo) isa "
					+ getBPMNConceptualModelMappingName() + ";");
			writer.println();

		} // else ignore mappings to conceptual model

		// a sample query for the ancestor-descendant relationship
		writer.println("## Query descendants of BPMN definitions tag");
		writer.println("#match");
		writer.println("# $definition isa " + getBPMNEntityNamePrefix() + "definitions, has attribute $attrib_root;");
		writer.println("# $descendant isa " + getBPMNEntityName() + ", has attribute $attrib;");
		writer.println("# $rel (ancestor: $definition, descendant: $descendant) isa "
				+ getBPMNTransitiveAncestorRelationName() + ";");
		writer.println();

	}

	/**
	 * Parses the content of {@link #getJSONConceptsNotToAddRole()}
	 * 
	 * @return collection of concept names not to be included as roles in
	 *         relationships (probably because the super-entity already does declare
	 *         such role).
	 */
	protected Collection<String> parseJSONConceptsNotToAddRole() {

		Collection<String> ret = new HashSet<>();

		try {
			JSONArray array = new JSONArray(getJSONConceptsNotToAddRole());
			array.forEach(obj -> ret.add(obj.toString()));
		} catch (Exception e) {
			logger.warn("Failed to parse list of concepts not to add roles: {}", getJSONConceptsNotToAddRole());
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
	has UID "https://camunda.org/examples#definitions123";
	
	insert $proc isa BPMN_process,
	has UID "https://camunda.org/examples#proc123";
	match
	$parent isa BPMN_definitions, has UID "https://camunda.org/examples#definitions123";
	$child isa BPMN_process, has UID "https://camunda.org/examples#proc123";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	insert $startEvent isa BPMN_startEvent,
	has BPMN_id "start",
	has UID "https://camunda.org/examples#start";
	match
	$parent isa entity, has UID "https://camunda.org/examples#proc123";
	$child isa entity, has UID "https://camunda.org/examples#start";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	insert $outgoing isa BPMN_outgoing,
	has BPMN_textContent "flow1",
	has UID "https://camunda.org/examples#outgoing1";
	match
	$parent isa entity, has UID "https://camunda.org/examples#start";
	$child isa entity, has UID "https://camunda.org/examples#outgoing1";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	insert $userTask isa BPMN_userTask,
	has BPMN_id "task",
	has BPMN_name "User Task",
	has UID "https://camunda.org/examples#task";
	match
	$parent isa entity, has UID "https://camunda.org/examples#proc123";
	$child isa entity, has UID "https://camunda.org/examples#task";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	insert $incoming isa BPMN_incoming,
	has BPMN_textContent "flow1",
	has UID "https://camunda.org/examples#taskincoming";
	match
	$parent isa entity, has UID "https://camunda.org/examples#task";
	$child isa entity, has UID "https://camunda.org/examples#taskincoming";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	insert $outgoing isa BPMN_outgoing,
	has BPMN_textContent "flow2",
	has UID "https://camunda.org/examples#taskoutgoing";
	match
	$parent isa entity, has UID "https://camunda.org/examples#task";
	$child isa entity, has UID "https://camunda.org/examples#taskoutgoing";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	insert $sequenceFlow isa BPMN_sequenceFlow,
	has BPMN_id "flow1",
	has BPMN_sourceRef "start",
	has BPMN_targetRef "task",
	has UID "https://camunda.org/examples#flow1";
	match
	$parent isa entity, has UID "https://camunda.org/examples#proc123";
	$child isa entity, has UID "https://camunda.org/examples#flow1";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	insert $endEvent isa BPMN_endEvent,
	has BPMN_id "end",
	has UID "https://camunda.org/examples#end";
	match
	$parent isa entity, has UID "https://camunda.org/examples#proc123";
	$child isa entity, has UID "https://camunda.org/examples#end";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	insert $incoming isa BPMN_incoming,
	has BPMN_textContent "flow2",
	has UID "https://camunda.org/examples#endincoming";
	match
	$parent isa entity, has UID "https://camunda.org/examples#end";
	$child isa entity, has UID "https://camunda.org/examples#endincoming";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	insert $sequenceFlow isa BPMN_sequenceFlow,
	has BPMN_id "flow2",
	has BPMN_sourceRef "task",
	has BPMN_targetRef "end",
	has UID "https://camunda.org/examples#flow2";
	match
	$parent isa entity, has UID "https://camunda.org/examples#proc123";
	$child isa entity, has UID "https://camunda.org/examples#flow2";
	insert $rel (parent: $parent, child: $child) isa BPMN_hasChildTag;
	
	## references to the conceptual model
	insert $mission isa Mission,
	has UID "https://camunda.org/examples#Mission_proc123";
	match
	$bpmnEntity isa BPMN_Entity, has UID 'https://camunda.org/examples#proc123';
	$conceptualModel isa entity, has UID 'https://camunda.org/examples#Mission_proc123';
	insert $rel (bpmnEntity: $bpmnEntity, conceptualModel: $conceptualModel) isa BPMN_hasConceptualModelElement;
	
	insert $task isa Task,
	has UID "https://camunda.org/examples#Task_task";
	match
	$bpmnEntity isa BPMN_Entity, has UID 'https://camunda.org/examples#task';
	$conceptualModel isa entity, has UID 'https://camunda.org/examples#Task_task';
	insert $rel (bpmnEntity: $bpmnEntity, conceptualModel: $conceptualModel) isa BPMN_hasConceptualModelElement;
	match
	$task isa Task, has UID 'https://camunda.org/examples#Task_task';
	$mission isa Mission, has UID 'https://camunda.org/examples#Mission_proc123';
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

		// Entities that are sensitive to ordering (like points in edge)
		Collection<String> sortableEntities = parseJSONSortableEntities();

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
					parseJSONMap(getJSONBPMNConceptualModelMap()),
					// some entities (e.g., points in edge) should be sorted
					sortableEntities);

			writer.println("## =============== End ===============");

			logger.info("Finished TypeQL data insertion");

		} // this will close writer

	}

	/**
	 * @return parsed {@link #getJSONSortableEntities()}
	 */
	protected Collection<String> parseJSONSortableEntities() {
		Collection<String> ret = new HashSet<>();

		JSONArray array = new JSONArray(getJSONSortableEntities());
		for (Object obj : array) {
			ret.add(obj.toString());
		}

		return ret;
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
	 * @param sortableEntities         : some entities (e.g., points in edges)
	 *                                 should be sorted.
	 * @see #getSortAttributeName()
	 * @see #parseJSONSortableEntities()
	 */
	protected void visitBPMNDataRecursive(PrintWriter writer, ModelElementInstance currentNode, String namespace,
			String parentUID, Set<String> usedUIDs, Map<String, String> bpmnToConceptualModelMap,
			Collection<String> sortableEntities) throws IOException {

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
		 * 		has UID "https://camunda.org/examples#definitions123";
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
		writer.println("\t has " + getUIDAttributeName() + " \"" + currentUID + "\";");

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
				writer.println("\t $parent isa " + getBPMNEntityName() + ", has " + getUIDAttributeName() + " \""
						+ parentUID + "\";");
				writer.println("\t $child isa " + getBPMNEntityName() + ", has " + getUIDAttributeName() + " \""
						+ currentUID + "\";");
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
			String conceptModelEntity = resolveName(bpmnToConceptualModelMap, currentEntityOriginalName,
					currentNode.getClass());

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
				writer.println("insert $concept isa " + conceptModelEntity + ", has " + getUIDAttributeName() + " \""
						+ conceptUID + "\";");
				// Add the relation to the above instance
				writer.println("match");
				writer.println("\t $bpmnEntity isa " + getBPMNEntityName() + ", has " + getUIDAttributeName() + " '"
						+ currentUID + "';");
				writer.println("\t $concept isa " + getRootConceptualModelEntityName() + ", has "
						+ getUIDAttributeName() + " '" + conceptUID + "';");
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
		List<ModelElementInstance> childrenToVisit = new ArrayList<>();

		for (ModelElementType childType : currentNode.getElementType().getAllChildElementTypes()) {
			// Consider only known child elements
			Collection<ModelElementInstance> children = currentNode.getChildElementsByType(childType);
			if (sortableEntities.contains(childType.getTypeName())) {
				// These children should have an attribute for explicit sorting.
				logger.debug("Entity {} should be sorted. Adding attribute {}.", childType.getTypeName(),
						getSortAttributeName());
				// Iterate on children and add such attribute explicitly...
				Iterator<ModelElementInstance> iterator = children.iterator();
				for (int order = 0; iterator.hasNext(); order++) {
					ModelElementInstance child = iterator.next();
					child.setAttributeValue(getSortAttributeName(), String.valueOf(order));
				}
			}
			childrenToVisit.addAll(children);
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
					bpmnToConceptualModelMap,
					// some entities (e.g., points in edges) should be sorted
					sortableEntities);
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
	 * 
	 * @return true if the test passed. False otherwise.
	 */
	public boolean checkDefinitionReferences(String typeql) throws ParseException, TypeQLException {

		Collection<String> namesToIgnore = parseJSONNamesToIgnoreInSanityCheck();

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
					// ignore "uid" since it's part of conceptual model, if we're mapping to it
					&& !(isMapBPMNToConceptualModel()
							&& typeVar.reference().asLabel().label().equals(getUIDAttributeName()))) {
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
					String name = typeVar.sub().orElseThrow().type().reference().asLabel().label();
					if (!namesToIgnore.contains(name)) {
						logger.debug("Ignored entity {}", name);
						referredEntities.add(name);
					}
				} // else: no need to store references to the top entity
			}
			// store references to attributes in 'owns' declaration
			for (Owns owns : typeVar.owns()) {
				referredAttributes.addAll(owns.variables().stream()
						// extract the labels after 'owns'
						.map(ownVar -> ownVar.reference().asLabel().label())
						// ignore "uid" since it's part of conceptual model
						.filter(label -> (!label.equals(getUIDAttributeName())))
						// ignore those in the collection of names to ignore
						.filter(label -> !namesToIgnore.contains(label)).collect(Collectors.toSet()));
			}
			// store references to relations/roles in 'plays' declaration
			for (Plays plays : typeVar.plays()) {
				// update map of referred relations and roles
				String roleLabel = plays.role().reference().asLabel().label();
				// role should be like reference:role
				String relationLabel = roleLabel.split(":")[0];
				// ignore those in the names to ignore
				if (namesToIgnore.contains(relationLabel)) {
					logger.debug("Ignored relation {}", relationLabel);
					continue;
				}
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

		// All rules must refer to declared entities, attributes, and relations.
		List<Rule> rules = define.rules();
		// use an index to keep track of which rule we are verifying now
		for (int ruleIndex = 0; ruleIndex < rules.size(); ruleIndex++) {

			// check the current rule
			Rule rule = rules.get(ruleIndex);

			// check for referred entity/relation/attribute names
			// in the list of conditions
			for (Pattern pattern : rule.when().patterns()) {
				BoundVariable variable = pattern.asVariable();
				if (variable.isThing()) {
					ThingVariable<?> thing = variable.asThing();
					Optional<Relation> relation = thing.relation();
					Optional<Isa> isa = thing.isa();
					if (relation.isPresent()) {
						// this is a relation
						if (isa.isPresent()) {
							String relationName = isa.get().type().toString();
							if (!namesToIgnore.contains(relationName)
									&& !declaredRelationRoles.containsKey(relationName)) {
								throw new ParseException(
										"No declaration found for relation " + relationName + " in " + pattern,
										ruleIndex);
							}
						}
					} else {
						// entity or attribute
						if (isa.isPresent()) {
							// extract what's after "isa"
							String entityOrAttribName = isa.get().type().toString();
							if (!namesToIgnore.contains(entityOrAttribName)) {
								// verify only the names that start with the expected prefixes
								if (entityOrAttribName.startsWith(getBPMNEntityNamePrefix())
										&& !declaredEntities.contains(entityOrAttribName)) {
									throw new ParseException(
											"No declaration found for entity " + entityOrAttribName + " in " + pattern,
											ruleIndex);
								} else if (entityOrAttribName.startsWith(getBPMNAttributeNamePrefix())
										&& !declaredAttributes.contains(entityOrAttribName)) {
									throw new ParseException("No declaration found for attribute " + entityOrAttribName
											+ " in " + pattern, ruleIndex);
								}
							}
						}
						// check the list of attributes
						for (Has has : thing.has()) {
							Optional<Isa> attribIsA = has.attribute().isa();
							if (attribIsA.isPresent()) {
								// get attribute type
								String attribName = attribIsA.get().type().toString();
								// only consider attributes starting with BPMN prefix
								if (!namesToIgnore.contains(attribName)
										&& attribName.startsWith(getBPMNAttributeNamePrefix())
										&& !declaredAttributes.contains(attribName)) {
									throw new ParseException(
											"No declaration found for attrbute " + attribName + " in " + pattern,
											ruleIndex);
								}
							}

						} // end of iteration on attributes

					} // end of if relation else

				} // else variable is not a "thing" (so ignore)

			} // end of iteration on patterns inside the condition of this rule

			// No need to check referred relations in the conclusion
			// because these are likely to be relations in the concept model
			// (which are not declared in the BPMN schema).
//			Optional<Isa> isa = rule.then().isa();
//			if (isa.isPresent()) {
//				String thingName = isa.get().type().toString();
//				if (!declaredRelationRoles.containsKey(thingName) && !declaredEntities.contains(thingName)
//						&& !declaredAttributes.contains(thingName)) {
//					throw new ParseException("No declaration found for " + thingName + " in " + rule, ruleIndex);
//				}
//			}

		} // end of iteration on all rules

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
	 * @return {@link #getJSONNamesToIgnoreInSanityCheck()} parsed to a collection.
	 * 
	 * @see #checkDefinitionReferences(String)
	 * @see #getJSONNamesToIgnoreInSanityCheck()
	 */
	protected Collection<String> parseJSONNamesToIgnoreInSanityCheck() {

		Collection<String> ret = new HashSet<>();

		try {
			JSONArray array = new JSONArray(getJSONNamesToIgnoreInSanityCheck());
			array.forEach(obj -> ret.add(obj.toString()));
		} catch (Exception e) {
			logger.warn("Failed to parse list of names to ignore in sanity check: {}",
					getJSONNamesToIgnoreInSanityCheck());
		}

		return ret;
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
	 * @return the providesRelationName
	 */
	public String getProvidesRelationName() {
		return providesRelationName;
	}

	/**
	 * @param providesRelationName the requiresRelationName to set
	 */
	public void setProvidesRelationName(String providesRelationName) {
		this.providesRelationName = providesRelationName;
	}

	/**
	 * @return JSON array containing the names of concepts not to include in roles.
	 * @see #getJSONBPMNConceptualModelMap()
	 * @see #parseJSONConceptsNotToAddRole()
	 */
	public String getJSONConceptsNotToAddRole() {
		return jsonConceptsNotToAddRole;
	}

	/**
	 * @param jsonConceptsNotToAddRole : JSON array containing the names of concepts
	 *                                 not to include in roles.
	 * @see #getJSONBPMNConceptualModelMap()
	 * @see #parseJSONConceptsNotToAddRole()
	 */
	public void setJSONConceptsNotToAddRole(String jsonConceptsNotToAddRole) {
		this.jsonConceptsNotToAddRole = jsonConceptsNotToAddRole;
	}

	/**
	 * @return JSON list of entity name that should contain a numeric attribute for
	 *         sorting.
	 */
	public String getJSONSortableEntities() {
		return jsonSortableEntities;
	}

	/**
	 * @param entities : JSON list of entity name that should contain a numeric
	 *                 attribute for sorting.
	 */
	public void setJSONSortableEntities(String entities) {
		this.jsonSortableEntities = entities;
	}

	/**
	 * @return attribute name used in {@link #getJSONSortableEntities()} to sort the
	 *         entities that are sensitive to the ordering. Prefix
	 *         {@link #getBPMNAttributeNamePrefix()} will be appended.
	 */
	public String getSortAttributeName() {
		return sortAttributeName;
	}

	/**
	 * @param sortAttributeName : attribute name used in
	 *                          {@link #getJSONSortableEntities()} to sort the
	 *                          entities that are sensitive to the ordering. Prefix
	 *                          {@link #getBPMNAttributeNamePrefix()} will be
	 *                          appended.
	 */
	public void setSortAttributeName(String sortAttributeName) {
		this.sortAttributeName = sortAttributeName;
	}

	/**
	 * @return the name of the root entity in the conceptual model
	 */
	public String getRootConceptualModelEntityName() {
		return rootConceptualModelEntityName;
	}

	/**
	 * @param name : the name of the root entity in the conceptual model
	 */
	public void setRootConceptualModelEntityName(String name) {
		rootConceptualModelEntityName = name;
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

	/**
	 * @return JSON map specifying common super entities for some BPMN entities. For
	 *         example, tasks/subprocesses/calls should be BPMN_Activity; and
	 *         parallel/inclusive/exclusive/complex/event-based gateways should be
	 *         BPMN_Gateway.
	 */
	public String getJSONCommonBPMNSuperEntityMap() {
		return jsonCommonBPMNSuperEntityMap;
	}

	/**
	 * @param jsonMap : JSON map specifying common super entities for some BPMN
	 *                entities. For example, tasks/subprocesses/calls should be
	 *                BPMN_Activity; and
	 *                parallel/inclusive/exclusive/complex/event-based gateways
	 *                should be BPMN_Gateway.
	 */
	public void setJSONCommonBPMNSuperEntityMap(String jsonMap) {
		this.jsonCommonBPMNSuperEntityMap = jsonMap;
	}

	/**
	 * @return name of the relation that represents the transitive closure of
	 *         gateway precedence.
	 */
	public String getBPMNGatewayTransitiveChainRelationName() {
		return bpmnGatewayTransitiveChainRelationName;
	}

	/**
	 * @param name : name of the relation that represents the transitive closure of
	 *             gateway precedence.
	 */
	public void setBPMNGatewayTransitiveChainRelationName(String name) {
		bpmnGatewayTransitiveChainRelationName = name;
	}

	/**
	 * @return JSON list specifying the names of entities/attributes/relations to
	 *         ignore in the test at {@link #checkDefinitionReferences(String)}
	 * 
	 * @see #parseJSONNamesToIgnoreInSanityCheck()
	 */
	public String getJSONNamesToIgnoreInSanityCheck() {
		return jsonNamesToIgnoreInSanityCheck;
	}

	/**
	 * @param jsonList : SON list specifying the names of
	 *                 entities/attributes/relations to ignore in the test at
	 *                 {@link #checkDefinitionReferences(String)}
	 * 
	 * @see #parseJSONNamesToIgnoreInSanityCheck()
	 */
	public void setJSONNamesToIgnoreInSanityCheck(String jsonList) {
		this.jsonNamesToIgnoreInSanityCheck = jsonList;
	}

	/**
	 * @return name of the transitive relationship that connects an XML tag to its
	 *         descendants.
	 * 
	 * @see #getBPMNParentChildRelationName()
	 */
	public String getBPMNTransitiveAncestorRelationName() {
		return bpmnTransitiveAncestorRelationName;
	}

	/**
	 * @param name : name of the transitive relationship that connects an XML tag to
	 *             its descendants.
	 * 
	 * @see #getBPMNParentChildRelationName()
	 */
	public void setBPMNTransitiveAncestorRelationName(String name) {
		bpmnTransitiveAncestorRelationName = name;
	}

}
