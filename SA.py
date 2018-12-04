import Cluster
import TurboMQ
import random
import math

NUM_Population = 100
# NUM_Iteration = 40


class SimulatedAnnealing:
    def __init__(self, targetMDG, WCAresult=None):
        self.graph = targetMDG
        self.result = []
        if WCAresult is None:  # initialize clusters by random
            for i in range(len(targetMDG.nodes)):
                self.result.append(Cluster.Cluster())
            for node in targetMDG.nodes:
                idx = random.randrange(0, len(self.result))
                self.result[idx].add_node(node)
            for cluster in self.result[:]:
                if len(cluster.get_nodes()) == 0:
                    self.result.remove(cluster)
        else:  # based on WCA
            self.result = WCAresult
        self.score = TurboMQ.calculate_fitness(self.result, self.graph)
        self.max_result = self.result[:]

    def __lt__(self, other):
        return self.score < other.score

    def __le__(self, other):
        return self.score <= other.score

    def add_new_cluster(self):
        """
        Add new cluster with 0 nodes to result
        :return: None
        """
        self.result.append(Cluster.Cluster())
        return len(self.result) - 1

    def add_node_to_cluster(self, idx, node):
        """
        Add given node to cluster
        :param idx: An index of cluster based on self.result
        :param node: Given node that wanted to add to given cluster.
        :return: None
        """
        if idx == len(self.result):
            target_cluster = Cluster.Cluster()
            self.result.append(target_cluster)
        else:
            target_cluster = self.result[idx]
        target_cluster.add_node(node)

    def remove_node_to_cluster(self, idx, node):
        """
        Remove given node to cluster
        :param idx: An index of cluster based on self.result
        :param node: Given node that wanted to remove to given cluster.
        :return:
        """
        target_cluster = self.result[idx]
        target_cluster.remove_node(node)
        if len(target_cluster.get_nodes()) == 0:
            self.result.remove(target_cluster)

    def replace_node(self, node, from_idx, to_idx):
        """
        Replace given node between two clusters
        :param node: Given node that wanted to remove to given cluster.
        :param from_idx: An index of cluster based on self.result
        :param to_idx: An index of cluster based on self.result
        :return: None
        """
        self.remove_node_to_cluster(from_idx, node)
        self.add_node_to_cluster(to_idx, node)
        self.score = TurboMQ.calculate_fitness(self.result, self.graph)

    def try_replace_node(self, node, from_idx, to_idx):
        """
        Try to replace node between two clusters and give fitness score of result
        :param node: Given node that wanted to remove to given cluster.
        :param from_idx: An index of cluster based on self.result
        :param to_idx: An index of cluster based on self.result
        :return: Fitness score after replace node
        """
        result = self.result[:]

        target_cluster = result[from_idx]
        target_cluster.remove_node(node)

        if to_idx == len(result):
            target_cluster = Cluster.Cluster()
            result.append(target_cluster)
        else:
            target_cluster = result[to_idx]
        target_cluster.add_node(node)

        tried_score = TurboMQ.calculate_fitness(result, self.graph)

        target_cluster = result[to_idx]
        target_cluster.remove_node(node)
        target_cluster = result[from_idx]
        target_cluster.add_node(node)

        return tried_score

    def search_cluster_by_node(self, target):
        """
        Search cluster which include given node, and return the index of it
        :param target: Given node that wanted to search
        :return: Index of cluster that has given node
        """
        for i in range(len(self.result)):
            cluster = self.result[i]
            for node in cluster.get_nodes():
                if target == node:
                    return i
        return None

    def search_highest_k_neighbor(self, k):
        """
        Search the highest neighbor between k random neighbors, and return the moved node and modified clusters
        :param k: int, number of neighbors to be considered
        :return: the moved node, modified clusters and max score of the highest neighbor
        """
        max_score = 0
        target_node = None
        from_idx = None
        to_idx = None
        for i in range(k):
            node = self.graph.nodes[random.randrange(len(self.graph.nodes))]
            cluster_idx = self.search_cluster_by_node(node)
            if len(self.result[cluster_idx].get_nodes()) == 1:
                end_i = len(self.result)
            else:
                end_i = len(self.result) + 1

            random_cluster_idx = random.randrange(end_i)
            if random_cluster_idx != cluster_idx:
                tried_score = self.try_replace_node(node, cluster_idx, random_cluster_idx)
                if max_score < tried_score:
                    max_score = tried_score
                    target_node = node
                    from_idx = cluster_idx
                    to_idx = random_cluster_idx

        return max_score, target_node, from_idx, to_idx

    def climb_with_annealing(self, k, t):
        """
        Climb to the neighborhood than the current state using simulated annealing.
        :param k: int, number of neighbors to be considered
        :param t: time, it is used with the formula of the simulated annealing
        :return: boolean, Whether or not it climbs to a higher neighborhood than the original state.
        """
        max_score, target_node, from_idx, to_idx = self.search_highest_k_neighbor(k)
        if not target_node:
            return False
        if max_score > self.score:
            self.replace_node(target_node, from_idx, to_idx)
            self.max_result = self.result[:]
        else:
            if random.random() < math.exp((max_score - self.score) / (t + 1)) - 1:
                self.replace_node(target_node, from_idx, to_idx)
        return True

    def update_score(self):
        """
        Update score with fitness function(TurboMQ).
        :return: None
        """
        self.score = TurboMQ.calculate_fitness(self.result, self.graph)

    def remove_empty_cluster(self):
        """
        Remove empty clusters in the list of clusters
        :return: None
        """
        for cluster in self.result[:]:
            if len(cluster.get_nodes()) == 0:
                self.result.remove(cluster)


