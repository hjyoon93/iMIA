# DALNIM TypeDB to BPMN2 writer

Tool to write BPMN2 files from information queried from a TypeDB database.

See *pom.xml* (the maven configuration file) for details about this project's configuration.

## How to build

1. Download and setup Apache Maven (recommended version 3.8.X) from [https://maven.apache.org/](https://maven.apache.org/).

2. Access (cd) this project's root directory (where the *pom.xml* resides).

3. Run the command below. Make sure you are connected to the Internet because Maven will attempt to automatically download some dependencies. You'll need to use the *-Dmaven.test.skip=true* option if you do not have an instance of TypeDB running in the default port (test units will try to access TypeDB).

				mvn clean package [-Dmaven.test.skip=true]

4. An executable JAR file called *TypeDB2BPMN-<VERSION>-jar-with-dependencies.jar* will be created in the *target* folder. This file can be executed with a Java Runtime Environment (version 11 or newer suggested).
	* Similarly, a source JAR file called *TypeDB2BPMN-<VERSION>-sources.jar* will be created in the *target* folder. This is a standard JAR container with the project's source code. A JAR file is an ordinary ZIP file that can be extracted with any ZIP package extraction tool of your choice.


## How to run

1. Make sure you have a Java Runtime Environment installed (version 11 or above suggested).

2. Run the following command in the console:

				java [-Dlog4j.configurationFile=log4j2.xml] -jar TypeDB2BPMN-<VERSION>-jar-with-dependencies.jar [COMMAND LINE ARGUMENTS]

### Command line arguments
				
	 	--help,		-h :	Prints this help. See application.properties for more configurable parameters.
	 	--url,		-u :	Address of TypeDB. Default is "localhost:1729"
	 	--database,	-d :	Name of database in TypeDB to open a session. Default is "BPMN"
	 	--uid,		-i :	UID of BPMN project to query (regex supported). E.g., "https://camunda.org/examples/#.*"
	 	--output,	-o :	The output BPMN file. Default is "output.bpmn"
