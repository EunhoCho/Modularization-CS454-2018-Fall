# TurboMQ functions - CF, summation of CF(calculate_fitness) functions

def calculate_CF(cluster, targetMDG):
    """
    Calculate cluster factor for single cluster
    :param cluster: target cluster for calculating Cluster factor
    :param targetMDG: Dependency graph including node and edge information
    :return: Cluster factor for given cluster
    """
    mu_i = 0
    e_ij = 0
    e_ji = 0

    for edge in targetMDG.edges:
        from_node = edge[0]
        to_node = edge[1]
        if from_node in cluster:
            if to_node in cluster:
                mu_i += 1
            else:
                e_ij += 1
        elif to_node in cluster:
            e_ji += 1

        if mu_i == 0:
            CF_i = 0
        else:
            CF_i = mu_i / (mu_i + ((e_ij + e_ji) / 2))
    return CF_i


def calculate_fitness(clusters, targetMDG):
    """
    Calculate TurboMQ for clustering result
    :param clusters: A list of clusters
    :param targetMDG: Dependency graph including node and edge information
    :return: TurboMQ for clustering result
    """
    TurboMQ = 0

    for cluster in clusters:
        names = []
        for node in cluster.get_nodes():
            names.append(node)

        TurboMQ += calculate_CF(names, targetMDG)
    return TurboMQ