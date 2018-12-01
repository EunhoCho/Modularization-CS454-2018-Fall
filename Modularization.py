import sys
import DotParser
import HC
import SA
import MDG
import PSO
from WCA import WCA


def main():
    # read .gv file(dot) and create graphs
    file_path = 'test/launch4j.dot'

    dot_file = DotParser.read_and_render(file_path)
    print(dot_file.source)

    # get edge information and parse it
    edges = DotParser.parser(dot_file, "->")  # second argument should be "--" or "->" (depends on .dot file format)

    # make dependency graph and set feature vector
    targetMDG = MDG.MDG(edges)
    print(targetMDG.edges)
    targetMDG.set_feature_vector()

    modularizeMethod = sys.argv[1]

    clusters = None
    if modularizeMethod == 'WCA':
        clusters = WCA(targetMDG)
        DotParser.write_file(file_path, clusters)
    elif modularizeMethod == 'HC':
        clusters = HC.HC(targetMDG)
    elif modularizeMethod == 'WCA_HC':
        clusters = HC.WCA_HC(targetMDG, WCA(targetMDG))
    elif modularizeMethod == 'SA':
        clusters = SA.SA(targetMDG)
    elif modularizeMethod == 'WCA_SA':
        clusters = SA.WCA_SA(targetMDG, WCA(targetMDG))
    elif modularizeMethod == 'PSO':
        clusters = PSO.PSO(targetMDG)
    elif modularizeMethod == 'WCA_PSO':
        clusters = PSO.WCA_PSO(targetMDG, WCA(targetMDG))
    DotParser.write_file(file_path, clusters)


if __name__ == "__main__":
    main()
