#!/bin/sh
java -jar -XX:+UseSerialGC -Xms1G -Xmx16G RandomSBNTraining-0.0.1-SNAPSHOT-jar-with-dependencies -verbose:gc -XX:+PrintGCDetails

