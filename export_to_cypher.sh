#!/us/bin/sh
# Assumes you have NEO4J_HOME on your path
$NEO4J_HOME/bin/neo4j-shell -c dump > gist/cogat_neo4j_$(date +"%y%m%d_%H%M%S").cypher
