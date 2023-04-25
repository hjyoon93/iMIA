::@echo off
setlocal enableDelayedExpansion
for /R repository\ %%A in (*.pom) do (
  mvn install:install-file -Dpackaging=jar -Dfile="%%~pnA.jar" -DpomFile="%%A"
)