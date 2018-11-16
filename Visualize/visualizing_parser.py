from graphviz import Digraph
from graphviz import Graph
from graphviz import Source
from graphviz import render
from pyparsing import Forward, Word, alphas, alphanums, nums, ZeroOrMore, Literal, Group, QuotedString
import sys
import pydot

#done - read .dot file(.gv)
#done - visualize graph
#done - calculate CF for a module
#plan - apply algorithm and make clusters

""" examples
# make a graph directly
dot = Digraph(comment='The Round Table')
dot  #doctest: +ELLIPSIS
dot.node('A', 'King Arthur')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')

dot.edges(['AB', 'AL'])
dot.edge('B', 'L', constraint='false')
print(dot.source)  # doctest: +NORMALIZE_WHITESPACE

dot.render('test-output/round-table.gv', view=True)  # doctest: +SKIP

# read existing .dot file
print("read from .dot file")
dot2 = Source.from_file('test-output/round-table.gv')
print(dot2.source)

print("read from existing .dot file")
dot3 = Source.from_file('test-output/b.gv')
print(dot3.source)
"""

def read_and_render(filename): #return source
    a = Source.from_file(filename)
    print(a.source)
    a.render(filename, view=True)
    return a

def parse_dot(dot):
    par1 = dot.source.split(";\n")
    par2 = []
    for i in par1:
        for j in i.split(" "):
            par2.append(j)
    return par2
def parse_line(lines):
    #remove "\n"
    result = lines[:]
    num = result.count("")
    for i in range(num):
        result.remove("")
    return result
def get_edges(data,arrow): #arrow = " -- " or " -> "
    length = len(data)
    edges = []
    for i in range(length):
        if data[i]==arrow:
            edges.append([data[i-1],data[i+1]])
    return edges
def parser(dot, arrow):
    a = parse_dot(dot)
    b = parse_line(a)
    edges = get_edges(b,arrow)
    edges[-1][1] = '"not found"'
    return edges
def is_contain(List,element):
    if List.count(element) >= 1:
        return True
    else:
        return False
    
def calculate_CF(cluster,edges):
    mu_i = 0
    e_ij = 0
    e_ji = 0
    
    for edge in edges:
        from_node = edge[0]
        to_node = edge[1]
        if is_contain(cluster, from_node):
            if is_contain(cluster, to_node):
                mu_i +=1
            else:
                e_ij +=1
        elif is_contain(cluster, to_node):
            e_ji +=1
    CF_i = mu_i / (mu_i + (e_ij+e_ji)/2)
    return CF_i
    
def find_nodes(edges):
    nodes = []
    for edge in edges:
        if not(is_contain(nodes, edge[0])):
            nodes.append(edges[0])
        
#read .gv file(dot) and create graphs
dot_file = read_and_render('test/test.gv')
print(dot_file.source)
edges = parser(dot_file,"->") # second argument should be "--" or "->" (depends on .dot file format)
print(edges)

#calculate CF
cluster = ['"scaffold-hunter-2.6.3.jar"','"java.base"']
CF1 = calculate_CF(cluster,edges)