# TypeDB2SBN

Some source code to generate an SBN structure (i.e., input for SBN parameter learning) from DALNIM iMIA knowledge base (stored in TypeDB).

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
