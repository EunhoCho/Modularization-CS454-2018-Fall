# TurboMQ functions - CF, summation of CF(calculate_fitness) functions


def calculate_CF(cluster, edges):
    mu_i = 0
    e_ij = 0
    e_ji = 0

    for edge in edges:
        from_node = edge[0]
        to_node = edge[1]
        if from_node in cluster:
            if to_node in cluster:
                mu_i += 1
            else:
                e_ij += 1
        elif to_node in cluster:
            e_ji += 1
    CF_i = mu_i / (mu_i + (e_ij + e_ji) / 2)
    return CF_i


def calculate_fitness(clusters, edges):
    TurboMQ = 0

    for cluster in clusters:
        names = []
        for node in cluster.get_nodes():
            names.append(node)

        TurboMQ += calculate_CF(names, edges)
    return TurboMQ