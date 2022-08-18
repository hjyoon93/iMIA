package edu.gmu.c4i.dalnim.typedb2bpmn.decoder;

import java.io.IOException;
import java.io.OutputStream;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Collection;
import java.util.List;
import java.util.Properties;
import java.util.stream.Collectors;

import org.apache.commons.lang3.StringUtils;
import org.camunda.bpm.model.bpmn.Bpmn;
import org.camunda.bpm.model.bpmn.BpmnModelInstance;
import org.camunda.bpm.model.bpmn.impl.BpmnModelConstants;
import org.camunda.bpm.model.bpmn.instance.Definitions;
import org.camunda.bpm.model.xml.instance.ModelElementInstance;
import org.camunda.bpm.model.xml.type.ModelElementType;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.vaticle.typedb.client.TypeDB;
import com.vaticle.typedb.client.api.TypeDBClient;
import com.vaticle.typedb.client.api.TypeDBOptions;
import com.vaticle.typedb.client.api.TypeDBSession;
import com.vaticle.typedb.client.api.TypeDBTransaction;
import com.vaticle.typedb.client.api.answer.ConceptMap;
import com.vaticle.typedb.client.api.concept.Concept;
import com.vaticle.typedb.client.api.concept.thing.Attribute;
import com.vaticle.typedb.client.api.concept.thing.Entity;

import edu.gmu.c4i.dalnim.util.ApplicationProperties;

/**
 * Default implementation of {@link Decoder} that reads a BPMN project from
 * TypeDB database and saves the content to a BPMN2 file format.
 * 
 * @author shou
 */
public class DecoderImpl implements Decoder {

	private static Logger logger = LoggerFactory.getLogger(DecoderImpl.class);

	private String typeDBAddress = "localhost:1729";

	private String databaseName = "BPMN";

	private String rootUID = "https://camunda.org/examples/#.*";

	private String parentUIDAttributeName = "parentUID";

	private String parentUID = rootUID;

	// TODO substitute entity/relation names with "@{key}" tags
	private String rootQueryTemplate = "## Query BPMN root by regex on UID (regex matches BPMN definitions or Mission in concept model)\n"
			+ "match\n" + "$query like \"@{rootUID}\";\n"
			+ "$entity isa BPMN_definitions, has uid $uid_b, has attribute $attribute;\n"
			+ "$mission isa Mission, has uid $uid_m;\n" + "{ $uid_m = $query; } or {  $uid_b = $query ;};\n"
			+ "(bpmnEntity: $entity, conceptualModel: $mission) isa BPMN_hasConceptualModelElement;\n"
			+ "get $entity, $attribute;";

	// TODO substitute entity/relation names with "@{key}" tags
	private String childQueryTemplate = "## query BPMN child and its attributes\n" + "match\n"
			+ "$parent has uid \"@{parentUID}\";\n" + "$entity isa BPMN_Entity, has attribute $attribute;\n"
			+ "(parent: $parent, child: $entity) isa BPMN_hasChildTag;\n" + "get $entity, $attribute;";

	private String bpmnEntityNamePrefix = "BPMN_";

	private String bpmnAttributeNamePrefix = "BPMNattrib_";

	private String bpmnTextContentAttributeName = bpmnEntityNamePrefix + "textContent";

	private boolean runSanityCheck = true;

	/**
	 * Default constructor is protected from public access. Use
	 * {@link #getInstance()} instead.
	 */
	protected DecoderImpl() {
		// Auto-generated constructor stub
	}

	/**
	 * Default constructor method.
	 * 
	 * @return a new instance of {@link DecoderImpl}
	 */
	public static Decoder getInstance() {

		Decoder ret = new DecoderImpl();

		try {
			ApplicationProperties.getInstance().loadApplicationProperties(ret);
		} catch (Exception e) {
			logger.warn("Failed to load application.properties. Ignoring...", e);
		}
		return ret;
	}

