# cogat-neo4j

Testing the Cognitive Atlas as a [neo4j graph](http://neo4j.com/)

#### 1. Download neo4j
the community edition of [neo4j](http://neo4j.com/download/). On linux this means extracting the binary to somewhere on your computer:


      cd $HOME/Downloads
      mv neo4j-community-2.2.5-unix.tar.gz $HOME/Packages/
      tar -xzvf neo4j-community-2.2.5-unix.tar.gz 
      rm neo4j-community-2.2.5-unix.tar.gz 

#### 2. Add to path 
To add to your path:

      vim ~/.bashrc
      export PATH=$PATH:/home/vanessa/Packages/neo4j-community-2.2.5/bin
      source ~/.bashrc
      which neo4j
      /home/vanessa/Packages/neo4j-community-2.2.5/bin/neo4j

Then start the server

      neo4j start

Open browser to [http://localhost:7474/](http://localhost:7474/) to see the server running.

#### 3. Download 
Set a new password

You will see a login screen, and instructions to log in with the old password, "neo4j." Log in and you will be prompted to set a new password. Don't forget it, you will need it to test the script.

#### 4. Download 
Make sure you have the [cognitive atlas python API](https://cogat-python.readthedocs.org/en/latest/getting_started.html#installation) wrapper installed. Also install `py2neo`, which is the module for working with neo4j from Python.


      pip install py2neo --user


#### 5. Authenticate
Next, go through the lines of the script [mk_cogat_neo4j.py](mk_cogat_neo4j.py). When it gets to the line:

      authenticate("localhost:7474", "neo4j", "neo4j")

this is where you will need to change your password to the one you just set. The authentication doesn't happen at this step, it will happen when you try to make the graph:

      graph = Graph()

so if there are authentication errors you will see them at this time point.

You should be able to run through the code, and see that the interface updates. The Cognitive Atlas API python wrapper spits out a lot of text, so be prepared for that. If the interface in the web browser doesn't update, click the circles in the left bar to see your graph nodes (or click monitor) and in the bottom right of the box that shows your graph (db/data) statistics, click the slider that says "auto refresh." Note that if you need to wipe the entire thing any time, just rm -rf db/data.

#### Exploration needed

The work has only been done to set up the skeleton for a graph! We want to know if Cognitive Atlas would be good to have in neo4j, so these are the questions we want to explore with this test:

- what kind of queries would I run, and what do they look like in neo4j?
- how easy/hard is it to add/delete/modify the graph?
- how easy is it to visualize the graph, or integrate into a web project?
- what about an API?
