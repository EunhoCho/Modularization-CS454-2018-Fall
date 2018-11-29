import sys
import DotParser
import HC
import MDG
from WCA import WCA

# read .gv file(dot) and create graphs
dot_file = DotParser.read_and_render('test/all.gv')
print(dot_file.source)

# get edge information and parse it
edges = DotParser.parser(dot_file, "->")  # second argument should be "--" or "->" (depends on .dot file format)
print(edges)

# make dependency graph and set feature vector
targetMDG = MDG.MDG(edges)
targetMDG.set_feature_vector()

modularizeMethod = sys.argv[1]

if modularizeMethod == 'WCA':
    WCA.WCA(targetMDG)
elif modularizeMethod == 'HC':
    HC.HC(targetMDG)
