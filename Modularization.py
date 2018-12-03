import sys
import DotParser
import HC
import SA
import PSO
import MakeResult
from WCA import WCA


def main():
            
    file_path = 'test/launch4j.dot'
    targetMDG = MakeResult.make_target_MDG(file_path)
    modularizeMethod = sys.argv[1]

    clusters = None
    if modularizeMethod == 'WCA':
        clusters = WCA(targetMDG) 
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
    elif modularizeMethod == 'All':
        MakeResult.print_result()
    
    if modularizeMethod != 'All': 
        DotParser.write_file(file_path, modularizeMethod, clusters)


if __name__ == "__main__":
    main()
