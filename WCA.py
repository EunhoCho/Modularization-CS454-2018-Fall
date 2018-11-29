import Cluster
import TurboMQ


def cluster_initialize(nodes):  # make initial cluster which contains all singleton nodes, and each node is considered as a single cluster
    clusters = []
    numofnodes = len(nodes)
    for i in range(numofnodes):
        cluster = Cluster.Cluster()
        cluster.add_node(nodes[i].get_name())
        cluster.set_feature_vector(nodes[i].get_feature_vector())
        clusters.append(cluster)
    return clusters


def compare_similarity(clusters, nodes):  # compare two clusters in clusters list, and return two most similar clusters among all clusters.
    numofcluster = len(clusters)
    numofnodes = len(nodes)  # numofnodes = dimension of feature vector
    max_UENM = -1
    max_c1 = Cluster.Cluster()
    max_c2 = Cluster.Cluster()

    for i in range(numofcluster):  # for all two-cluster combinations
        for j in range(numofcluster):
            if i >= j:
                continue

            cluster1 = clusters[i].copy()
            cluster2 = clusters[j].copy()
            feature1 = cluster1.get_feature_vector()
            feature2 = cluster2.get_feature_vector()
            # use WCA_UENM value
            a = 0
            b = 0
            c = 0
            d = 0
            n = 0
            Ma = 0
            # get a,b,c,d,n,Ma
            for k in range(numofnodes):
                if feature1[k] > 0 and feature2[k] > 0:
                    a += 1
                    Ma += feature1[k] + feature2[k]
                if feature1[k] > 0 and feature2[k] == 0:
                    b += 1
                if feature1[k] == 0 and feature2[k] > 0:
                    c += 1
                if feature1[k] == 0 and feature2[k] == 0:
                    d += 1
            # calculate UENM
            n = a + b + c + d
            UENM = (0.5 * Ma) / ((0.5 * Ma) + b + c + n)
            # if new UENM is higher than origianal max_UENM, then update it
            if UENM > max_UENM:
                max_UENM = UENM
                max_c1 = clusters[i]
                max_c2 = clusters[j]
    # print("UENM= ",max_UENM)
    return max_c1, max_c2


def merge_cluster(c1, c2, clusters, nodes):  # merge two most-similar clusters into one cluster.
    clus = clusters[:]
    clus.remove(c1)
    clus.remove(c2)
    merged_cluster = Cluster.Cluster()
    c1_nodes = c1.get_nodes()
    c2_nodes = c2.get_nodes()
    for node in c1_nodes:
        merged_cluster.add_node(node)
    for node in c2_nodes:
        merged_cluster.add_node(node)

    # get new c1+c2 feature vector
    numofnodes = len(nodes)  # numofnodes = dimension of feature vector
    feature_vector = []  # initialize  feature vector
    for i in range(numofnodes):  # make n dimeansional feature vector
        feature_vector.append(0)
    feature1 = c1.get_feature_vector()
    feature2 = c2.get_feature_vector()
    numnode1 = len(c1.get_nodes())
    numnode2 = len(c2.get_nodes())

    for i in range(numofnodes):
        feature_vector[i] = feature1[i] + feature2[i]
        feature_vector[i] /= (numnode1 + numnode2)
    merged_cluster.set_feature_vector(feature_vector)

    clus.append(merged_cluster)
    return clus


def applyWCA(clusters, targetMDG):
    max_TurboMQ = 0
    max_clusters = []
    numofnodes = len(targetMDG.nodes)
    count = 0
    for i in range(numofnodes - 1):  # clustering
        [c1, c2] = compare_similarity(clusters, targetMDG.nodes)  # clusters중 가장 비슷한 2개의 cluster를 선택
        # print (c1.nodes)
        # print (c2.nodes)
        clusters = merge_cluster(c1, c2, clusters, targetMDG.nodes)  # c1,c2가 merge된 clusters를 return
        TMQ = TurboMQ.calculate_fitness(clusters, targetMDG.edges)  # calculate TurboMQ of these clusters
        if TMQ >= max_TurboMQ and TMQ != 1:
            max_TurboMQ = TMQ
            max_clusters = clusters[:]
            count = 0
        else:
            count += 1
        #if count == 3:
            #print("TurboMQ = ", TurboMQ)
            #break
        print("TurboMQ = ", TurboMQ)
    return [max_TurboMQ, max_clusters]


def WCA(targetMDG):
    # apply WCA algorithm
    clusters = cluster_initialize(targetMDG.nodes)
    result_MQ, result_clusters = applyWCA(clusters, targetMDG)  # result of WCA algorithm

    for c in result_clusters:  # print all clusters which are not singleton
        if 1 != len(c.get_nodes()):
            print(c.get_nodes())

    return result_clusters
