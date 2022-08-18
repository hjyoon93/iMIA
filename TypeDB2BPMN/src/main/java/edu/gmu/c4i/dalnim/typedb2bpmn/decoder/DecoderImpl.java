package edu.gmu.c4i.dalnim.typedb2bpmn.decoder;

import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.Properties;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import org.apache.commons.lang3.StringUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import com.vaticle.typedb.client.TypeDB;
import com.vaticle.typedb.client.api.TypeDBClient;
import com.vaticle.typedb.client.api.TypeDBOptions;
import com.vaticle.typedb.client.api.TypeDBSession;
import com.vaticle.typedb.client.api.TypeDBTransaction;
import com.vaticle.typedb.client.api.answer.ConceptMap;

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

	private String parentUID = rootUID;

	// TODO substitute entity/relation names with "@{key}" tags
	private String rootQueryTemplate = "## Query BPMN root by regex on UID (regex matches BPMN definitions or Mission in concept model)\n"
			+ "match\n" + "$query like \"@{rootUID}\";\n"
			+ "$bpmnroot isa BPMN_definitions, has uid $uid_b, has attribute $attrib;\n"
			+ "$mission isa Mission, has uid $uid_m;\n" + "{ $uid_m = $query; } or {  $uid_b = $query ;};\n"
			+ "(bpmnEntity: $bpmnroot, conceptualModel: $mission) isa BPMN_hasConceptualModelElement;\n"
			+ "get $bpmnroot, $attrib;";

	// TODO substitute entity/relation names with "@{key}" tags
	private String childQueryTemplate = "## query BPMN child and its attributes\n" + "match\n"
			+ "$parent has uid \"@{parentUID}\";\n" + "$child isa BPMN_Entity, has attribute $attrib;\n"
			+ "(parent: $parent, child: $child) isa BPMN_hasChildTag;\n" + "get $child, $attrib;";

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

		// option to enable inference
		TypeDBOptions infer = TypeDBOptions.core().infer(true);

		// obtains a property object pre-filled with attributes in this class.
		Properties properties = this.getPropertiesFromFields();

		// Prepare a query the root BPMN tag (aka 'definitions')
		String rootQuery = getQuery(getRootQueryTemplate(), properties);

		// start a session to query the database
		String database = getDatabaseName();
		logger.info("Creating a session to database '{}'", database);
		try (TypeDBSession session = client.session(database, TypeDBSession.Type.DATA, infer)) {

			// prepare writer for output stream
			try (PrintWriter writer = new PrintWriter(outputStream)) {

				// Run a transaction to extract the BPMN 'definitions' node from the answer
				try (TypeDBTransaction readTransaction = session.transaction(TypeDBTransaction.Type.READ, infer)) {
					Stream<ConceptMap> answers = readTransaction.query().match(rootQuery);
					for (ConceptMap conceptMap : answers.collect(Collectors.toList())) {
						// TODO extract the definitions tag and its attributes

					}
				}

				// TODO recursively access children

			}

		}

		// make sure to close the connection to TypeDB
		logger.debug("Closing connection to TypeDB: {}", client);
		client.close();

		throw new UnsupportedOperationException("Not finished yet");
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
	protected Properties getPropertiesFromFields() {

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

}