	@Override
	public void saveBPMN(OutputStream outputStream) throws IOException {

		String dbAddress = getTypeDBAddress();
		logger.info("Starting a connection to TypeDB at {}", dbAddress);
		TypeDBClient client = TypeDB.coreClient(dbAddress);
		logger.debug("Created connection to TypeDB: {}", client);

		// the database name to query
		String database = getDatabaseName();

		// Obtains a property object pre-filled with attributes in this class.
		// This information will be used to build queries.
		Properties queryProperties = this.getQueryPropertiesFromFields();

		// query the root node (definitions)
		String query = getQuery(getRootQueryTemplate(), queryProperties);

		// prepare the BPMN model to write
		BpmnModelInstance bpmnModel = Bpmn.createEmptyModel();

		// option to turn inference mode on
		TypeDBOptions inferOption = TypeDBOptions.core().infer(true);

		// start a session to query the database
		logger.info("Creating a session to database '{}'", database);
		try (TypeDBSession session = client.session(database, TypeDBSession.Type.DATA,
				// enable inference mode
				inferOption)) {

			// save the root entity as 'definitions'
			Definitions definitions = bpmnModel.newInstance(Definitions.class);

			// Run a transaction to extract the BPMN 'definitions' node from the answer
			try (TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.READ,
					// enable inference mode
					inferOption)) {

				// Run query.
				// This query is supposed to return an entity and its attributes
				List<ConceptMap> response = transaction.query().match(query).collect(Collectors.toList());

				// Assume we have only 1 entity (the root) in the response. Get it.
				Concept entity = response.stream().flatMap(map -> map.concepts().stream()).filter(Concept::isEntity)
						.findAny().orElseThrow(() -> new IOException(
								"No root entity (BPMN definitions) found. Response: " + response));

				// extract the attributes
				Collection<Attribute<?>> attributes = response.stream()
						// only consider those related to the root entity
						.filter(map -> map.concepts().contains(entity)).flatMap(map -> map.concepts().stream())
						// convert to attributes
						.filter(Concept::isAttribute).map(Concept::asAttribute).distinct().collect(Collectors.toSet());

				// Save the attributes.
				// Store the uid.
				String uid = null;
				for (Attribute<?> attrib : attributes) {

					String attribName = attrib.getType().getLabel().name();
					String attribValue = attrib.asString().getValue();

					// handle some special attributes
					if (attribName.equals(getBPMNAttributeNamePrefix() + "xmlns")) {
						// No need to change the model's BPMN namespace
						// because it is already set by camunda library.
						logger.debug("xmlns of entity {} is {}", entity, attribName);
					} else if (attribName.equals("uid")) {
						uid = attribValue;
						// no need to store UID in BPMN
						logger.debug("uid of entity {} is {}", entity, attribName);
					} else if (attribName.equals(getBPMNAttributeNamePrefix() + "targetNamespace")) {
						definitions.setTargetNamespace(attribValue);
					} else if (attribName.equals(getBPMNAttributeNamePrefix() + "id")) {
						definitions.setId(attribValue);
					} else if (attribName.equals(getBPMNAttributeNamePrefix() + "name")) {
						definitions.setName(attribValue);
					} else {
						// handle ordinary attributes
						if (attribName.startsWith(getBPMNAttributeNamePrefix())) {
							// remove prefix if any
							attribName = attribName.substring(getBPMNAttributeNamePrefix().length());
						}
						definitions.setAttributeValue(attribName, attribValue);
					}
				}

				// update the definitions (root) in BPMN model
				bpmnModel.setDefinitions(definitions);

				// update the parent uid for the recursive call
				queryProperties.setProperty(getParentUIDAttributeName(), uid);

			} // end of TypeDB transaction

			// recursively access children
			visitChildrenRecursive(bpmnModel, definitions, session, queryProperties);

		} // end of TypeDB session

		// make sure to close the connection to TypeDB
		logger.debug("Closing connection to TypeDB: {}", client);
		client.close();

		// save the BPMN model
		logger.debug("Saving the model...");
		Bpmn.writeModelToStream(outputStream, bpmnModel);

