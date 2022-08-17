# DALNIM BPMN2 to TypeQL converter

Tool to convert BPMN2 files to TypeQL insert scripts, or to load BPMN processes from TypeDB.

See *pom.xml* (the maven configuration file) for details about this project's configuration.

## How to build

1. Download and setup Apache Maven (recommended version 3.8.X) from [https://maven.apache.org/](https://maven.apache.org/).

2. Access (cd) this project's root directory (where the *pom.xml* resides).

3. Run the command below. Make sure you are connected to the Internet because Maven will attempt to automatically download some dependencies.

				mvn clean package

4. An executable JAR file called *BPMN2TypeDB-<VERSION>-jar-with-dependencies.jar* will be created in the *target* folder. This file can be executed with a Java Runtime Environment (version 11 or newer suggested).
	* Similarly, a source JAR file called *BPMN2TypeDB-<VERSION>-sources.jar* will be created in the *target* folder. This is a standard JAR container with the project's source code. A JAR file is an ordinary ZIP file that can be extracted with any ZIP package extraction tool of your choice.


## How to run

1. Make sure you have a Java Runtime Environment installed (version 11 or above suggested).

2. Run the following command in the console:

				java [-Dlog4j.configurationFile=log4j2.xml] -jar BPMN2TypeDB-<VERSION>-jar-with-dependencies.jar [COMMAND LINE ARGUMENTS]

### Command line arguments
				
				 --help,  -h :	Prints this help. See application.properties for more configurable parameters.
				 
				 --input, -i :	The input BPMN file. 
				 					Will be ignored if "--url" is present.
				 					Default is "input.bpmn"
				 
				 --output, -o :	Output directory. 
				 					If running with "--url", then this program will output a BPMN file read from TypeDB.
				 					If not running with "--url", then this will be the folder to write 
				 					TypeQL schema (schema.tql) and data (data.tql).
				 					Default is "./output/"
