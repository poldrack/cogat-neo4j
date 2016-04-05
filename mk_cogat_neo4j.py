from cognitiveatlas.api import get_concept, get_task
from py2neo import Graph, Path, Node, Rel, authenticate
import os

# Get concepts, tasks
concepts = get_concept()
concept_ids = concepts.pandas.id.tolist()
concept_names = concepts.pandas.name.tolist()
tasks = get_task()
task_ids = tasks.pandas.id.tolist()
task_names = tasks.pandas.name.tolist()

# get contrasts from tasks
contrast_ids = []
contrast_names = []
contrast_tasks = []
for t in tasks.json:
    task = get_task(id=t["id"])
    contrasts = task.json[0]["contrasts"]
    for contrast in contrasts:
        contrast_tasks.append(t["id"])
        contrast_ids.append(contrast["id"])
        contrast_names.append(contrast["contrast_text"])

# set up authentication parameters
pw=open('neo4j_pw').readline().strip()
authenticate("localhost:7474", "neo4j", pw)

# connect to authenticated graph database
graph = Graph()

tx = graph.cypher.begin()
conceptnodes={}
tasknodes={}
contrastnodes={}

# Create concept nodes
for i in range(len(concept_ids)):
    tx.append('CREATE (%s:concept {name: "%s", id:"%s"}) RETURN %s'%(concept_ids[i],
        concept_names[i],concept_ids[i],concept_ids[i]))
    if graph.find_one('concept',property_key='id', property_value=concept_ids[i]) == None:
        conceptnode= Node("concept",name=concept_names[i],id=concept_ids[i])
        graph.create(conceptnode)

# Create task nodes
for i in range(len(task_ids)):
    tx.append('CREATE (%s:task {name: "%s", id:"%s"}) RETURN %s'%(task_ids[i],
        task_names[i],task_ids[i],task_ids[i]))
    if graph.find_one('task',property_key='id', property_value=task_ids[i]) == None:
        tasknode= Node("task", name=task_names[i],id=task_ids[i])
        graph.create(tasknode)

# Create contrast nodes, associate with task
for i in range(len(contrast_tasks)):
    tasknode=graph.find_one('task',property_key='id', property_value=contrast_tasks[i])
    path = Path(tasknode,Rel("HASCONTRAST"),Node("contrast", name=contrast_names[i],id=contrast_ids[i]))
    graph.create(path)

# from http://stackoverflow.com/questions/26747441/py2neo-how-to-check-if-a-relationship-exists
def create_or_fail(graph_db, start_node, end_node, relationship):
    if len(list(graph_db.match(start_node=start_node, end_node=end_node, rel_type=relationship))) > 0:
        print("Relationship already exists")
        return None
    return graph_db.create((start_node, relationship, end_node))

# Add relationships between concepts
for i in range(len(concepts.json)):
    concept = concepts.json[i]
    if "relationships" in concept:
        for relation in concept["relationships"]:
            # We have assertions for concept ids that don't exist in the atlas [bug]
            if relation["id"] in concept_ids:
                conceptnode1=graph.find_one('concept',property_key='id',property_value=concept["id"])
                conceptnode2=graph.find_one('concept',property_key='id',property_value=relation["id"])
                if relation["direction"] == "parent":
                    if relation["relationship"] == "kind of":
                        path=create_or_fail(graph,conceptnode1,conceptnode2,"ISAKINDOF")
                    else:
                        path=create_or_fail(graph,conceptnode1,conceptnode2,"ISPARTOF")
                elif relation["direction"] == "child":
                    if relation["relationship"] == "kind of":
                        path=create_or_fail(graph,conceptnode2,conceptnode1,"ISAKINDOF")
                    else:
                        path=create_or_fail(graph,conceptnode2,conceptnode1,"ISPARTOF")
                print(conceptnode1,conceptnode2,relation["direction"] )
                #graph.create(path)
            else:
                print("Concept %s is not defined in the Cognitive Atlas, but an assertion exists." %(relation["id"]))

# Add relationships between tasks and contrasts (this may be redundant give above, oh well) :)
for i in range(len(contrast_ids)):
    contrastnode=graph.find_one('contrast',property_key='id',property_value=contrast_ids[i])
    tasknode=graph.find_one('task',property_key='id',property_value=contrast_tasks[i])
    path=Path(tasknode,Rel("HASCONTRAST"),contrastnode)
    graph.create(path)

# Add relationships between contrasts and concepts
# This section will output a lot of text as a separate query is needed to
# get concepts for each contrast
for i in range(len(contrast_ids)):
    # Sometimes the query returns a json object that cannot be decoded
    # It is not clear if this is a connectivity issue or API empty result [bug]
    try:
        contrast_concepts = get_concept(contrast_id=contrast_ids[i]).json
        for cc in contrast_concepts:
            contrastnode=graph.find_one('contrast',property_key='id',property_value=contrast_ids[i])
            conceptnode=graph.find_one('concept',property_key='id',property_value=cc["id"])
            if cc["id"] in concept_ids:
                path=Path(conceptnode,Rel("MEASUREDBY"),contrastnode)
                graph.create(path)
            else:
                print("Contrast %s is not defined in the Cognitive Atlas, but an assertion exists." %(cc["id"]))
    except:
         print("Problem retrieving contrast %s" %(contrast_ids[i]))