def SA(targetMDG):
    """
    Simulated Annealing algorithm base on Hill climbing algorithm for clustering problem
    :param targetMDG: Dependency graph
    :return: A list of clusters after algorithm
    """
    hill_climbers = []
    for i in range(NUM_Population):
        hill_climbers.append(SimulatedAnnealing(targetMDG))

    completed_climbers = []
    completed_max_climbers = []

    # k: int, number of neighbors to be considered
    k = 20
    i = 0
    not_increased = 0
    max_score = 0

    while True:
        for climber in hill_climbers[:]:
            result = climber.climb_with_annealing(k, i)
            if not result:
                completed_climbers.append(climber)
                hill_climbers.remove(climber)
            max_completed_climber = SimulatedAnnealing(targetMDG)
            max_completed_climber.result = climber.max_result
            max_completed_climber.update_score()
            completed_max_climbers.append(max_completed_climber)

        total_climbers = hill_climbers + completed_climbers + completed_max_climbers
        total_climbers.sort()
        print("Iteration ", i, ": ", total_climbers[-1].score)

        if total_climbers[-1].score - max_score != 0:
            not_increased = 0
        else:
            not_increased += 1

        if len(hill_climbers) == 0 or not_increased == 10:
            break
        i += 1
        max_score = total_climbers[-1].score

    total_climbers = hill_climbers + completed_climbers + completed_max_climbers
    total_climbers.sort()

    max_climber = total_climbers[-1]

    print("TurboMQ = ", max_climber.score)
    for c in max_climber.result:  # print all clusters which are not singleton
        if 1 != len(c.get_nodes()):
            print(c.get_nodes())

    return max_climber.result


def WCA_SA(targetMDG, WCAresult):
    """
    Simulated Annealing algorithm base on Hill climbing algorithm and WCA(1 Population) for clustering problem
    :param targetMDG: Dependency graph
    :param WCAresult: Result of WCA algorithm based on dependency graph
    :return: A list of clusters after algorithm
    """
    hill_climbers = []
    for i in range(NUM_Population):
        hill_climbers.append(SimulatedAnnealing(targetMDG, WCAresult))

    completed_climbers = []
    completed_max_climbers = []

    # k: int, number of neighbors to be considered
    k = 20
    i = 0
    not_increased = 0
    max_score = 0
    Temperature = 20

    while True:
        for climber in hill_climbers[:]:
            result = climber.climb_with_annealing(k, Temperature)
            if not result:
                completed_climbers.append(climber)
                hill_climbers.remove(climber)
            max_completed_climber = SimulatedAnnealing(targetMDG)
            max_completed_climber.result = climber.max_result
            max_completed_climber.update_score()
            completed_max_climbers.append(max_completed_climber)

        total_climbers = hill_climbers + completed_climbers + completed_max_climbers
        total_climbers.sort()
        print("Iteration ", i, ": ", total_climbers[-1].score)

        if total_climbers[-1].score - max_score != 0:
            not_increased = 0
        else:
            not_increased += 1

        if len(hill_climbers) == 0 or not_increased == 10:
            break
        i += 1
        max_score = total_climbers[-1].score
        if Temperature > 0:
            Temperature -= 0.5

    total_climbers = hill_climbers + completed_climbers + completed_max_climbers
    total_climbers.sort()

    max_climber = total_climbers[-1]

    print("TurboMQ = ", max_climber.score)
    for c in max_climber.result:  # print all clusters which are not singleton
        if 1 != len(c.get_nodes()):
            print(c.get_nodes())

    max_climber.remove_empty_cluster()
    return max_climber.result
