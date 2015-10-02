from py2neo import Graph, Path, Node,Rel
import os


basedir='/Users/poldrack/code/cogat-neo4j'

# load concepts

f=open(os.path.join(basedir,'Dump_concept_2015-10-01_560d3c1a886ef.csv'))
hdr=f.readline()
concept_lines=[i.strip().replace('"','').split(';') for i in f.readlines()]
f.close()
concept_id=[]
for l in concept_lines:
    concept_id.append(l[2].split('/')[-1])

f=open(os.path.join(basedir,'Dump_task_2015-10-01_560d3c2116654.csv'))
hdr=f.readline()
task_lines=[i.strip().replace('"','').split(';') for i in f.readlines()]
f.close()
task_id=[]
for l in task_lines:
    task_id.append(l[2].split('/')[-1])

f=open(os.path.join(basedir,'Dump_contrast_2015-10-01_560d3c2731758.csv'))
hdr=f.readline()
contrast_lines=[i.strip().replace('"','').split(';') for i in f.readlines()]
f.close()
contrast_id=[]
for l in contrast_lines:
    contrast_id.append(l[0].split('/')[-1])

# set up authentication parameters
#authenticate("localhost:7474", "arthur", "excalibur")

# connect to authenticated graph database
graph = Graph()

tx = graph.cypher.begin()
conceptnodes={}
tasknodes={}
contrastnodes={}
ctr=1

for i in range(len(concept_id)):

    #tx.append('CREATE (%s:Concept {name: "%s", id:"%s"}) RETURN %s'%(concept_id[i],
    #    concept_lines[i][0],concept_id[i],concept_id[i]))
    if graph.find_one('Concept',property_key='id', property_value=concept_id[i]) == None:
        conceptnode= Node("Concept", name=concept_lines[i][0],
                                    id=concept_id[i])
        graph.create(conceptnode)


for i in range(len(task_id)):

    #tx.append('CREATE (%s:Task {name: "%s", id:"%s"}) RETURN %s'%(task_id[i],
    #    task_lines[i][0],task_id[i],task_id[i]))
    if graph.find_one('Task',property_key='id', property_value=task_id[i]) == None:
        tasknode= Node("Task", name=task_lines[i][0],id=task_id[i])
        graph.create(tasknode)



for i in range(len(contrast_lines)):
    tasknode=graph.find_one('Task',property_key='id', property_value=contrast_lines[i][2])
    if not tasknode==None:
        path = Path(tasknode,
                    Rel("HASCONTRAST"),
                    Node("Contrast", name=contrast_lines[i][3],id=contrast_id[i]))
        graph.create(path)
    else:
        print 'problem with',contrast_lines[i]



f=open(os.path.join(basedir,'Dump_assertion_2015-10-01_560d3c2dafcea.csv'))
hdr=f.readline()
assertion_lines=[i.strip().replace('"','').split(';') for i in f.readlines()]
f.close()
for i in range(len(assertion_lines)):
    if not assertion_lines[i][5]=="concept-task":
        continue

    conceptnode=graph.find_one('Concept',property_key='id',
                            property_value=assertion_lines[i][2])
    contrastnode=graph.find_one('Contrast',property_key='id',
                                property_value=assertion_lines[i][10])
    goodnodes=True
    if  contrastnode==None:
        print i,'problem with contrast node',assertion_lines[i][10]
        print assertion_lines[i]
        print
        goodnodes=False

    elif conceptnode==None:
        print i,'problem with concept node',assertion_lines[i][2]
        print assertion_lines[i]
        print
        goodnodes=False

    if goodnodes:
        #print 'creating %s->%s'%(assertion_lines[i][2],assertion_lines[i][10])
        path=Path(conceptnode,Rel("MEASUREDBY"),contrastnode)
        graph.create(path)

#friends = Path(alice, "KNOWS", bob, "KNOWS", carol)

#graph.create(friends)
