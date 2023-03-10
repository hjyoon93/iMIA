# TypeDB2SBN

This is some source code to generate an SBN structure (i.e., input for SBN parameter learning) from DALNIM iMIA knowledge base (stored in TypeDB).
It can be used to write Hugin .NET files from information queried from a TypeDB database.

See *pom.xml* (the maven configuration file) for details about this project's configuration.

Basically, this tool will look for instances of some special classes/relations in the TypeDB knowledge base and interpret them as nodes or arcs in the SBN.
Please, find the [DALNIM concept model](https://github.com/cardialfly/DALNIM/blob/main/Final_Concept_Model_Version3.pdf) (../Final_Concept_Model_Version3.pdf) for the available classes.

The resulting SBN will be stored in Hugin NET format, which can be opened and managed with [UnBBayes-SBN](https://sourceforge.net/p/unbbayes/code/HEAD/tree/trunk/unbbayes.prs.sbn/) (see <https://sourceforge.net/p/unbbayes/code/HEAD/tree/trunk/unbbayes.prs.sbn/>).


## Translation rules

The following list summarizes what classes/relations in the DALNIM concept model (in TypeDB) shall be interpreted as nodes or arcs in the SBN:

+ Classes that shall be interpreted as nodes
    * Mission
    * Task
    * ANDPrecedenceTaskList (shall be interpreted as noisy-and nodes)
    * ORPrecedenceTaskList (shall be interpreted as noisy-or nodes)
    * Performer (including its subclasses, such as Service and Asset).

+ Classes/relations that shall be interpreted as arcs/edges:
    * PrecedenceTask (if not ANDPrecedenceTaskList nor ORPrecedenceTaskList)
        - isCompoundBySetOfTask shall point to the parent node
        - inverse of isPrecededBySetOfTask shall point to the child node
    * inverse of isCompoundBy
    * inverse of isPerformedBy
    * provides

    
## How to build

1. Download and setup Apache Maven (recommended version 3.8.X) from [https://maven.apache.org/](https://maven.apache.org/).

2. Access (cd) this project's root directory (where the *pom.xml* resides).

3. Run the command below. Make sure you are connected to the Internet because Maven will attempt to automatically download some dependencies. You'll need to use the *-Dmaven.test.skip=true* option if you do not have an instance of TypeDB running in the default port (test units will try to access TypeDB).

				mvn clean package [-Dmaven.test.skip=true]

4. An executable JAR file called *TypeDB2SBN-<VERSION>-jar-with-dependencies.jar* will be created in the *target* folder. This file can be executed with a Java Runtime Environment (version 11 or newer suggested).
	* Similarly, a source JAR file called *TypeDB2SBN-<VERSION>-sources.jar* will be created in the *target* folder. This is a standard JAR container with the project's source code. A JAR file is an ordinary ZIP file that can be extracted with any ZIP package extraction tool of your choice.


## How to run

1. Make sure you have a Java Runtime Environment installed (version 11 or above suggested).

2. Run the following command in the console:

				java [-Dlog4j.configurationFile=log4j2.xml] -jar TypeDB2SBN-<VERSION>-jar-with-dependencies.jar [COMMAND LINE ARGUMENTS]

### Command line arguments
				
	 	--help,		-h :	Prints this help. See application.properties for more configurable parameters.
	 	--url,		-u :	Address of TypeDB. Default is "localhost:1729"
	 	--database,	-d :	Name of database in TypeDB to open a session. Default is "BPMN"
	 	--uid,		-i :	UID of concept model element to query (regex supported). E.g., "https://camunda.org/examples/#.*"
	 	--output,	-o :	The output NET file. Default is "structure.net"