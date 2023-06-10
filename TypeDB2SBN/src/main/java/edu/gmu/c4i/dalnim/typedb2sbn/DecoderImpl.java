package edu.gmu.c4i.dalnim.typedb2sbn;

import java.io.File;
import java.io.IOException;
import java.net.URI;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.Properties;
import java.util.stream.Collectors;

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

import unbbayes.io.BaseIO;
import unbbayes.io.CountCompatibleNetIO;
import unbbayes.prs.Edge;
import unbbayes.prs.Node;
import unbbayes.prs.bn.ProbabilisticNetwork;
import unbbayes.prs.bn.ProbabilisticNode;
import unbbayes.prs.bn.cpt.impl.UniformTableFunction;
import unbbayes.prs.exception.InvalidParentException;

/**
 * Default implementation of {@link Decoder} that reads a BPMN project from
 * TypeDB database and saves the content to a BPMN2 file format.
 * 
 * @author shou
 */
public class DecoderImpl implements Decoder {

	private static Logger logger = LoggerFactory.getLogger(DecoderImpl.class);

	private String typeDBAddress = "localhost:1729";

	private String databaseName = "demo";

	private String rootUID = ".*";

	private String uidAttributeName = "UID";

	private BaseIO netIO = new CountCompatibleNetIO();

	private String nodeQuery = "match" + "$entity isa $type, has UID $uid;" + "{$type sub ANDPrecedenceTaskList;}"
			+ "or {$type sub ORPrecedenceTaskList;}" + "or {$type sub Task;}" + "or {$type sub Performer;};"
			+ "get $entity,$uid;";

	private String edgeQuery = "match \n" + "    $child isa $childType, has UID $cuid;\n"
			+ "    $parent isa $parentType, has UID $puid;\n" + "    $cuid = \"@{UID}\" ;\n" + "    {\n"
			+ "        # Parents from PrecedenceTask\n" + "        $childType sub Task;\n"
			+ "        $parentType sub Task;\n" + "        $precedence isa! PrecedenceTask;\n"
			+ "        (precedence_task: $precedence, task: $child) isa isPrecededBySetOfTask;\n"
			+ "        (precedence_task: $precedence, task: $parent) isa isCompoundBySetOfTask;\n" + "    } or {\n"
			+ "        #  Parents that are AND/OR PrecedenceTask\n" + "        $childType sub Task;\n"
			+ "        {$parentType sub ANDPrecedenceTaskList;} \n"
			+ "            or {$parentType sub ORPrecedenceTaskList;};\n"
			+ "        (precedence_task: $parent, task: $child) isa isPrecededBySetOfTask;\n" + "    } or {\n"
			+ "        #  Parents of AND/OR PrecedenceTask\n" + "        $parentType sub Task;\n"
			+ "        {$childType sub ANDPrecedenceTaskList;} \n"
			+ "            or {$childType sub ORPrecedenceTaskList;};\n"
			+ "        (precedence_task: $child, task: $parent) isa isCompoundBySetOfTask;\n" + "    } or {\n"
			+ "        # Parents from isPerformedBy\n" + "        $childType sub Task;\n"
			+ "        $parentType sub Performer;\n" + "        (performer: $parent, task: $child) isa isPerformedBy;\n"
			+ "    } or {\n" + "        # Parents from provides\n" + "        $childType sub Service;\n"
			+ "        $parentType sub Asset;\n" + "        (asset: $parent, service: $child) isa provides;\n"
			+ "    };\n" + "get $parent, $puid;";
	

	private String descriptionQuery = "match\n"
			+ "    $entity isa $MIAEntity, has UID $uid;\n"
			+ "    $bpmnEntity isa $BPMN_Entity, has BPMNattrib_name $name;\n"
			+ "    $uid = \"@{UID}\";\n"
			+ "    (bpmnEntity: $bpmnEntity, conceptualModel: $entity) isa BPMN_hasConceptualModelElement;\n"
			+ "get $name;";

	private boolean isFillUniformCPT = true;
	
	private int nodePositionXGap = 280;
	
	private int nodePositionYGap = 120;

	private String nameAttributeName = "BPMNattrib_name";


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

