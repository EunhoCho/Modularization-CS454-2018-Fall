import sys
import DotParser
import Node
from WCA import WCA

# read .gv file(dot) and create graphs
dot_file = DotParser.read_and_render('test/all.gv')
print(dot_file.source)

# get edge information and parse it
edges = DotParser.parser(dot_file, "->")  # second argument should be "--" or "->" (depends on .dot file format)
print(edges)

# make nodes as a list of node classes
nodes = Node.make_nodes(edges)

# make dependency graph
MDG = Node.make_dependency_graph(edges, nodes)

# get feature vector using MDG
for i in range(len(nodes)):
    nodes[i].set_feature_vector(MDG[i])

if sys.argv[1] == 'WCA':
    WCA.WCA(nodes, edges)