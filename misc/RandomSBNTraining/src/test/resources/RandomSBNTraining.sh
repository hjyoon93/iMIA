#!/bin/sh
java -jar -XX:+UseSerialGC -Xms1G -Xmx16G -verbose:gc -XX:+PrintGCDetails RandomSBNTraining-0.0.1-SNAPSHOT-jar-with-dependencies.jar -n 600 -s 2 -t 15 -d 100