		// add any initialization code here
		return new DecoderImpl();
	}

	/**
	 * Query the concepts in TypeDB Knowledge base that represent nodes in semantic
	 * network model, then also queries the concepts/relations that represents the
	 * edges in the network model, and finally saves the network model. Sample
	 * queries:
	 * 
	 * <pre>
	# all node-like entities
	match
	$entity isa $type, has UID $uid;
	{$type sub ANDPrecedenceTaskList;}
	    or {$type sub ORPrecedenceTaskList;}
	    or {$type sub Mission;}
	    or {$type sub Task;}
	    or {$type sub Performer;};
	get $entity,$uid;
	 * </pre>
	 * 
	 * <pre>
	# Parents of a given node
	match 
	$child isa $childType, has UID $cuid;
	$parent isa $parentType, has UID $puid;
	$cuid = "http://bpmn.io/schema/bpmn/#Task_Activity_1mizk6r" ;
	{
	    # Parents from PrecedenceTask
	    $childType sub Task;
	    $parentType sub Task;
	    $precedence isa! PrecedenceTask;
	    (precedence_task: $precedence, task: $child) isa isPrecededBySetOfTask;
	    (precedence_task: $precedence, task: $parent) isa isCompoundBySetOfTask;
	} or {
	    #  Parents that are AND/OR PrecedenceTask
	    $childType sub Task;
	    {$parentType sub ANDPrecedenceTaskList;} 
	        or {$parentType sub ORPrecedenceTaskList;};
	    (precedence_task: $parent, task: $child) isa isPrecededBySetOfTask;
	} or {
	    #  Parents of AND/OR PrecedenceTask
	    $parentType sub Task;
	    {$childType sub ANDPrecedenceTaskList;} 
	        or {$childType sub ORPrecedenceTaskList;};
	    (precedence_task: $child, task: $parent) isa isCompoundBySetOfTask;
	} or {
	    # Parents from isPerformedBy
	    $childType sub Task;
	    $parentType sub Performer;
	    (performer: $parent, task: $child) isa isPerformedBy;
	} or {
	    # Parents from provides
	    $childType sub Service;
	    $parentType sub Asset;
	    (asset: $parent, service: $child) isa provides;
	};
	get $parent, $puid;
	 * </pre>
	 * 
	 * 
	 * @see #getNetIO()
	 */
	@Override
	public void saveSBNFile(File outputFile) throws IOException {

		String dbAddress = getTypeDBAddress();
		logger.info("Starting a connection to TypeDB at {}", dbAddress);
		TypeDBClient client = TypeDB.coreClient(dbAddress);
		logger.debug("Created connection to TypeDB: {}", client);

		// the database name to query
		String database = getDatabaseName();

		// prepare the network model to write
		ProbabilisticNetwork net = new ProbabilisticNetwork(database + System.currentTimeMillis());

		// ensure there is a mission node
		ProbabilisticNode missionNode = new ProbabilisticNode();
		missionNode.setName("Mission");
		missionNode.setDescription("Mission goal achievement");
		// make sure the nodes are boolean (2 states)
		missionNode.removeAllStates();
		for (int i = 0; missionNode.getStatesSize() < 2; i++) {
			missionNode.appendState("state" + i);
		}
		missionNode.setStateAt("false", 0);
		missionNode.setStateAt("true", 1);
		missionNode.getProbabilityFunction().addVariable(missionNode);

		net.addNode(missionNode);

		// option to turn inference mode on
		TypeDBOptions inferOption = TypeDBOptions.core().infer(true);

		// start a session to query the database
		logger.info("Creating a session to database '{}'", database);
		try (TypeDBSession session = client.session(database, TypeDBSession.Type.DATA,
				// enable inference mode
				inferOption)) {

			// Run a transaction to extract the concepts that represent nodes
			Map<String, Entity> uidToEntityMap = new HashMap<>();
			Map<String, ProbabilisticNode> uidToNodeMap = new HashMap<>();
			try (TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.READ,
					// enable inference mode
					inferOption)) {

				// Run query.
				List<ConceptMap> queryResponse = transaction.query().match(nodeQuery).collect(Collectors.toList());

				// retrieve all entities
				List<Entity> nodeEntities = queryResponse.stream().flatMap(map -> map.concepts().stream())
						// iterate on entities only
						.filter(Concept::isEntity).map(Concept::asEntity).distinct().collect(Collectors.toList());

				// create the nodes
				for (Entity nodeEntity : nodeEntities) {

					logger.debug("Creating node associated with entity {}", nodeEntity);

					// obtain the UID
					String uid = retrieveUID(nodeEntity, queryResponse);
					uidToEntityMap.put(uid, nodeEntity);

					// generate node name (ID)
					String nodeName = "";
					// append the fragment of URI
					try {
						URI uri = URI.create(uid);
						String fragment = uri.getFragment();
						if (fragment.isEmpty()) {
							fragment = uri.getPath().replaceAll("[\\s,:.;/\\\\]+", "_");
						}
						nodeName = fragment;
					} catch (Exception e) {
						logger.warn(
								"Failed to extract fragment of UID '{}'. Appending a number to node name instead... ",
								uid);
						nodeName = nodeEntity.getType().getLabel().name() + net.getNodeCount();
					}

					// obtain the BPMN node's name (i.e., short textual description).
					String description = retrieveDescription(uid, transaction);
					if (description == null || description.trim().isEmpty()) {
						// use the ID if name was not found...
						logger.warn("No description/name found for BPMN entity {}. Using ID {} by default...",
								nodeEntity, nodeName);
						description = nodeName;
					}

					// create a BN node accordingly
					ProbabilisticNode node = new ProbabilisticNode();
					node.setName(nodeName);
					node.setDescription(description);
					// make sure the nodes are boolean (2 states)
					node.removeAllStates();
					for (int i = 0; node.getStatesSize() < 2; i++) {
						node.appendState("state" + i);
					}
					node.setStateAt("false", 0);
					node.setStateAt("true", 1);
					node.getProbabilityFunction().addVariable(node);

					// add the node to the network
					net.addNode(node);
					uidToNodeMap.put(uid, node);

				} // end of iteration on nodes

			} // end of TypeDB transaction for nodes

			logger.info("Finished creating nodes");

			// create the edges related to parents of each node
			for (Entry<String, Entity> childEntityEntry : uidToEntityMap.entrySet()) {

				// resolve query template for edges
				Properties property = new Properties();
				property.put(getUIDAttributeName(), childEntityEntry.getKey());
				// convert @{UID} to its value
				String parentQuery = resolveQuery(getEdgeQueryTemplate(), property);

				// run another transaction to query edges
				try (TypeDBTransaction transaction = session.transaction(TypeDBTransaction.Type.READ,
						// enable inference mode
						inferOption)) {

					// Run query.
					List<ConceptMap> response = transaction.query().match(parentQuery).collect(Collectors.toList());

					// retrieve all parent entities
					List<Entity> parentEntities = response.stream().flatMap(map -> map.concepts().stream())
							// iterate on entities only
							.filter(Concept::isEntity).map(Concept::asEntity).distinct().collect(Collectors.toList());

					// iterate on retrieved parents
					for (Entity parentEntity : parentEntities) {

						String parentUID = retrieveUID(parentEntity, response);

						logger.debug("Creating edge from '{}' to '{}'", parentEntity, childEntityEntry.getValue());

						// obtain the child node
						ProbabilisticNode child = uidToNodeMap.get(childEntityEntry.getKey());
						if (child == null) {
							logger.warn("Failed to retrieve child node: {}", childEntityEntry);
							continue;
						}

						// obtain the parent node
						ProbabilisticNode parent = uidToNodeMap.get(parentUID);
						if (parent == null) {
							logger.warn("Failed to retrieve parent node: {}", childEntityEntry);
							continue;
						}

						// generate the edge
						try {
							net.addEdge(new Edge(parent, child));
						} catch (InvalidParentException e) {
							logger.warn("Failed to create edge between '{}' and '{}'.", parent, child);
						}

					} // end of iteration on nodes

				} // end of TypeDB transaction for edges

			} // end of iteration on children

		} // end of TypeDB session

		logger.info("Finished creating edges");

		// make sure to close the connection to TypeDB
		logger.debug("Closing connection to TypeDB: {}", client);
		client.close();

		// connect all leaf nodes to the mission node
		for (Node node : net.getNodes()) {
			if (!node.equals(missionNode)
					&& node.getChildNodes().isEmpty()) {
				try {
					net.addEdge(new Edge(node, missionNode));
				} catch (InvalidParentException e) {
					logger.warn("Failed to add edge from leaf node '{}' to the mission node", node);
				}
			}
		}

		if (isFillUniformCPT()) {
			// fill CPTs with uniform distribution
			logger.info("Filling CPT with uniform distribution");
			UniformTableFunction uniform = new UniformTableFunction();
			for (Node node : net.getNodes()) {
				if (node instanceof ProbabilisticNode) {
					uniform.applyFunction(((ProbabilisticNode) node).getProbabilityFunction());
				}
			}
		}

		adjustNodePositions(net);

		// save the model
		logger.info("Saving the model...");
		getNetIO().save(outputFile, net);

	}

	/**
	 * Adjust the position of the nodes by moving all leaf nodes to
	 * the top and their parents down, parents of parents down, and so on.
	 * 
	 * @param net : the net containing the nodes
	 * 
	 * @see Node#setPosition(double, double)
	 */
	public void adjustNodePositions(ProbabilisticNetwork net) {

		Collection<Node> nodesInCurrentLevel = new HashSet<>();

		// move leaves to top
		for (Node node : net.getNodes()) {
			if (node.getChildNodes().isEmpty()) {
				nodesInCurrentLevel.add(node);
			}
		}

		// iterate until we reach root nodes
		for (int row = 1; !nodesInCurrentLevel.isEmpty(); row++) {

			Collection<Node> nodesInNextLevel = new HashSet<>();

			// handle current level
			int column = 1;
			for (Node node : nodesInCurrentLevel) {

				// move the node to current row & column
				node.setPosition(getNodePositionXGap() * (double) column, getNodePositionYGap() * (double) row);

				// next level should contain parents
				nodesInNextLevel.addAll(node.getParents());

				// next iteration will move the node to next available column
				column++;
			}

			// this will be the list in next iteration
			nodesInCurrentLevel = nodesInNextLevel;
		}
	}

	/**
	 * @param typeDBEntity  : the entity with UID
	 * @param queryResponse : the response where the entity resides
	 * @return the UID of the TypeDB entity
	 */
	protected String retrieveUID(Entity typeDBEntity, List<ConceptMap> queryResponse) {

		// extract the attributes associated with current entity
		Collection<Attribute<?>> attributes = queryResponse.stream()
				// only consider those related to the current entity
				.filter(map -> map.concepts().contains(typeDBEntity)).flatMap(map -> map.concepts().stream())
				// convert to attributes
				.filter(Concept::isAttribute).map(Concept::asAttribute).distinct().collect(Collectors.toList());

		// Keep track of the uid.
		// access the attributes.
		for (Attribute<?> attrib : attributes) {

			String attribName = attrib.getType().getLabel().name();
			String attribValue = attrib.asString().getValue();

			// handle some special attributes
			if (attribName.equals(getUIDAttributeName())) {
				logger.debug("uid of entity {} is {}", typeDBEntity, attribValue);
				return attribValue;
			}
		} // end of iteration on attributes

		return null;
	}

	/**
	 * @param uid  : the entity's UID
	 * @param transaction : access point to TypeDB query
	 * @return the "name" attribute of the TypeDB entity
	 */
	protected String retrieveDescription(String uid, TypeDBTransaction transaction) {

		// resolve key placeholders in query template
		// (e.g., substitute "@{UID}" with uid's value)
		Properties keywords = new Properties();
		keywords.put(getUIDAttributeName(), uid);
		String resolvedDescriptionQuery = this.resolveQuery(getDescriptionQuery(), keywords);

		// Run query.
		List<ConceptMap> queryResponse = transaction.query().match(resolvedDescriptionQuery)
				.collect(Collectors.toList());

		// extract the attributes associated with current entity
		Collection<Attribute<?>> attributes = queryResponse.stream()
				// convert to attributes
				.flatMap(map -> map.concepts().stream()).filter(Concept::isAttribute).map(Concept::asAttribute)
				.distinct().collect(Collectors.toList());

		// access the attribute
		for (Attribute<?> attrib : attributes) {

			String attribName = attrib.getType().getLabel().name();
			String attribValue = attrib.asString().getValue();

			// extract the "name" attribute
			if (attribName.equals(getNameAttributeName())) {
				logger.debug("Name of entity {} is {}", uid, attribValue);
				return attribValue;
			}
		} // end of iteration on attributes

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
	 * match $query like "@{UID}";
	 * 	(...)
	 * </pre>
	 * <p>
	 * Then '@{UID}' will be substituted with {@link Properties#get(Object)} with
	 * 'UID' as the key.
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
	 * @see #getEdgeQueryTemplate()
	 */
	protected String resolveQuery(String template, Properties properties) {

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
	 * @return address of TypeDB (e.g., "localhost:1729").
	 */
	public String getTypeDBAddress() {
		return typeDBAddress;
	}

	/**
	 * @param address : address of TypeDB (e.g., "localhost:1729").
	 */
	@Override
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
	@Override
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
	@Override
	public void setRootUID(String uid) {
		this.rootUID = uid;
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
	 * @return the netIO
	 */
	public BaseIO getNetIO() {
		if (netIO == null) {
			netIO = new CountCompatibleNetIO();
		}
		return netIO;
	}

	/**
	 * @param netIO the netIO to set
	 */
	public void setNetIO(BaseIO netIO) {
		this.netIO = netIO;
	}

	/**
	 * @return the edgeQuery
	 */
	public String getEdgeQueryTemplate() {
		return edgeQuery;
	}

	/**
	 * @param edgeQuery the edgeQuery to set
	 */
	public void setEdgeQueryTemplate(String edgeQuery) {
		this.edgeQuery = edgeQuery;
	}

	/**
	 * @return the isFillUniformCPT : if true, the CPTs will be filled with uniform
	 *         distribution.
	 * @see #saveSBNFile(File)
	 */
	public boolean isFillUniformCPT() {
		return isFillUniformCPT;
	}

	/**
	 * @param isFillUniformCPT : if true, the CPTs will be filled with uniform
	 *                         distribution.
	 * @see #saveSBNFile(File)
	 */
	public void setFillUniformCPT(boolean isFillUniformCPT) {
		this.isFillUniformCPT = isFillUniformCPT;
	}

	/**
	 * @return the nodePositionXGap
	 */
	public int getNodePositionXGap() {
		return nodePositionXGap;
	}

	/**
	 * @param nodePositionXGap the nodePositionXGap to set
	 */
	public void setNodePositionXGap(int nodePositionXGap) {
		this.nodePositionXGap = nodePositionXGap;
	}

	/**
	 * @return the nodePositionYGap
	 */
	public int getNodePositionYGap() {
		return nodePositionYGap;
	}

	/**
	 * @param nodePositionYGap the nodePositionYGap to set
	 */
	public void setNodePositionYGap(int nodePositionYGap) {
		this.nodePositionYGap = nodePositionYGap;
	}

	/**
	 * @return the "name" attribute of BPMN. Default is "BPMNattrib_name".
	 */
	public String getNameAttributeName() {
		return nameAttributeName;
	}

	/**
	 * @param nameAttributeName : the "name" attribute of BPMN. Default is "name".
	 */
	public void setNameAttributeName(String nameAttributeName) {
		this.nameAttributeName = nameAttributeName;
	}

	/**
	 * @return the query to perform in order to obtain the description of a node
	 *         associated with some UID.
	 * 
	 * @see #retrieveDescription(String, TypeDBTransaction)
	 */
	public String getDescriptionQuery() {
		return descriptionQuery;
	}

	/**
	 * @param descriptionQuery : the query to perform in order to obtain the
	 *                         description of a node associated with some UID.
	 * @see #retrieveDescription(String, TypeDBTransaction)
	 */
	public void setDescriptionQuery(String descriptionQuery) {
		this.descriptionQuery = descriptionQuery;
	}

}