		// run basic sanity check
		if (isRunSanityCheck()) {
			logger.debug("Checking model validity");
			Bpmn.validateModel(bpmnModel);
		}
	}

	/**
	 * Recursively visit the children.
	 * 
	 * @param currentNode
	 * @param parentNode
	 * @param definitions
	 * @param session
	 * @param queryProperties
	 * 
	 * @throws IOException
	 */
	protected void visitChildrenRecursive(BpmnModelInstance bpmnModel, ModelElementInstance parentNode,
			TypeDBSession session, Properties queryProperties) throws IOException {

		// Prepare a query to the child BPMN tags
		// use the template to query the child node
		String query = getQuery(getChildQueryTemplate(), queryProperties);

		// Run a transaction to extract the child nodes
		List<ConceptMap> response = null;
		logger.debug("Querying children of {}. Query is:\n{}", parentNode, query);
		try (TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.READ,
				// enable inference mode
				TypeDBOptions.core().infer(true))) {

			// Run query.
			// This query is supposed to return multiple entities and their attributes
			response = transaction.query().match(query).collect(Collectors.toList());

		} // end of TypeDB transaction

		// Keep transaction life short: run recursive calls outside transaction.

		// we should have some response
		if (response == null) {
			throw new IOException(
					"Null response obtained while querying children of " + parentNode + ". Query was:\n " + query);
		}

		// retrieve the children
		for (Entity childTypeDBEntity : response.stream().flatMap(map -> map.concepts().stream())
				// iterate on entities only
				.filter(Concept::isEntity).map(Concept::asEntity).collect(Collectors.toSet())) {

			logger.debug("Creating BPMN child for entity {}", childTypeDBEntity);

			// extract the child entity name
			String childEntityName = childTypeDBEntity.getType().getLabel().name();
			// remove prefix, if any
			if (childEntityName.startsWith(getBPMNEntityNamePrefix())) {
				childEntityName = childEntityName.substring(getBPMNEntityNamePrefix().length());
			}

			// create a BPMN node accordingly to the name of the entity
			// translate TypeDB-type to BPMN-type.
			ModelElementType childBPMNType = getElementTypeByName(bpmnModel, childEntityName);
			if (childBPMNType == null) {
				logger.error("BPMN node of type '{}' is not supported. Ignoring...", childEntityName);
				continue;
			}

			// create a new BPMN node of this type
			logger.debug("Creating BPMN child of type '{}'", childEntityName);
			ModelElementInstance childBPMNNode = bpmnModel.newInstance(childBPMNType);

			// add the new node as child of the parent node
			parentNode.addChildElement(childBPMNNode);

			// extract the attributes associated with current entity
			Collection<Attribute<?>> attributes = response.stream()
					// only consider those related to the current entity
					.filter(map -> map.concepts().contains(childTypeDBEntity)).flatMap(map -> map.concepts().stream())
					// convert to attributes
					.filter(Concept::isAttribute).map(Concept::asAttribute).distinct().collect(Collectors.toSet());

			// Keep track of the uid.
			String uid = null;
			// Save the attributes.
			for (Attribute<?> attrib : attributes) {

				String attribName = attrib.getType().getLabel().name();
				String attribValue = attrib.asString().getValue();

				// handle some special attributes
				if (attribName.equals("uid")) {
					uid = attribValue;
					// no need to store UID in BPMN
					logger.debug("uid of entity {} is {}", childTypeDBEntity, attribName);
				} else if (attribName.equals(getBPMNTextContentAttributeName())) {
					// in BPMN, text content is a child instead of attribute.
					logger.debug("Text content found for {}. Text is '{}'", childBPMNNode, attribValue);
					childBPMNNode.setTextContent(attribValue);
				} else {
					// handle ordinary attributes
					if (attribName.startsWith(getBPMNAttributeNamePrefix())) {
						// remove prefix if any
						attribName = attribName.substring(getBPMNAttributeNamePrefix().length());
					}
					childBPMNNode.setAttributeValue(attribName, attribValue);
				}
			} // end of iteration on attributes

			// update parent UID in next recursive call
			queryProperties.setProperty(getParentUIDAttributeName(), uid);

			// call recursive
			visitChildrenRecursive(bpmnModel, childBPMNNode, session, queryProperties);

		} // end of iteration on each child entity

	}

	protected ModelElementType getElementTypeByName(BpmnModelInstance bpmnModel, String name) {

		// try default root namespace first
		ModelElementType elementType = bpmnModel.getModel()
				.getTypeForName(bpmnModel.getDocument().getRootElement().getNamespaceURI(), name);
		if (elementType != null) {
			logger.debug("Found type {} from root namespace {}.", elementType,
					bpmnModel.getDocument().getRootElement().getNamespaceURI());
			return elementType;
		}

		// Try other namespaces if we did not find with default namespace
		// These are ordered by relevance...

		// The BPMN 2.0 namespace
		elementType = bpmnModel.getModel().getTypeForName(BpmnModelConstants.BPMN20_NS, name);
		if (elementType != null) {
			logger.debug("Found type {} from BPMN 2.0 namespace.", elementType);
			return elementType;
		}

		// The BPMNDI namespace
		elementType = bpmnModel.getModel().getTypeForName(BpmnModelConstants.BPMNDI_NS, name);
		if (elementType != null) {
			logger.debug("Found type {} from BPMNDI namespace.", elementType);
			return elementType;
		}

		// The DC namespace
		elementType = bpmnModel.getModel().getTypeForName(BpmnModelConstants.DC_NS, name);
		if (elementType != null) {
			logger.debug("Found type {} from DC namespace.", elementType);
			return elementType;
		}

		// The DI namespace
		elementType = bpmnModel.getModel().getTypeForName(BpmnModelConstants.DI_NS, name);
		if (elementType != null) {
			logger.debug("Found type {} from DI namespace.", elementType);
			return elementType;
		}

		// The XSI namespace
		elementType = bpmnModel.getModel().getTypeForName(BpmnModelConstants.XSI_NS, name);
		if (elementType != null) {
			logger.debug("Found type {} from XSI namespace.", elementType);
			return elementType;
		}

		// Xml Schema is the default type language
		elementType = bpmnModel.getModel().getTypeForName(BpmnModelConstants.XML_SCHEMA_NS, name);
		if (elementType != null) {
			logger.debug("Found type {} from XML Schema namespace.", elementType);
			return elementType;
		}

		// XPATH namespace
		elementType = bpmnModel.getModel().getTypeForName(BpmnModelConstants.XPATH_NS, name);
		if (elementType != null) {
			logger.debug("Found type {} from XPATH namespace.", elementType);
			return elementType;
		}

		logger.warn("No type of name {} found in the known namespaces...", name);
		return null;
	}

	/**
	 * <p>
	 * Builds a TypeQL query script by reading a template and substituting the
	 * occurrences of "@{key}" to values in the provided {@link Properties}.
	 * </p>
	 * <p>
	 * For example, if the template is like the following:
	 * </p>
	 * 
	 * <pre>
	 * match $query like "@{rootUID}";
	 * 	(...)
	 * </pre>
	 * <p>
	 * Then '@{rootUID}' will be substituted with {@link Properties#get(Object)}
	 * with 'rootUID' as the key.
	 * </p>
	 * 
	 * @param template   template of TypeQL which may optionally contain tags
	 *                   starting from '@{' and ending with '}'. These tags will be
	 *                   substituted with values in a {@link Properties} object.
	 * @param properties : properties storing the values to be used when a tag like
	 *                   "@{key}" is found in the template.
	 * 
	 * @return template with the tags/annotations filled.
	 * 
	 * @see #getRootUID();
	 * @see #getRootQueryTemplate()
	 * @see #saveBPMN(OutputStream)
	 */
	protected String getQuery(String template, Properties properties) {

		// split the template where "@{key}" occurs
		// so that we can substitute the keys with its vales
		// whenever we find a "@{key}".
		String[] split = template.split("@\\{");
		// split will start with "key}"

		// re-join the string, but substitute "key}" with respective value
		StringBuilder join = new StringBuilder();
		for (String part : split) {
			// part supposedly starts with "key}"
			// extract the key
			int keyEndIndex = part.indexOf('}');
			if (keyEndIndex > 0) {
				String key = part.substring(0, keyEndIndex);
				// obtain the value from attributes in this class.
				Object value = properties.get(key);
				if (value == null) {
					throw new IllegalArgumentException(
							"Key '" + key + "' was not found in the properties: " + properties);
				}
				// append the value
				join.append(value);
				// and then what's after '}'
				join.append(part.substring(keyEndIndex + 1));
			} else {
				// the template did not have occurrence of key
				// just append as-is.
				join.append(part);
			}
		} // end of iteration on parts of the template

		return join.toString();
	}

	/**
	 * @return a property object pre-filled with attributes in this class. Default
	 *         values can be specified in application.properties.
	 * 
	 * @see ApplicationProperties
	 */
	protected Properties getQueryPropertiesFromFields() {

		// the properties to return
		Properties properties = new Properties(
				// read defaults from application.properties
				ApplicationProperties.getInstance());

		logger.debug("Retrieving field names and values...");
		for (Field field : this.getClass().getFields()) {
			try {
				Object value = field.get(this);
				if (value != null) {
					logger.debug("Adding value {} from field {}.", value, field);
					properties.put(field.getName(), value);
				}
			} catch (IllegalArgumentException | IllegalAccessException e) {
				logger.warn("Failed obtain the value of the field '{}'", field, e);
			}
		}

		logger.debug("Also retrieving keys and values from simple getters with no arguments...");
		for (Method method : this.getClass().getMethods()) {

			// getter methods should have names starting with "get"
			if (!method.getName().startsWith("get")
					// simple getters should not have arguments
					|| method.getParameterCount() > 0) {
				// skip because this is not a getter
				continue;
			}

			try {
				// retrieve the value
				Object value = method.invoke(this);
				if (value != null) {

					// Remove the "get" from the name
					String key = method.getName().substring(3);
					// support both capitalized key and uncapitalized keys
					String uncapitalizedKey = StringUtils.uncapitalize(key);

					logger.debug("Adding property '{}={}' and '{}={}' from getter {}.", key, value, uncapitalizedKey,
							value, method);
					properties.put(key, value);
					properties.put(uncapitalizedKey, value);

				}
			} catch (IllegalAccessException | IllegalArgumentException | InvocationTargetException e) {
				logger.warn("Failed to invoke getter '{}'", method, e);
			}

		} // end of iteration on methods

		return properties;
	}

	/**
	 * @return address of TypeDB (e.g., "localhost:1729").
	 */
	public String getTypeDBAddress() {
		return typeDBAddress;
	}

	/**
	 * @param address : address of TypeDB (e.g., "localhost:1729").
	 */
	public void setTypeDBAddress(String address) {
		this.typeDBAddress = address;
	}

	/**
	 * @return name of the database in TypeDB to access.
	 */
	public String getDatabaseName() {
		return databaseName;
	}

	/**
	 * @param databaseName : name of the database in TypeDB to access.
	 */
	public void setDatabaseName(String databaseName) {
		this.databaseName = databaseName;
	}

	/**
	 * @return the uid attribute to query in the TypeDB database to retrieve the
	 *         root of the BPMN model. Regular expression is supported.
	 */
	public String getRootUID() {
		return rootUID;
	}

	/**
	 * @param uid : the uid attribute to query in the TypeDB database to retrieve
	 *            the root of the BPMN model. Regular expression is supported.
	 */
	public void setRootUID(String uid) {
		this.rootUID = uid;
	}

	/**
	 * @return template of TypeQL to be used to retrieve the root BPMN object.
	 *         Annotated keywords between "@{" and "}" will be retrieved from
	 *         attributes in this class. (see application.properties).
	 * 
	 * @see #getRootUID()
	 * @see #getQuery(String, Properties)
	 */
	public String getRootQueryTemplate() {
		return rootQueryTemplate;
	}

	/**
	 * @param template : template of TypeQL to be used to retrieve the root BPMN
	 *                 object. Annotated keywords between "@{" and "}" will be
	 *                 retrieved from attributes in this class. (see
	 *                 application.properties).
	 * 
	 * @see #getRootUID()
	 * @see #getQuery(String, Properties)
	 */
	public void setRootQueryTemplate(String template) {
		this.rootQueryTemplate = template;
	}

	/**
	 * @return the parentUID
	 */
	public String getParentUID() {
		return parentUID;
	}

	/**
	 * @param parentUID the parentUID to set
	 */
	public void setParentUID(String parentUID) {
		this.parentUID = parentUID;
	}

	/**
	 * @return template of TypeQL to be used to retrieve the children of a BPMN
	 *         object identified by its UID. Annotated keywords between "@{" and "}"
	 *         will be retrieved from attributes in this class. (see
	 *         application.properties).
	 * 
	 * @see #getParentUID()
	 * @see #getQuery(String, Properties)
	 */
	public String getChildQueryTemplate() {
		return childQueryTemplate;
	}

	/**
	 * @param template : template of TypeQL to be used to retrieve the children of a
	 *                 BPMN object identified by its UID. Annotated keywords between
	 *                 "@{" and "}" will be retrieved from attributes in this class.
	 *                 (see application.properties).
	 * 
	 * @see #getParentUID()
	 * @see #getQuery(String, Properties)
	 */
	public void setChildQueryTemplate(String template) {
		this.childQueryTemplate = template;
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
	 * @return if true, a sanity check will be executed at the end of
	 *         {@link #saveBPMN(OutputStream)}
	 */
	public boolean isRunSanityCheck() {
		return runSanityCheck;
	}

	/**
	 * @param run : if true, a sanity check will be executed at the end of
	 *            {@link #saveBPMN(OutputStream)}
	 */
	public void setRunSanityCheck(boolean run) {
		this.runSanityCheck = run;
	}

	/**
	 * @return Name of the @{key} to hold the UID of parent node in the template at
	 *         {@link #getChildQueryTemplate()}.
	 */
	public String getParentUIDAttributeName() {
		return parentUIDAttributeName;
	}

	/**
	 * @param key : Name of the @{key} to hold the UID of parent node in the
	 *            template at {@link #getChildQueryTemplate()}.
	 */
	public void setParentUIDAttributeName(String key) {
		this.parentUIDAttributeName = key;
	}

}
