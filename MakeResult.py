import sys
import DotParser
import HC
import SA
import MDG
import PSO
import TurboMQ
from WCA import WCA



# read .gv file(dot) and create graphs
def make_target_MDG(file_path):
    dot_file = DotParser.read_and_render(file_path)
    #print(dot_file.source)
    
    # get edge information and parse it
    edges = DotParser.parser(dot_file, "->")  # second argument should be "--" or "->" (depends on .dot file format)
    
    # make dependency graph and set feature vector
    targetMDG = MDG.MDG(edges)
    #print(targetMDG.edges)
    targetMDG.set_feature_vector()
    return targetMDG

def get_information(targetMDG, file_path): #using target_MDG and a benchmark, create result
    methods = ['WCA','HC','WCA_HC','SA','WCA_SA','PSO','WCA_PSO']
    clusters_set = []
    TMQ = []
    cohe_coup = []
    clusters_set.append(WCA(targetMDG))
    clusters_set.append(HC.HC(targetMDG))
    clusters_set.append(HC.WCA_HC(targetMDG, WCA(targetMDG)))
    clusters_set.append(SA.SA(targetMDG))
    clusters_set.append(SA.WCA_SA(targetMDG, WCA(targetMDG)))
    clusters_set.append(PSO.PSO(targetMDG))
    clusters_set.append(PSO.WCA_PSO(targetMDG, WCA(targetMDG)))
    
    #get TMQ data
    for clusters in clusters_set:
        TMQ.append(TurboMQ.calculate_fitness(clusters, targetMDG))
        cohe_coup.append(TurboMQ.get_cohesion_coupling(clusters, targetMDG))
    #write result files
    for i in range(len(methods)):
        DotParser.write_file(file_path, methods[i], clusters_set[i])
        
    return TMQ, cohe_coup, clusters_set

def print_result():
    file_paths=['test/launch4j.dot','test/hibernate.dot','test/pmd.dot','test/scaffold.dot']
    methods = ['WCA','HC','WCA_HC','SA','WCA_SA','PSO','WCA_PSO']
    TMQs = []
    cohe_coups = []
    
    #test for all benchmarks
    for file_path in file_paths:
        
        targetMDG = make_target_MDG(file_path)
        TMQ, cohe_coup, clusters_set = get_information(targetMDG, file_path)
        TMQs.append(TMQ)
        cohe_coups.append(cohe_coup)
        
    #print Information
    print("\n=====Result=====")
    for i in range(len(file_paths)):
        for j in range(len(methods)):
            print(file_paths[i] + " " + methods[j])
            print("TMQ= " + str(TMQs[i][j]) + ", " + "Cohesion= " + str(cohe_coups[i][j][0])+ ", " + "Coupling= " + str(cohe_coups[i][j][1])+"\n")
    return 0