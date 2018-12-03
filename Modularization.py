import DotParser
import HC
import SA
import PSO
import MakeResult
import argparse
from WCA import WCA


def main():

    parser = argparse.ArgumentParser(description='Modularize given dot file')
    parser.add_argument('file_path', metavar='F', type=str, nargs='+',
                        help='File path for dot file')
    parser.add_argument('-a', help='Algorithm for modularization. All, WCA, HC, WCA_HC, SA, WCA_SA, PSO, WCA_PSO')
    args = parser.parse_args()

    file_path = args.file_path
    if args.a:
        modularizeMethod = args.a
    else:
        modularizeMethod = 'All'

    for single_file in file_path:

        targetMDG = MakeResult.make_target_MDG(single_file)
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
            MakeResult.print_result(single_file)

        if modularizeMethod != 'All':
            DotParser.write_file(single_file, modularizeMethod, clusters, targetMDG)


if __name__ == "__main__":
    main()
