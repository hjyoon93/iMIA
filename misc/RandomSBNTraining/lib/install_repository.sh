#!/bin/bash
for file in $(find repository/ -type f -name '*.pom'); do mvn install:install-file -Dpackaging=jar -Dfile="${file/%.pom/.jar}" -DpomFile="$file"; done