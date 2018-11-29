import Cluster
import TurboMQ
import random

NUM_Population = 1
NUM_Iteration = 10


class HillClimber:
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

    def search_highest_neighbor(self):
        max_score = self.score
        target_node = None
        from_idx = None
        to_idx = None
        for node in self.graph.nodes:
            cluster_idx = self.search_cluster_by_node(node)
            if len(self.result[cluster_idx].get_nodes()) == 1:
                end_i = len(self.result)
            else:
                end_i = len(self.result) + 1

            for i in range(end_i):
                if i != cluster_idx:
                    tried_score = self.try_replace_node(node, cluster_idx, i)
                    if max_score < tried_score:
                        max_score = tried_score
                        target_node = node
                        from_idx = cluster_idx
                        to_idx = i

        return target_node, from_idx, to_idx

    def climb(self):
        target_node, from_idx, to_idx = self.search_highest_neighbor()
        if not target_node:
            return False
        self.replace_node(target_node, from_idx, to_idx)
        return True


def HC(targetMDG):
    """
    Hill climbing algorithm for clustering problem
    :param targetMDG: Dependency graph
    :return: A list of clusters after algorithm
    """
    hill_climbers = []
    for i in range(NUM_Population):
        hill_climbers.append(HillClimber(targetMDG))

    completed_climbers = []
    total_climbers = []

    for i in range(NUM_Iteration):
        for climber in hill_climbers[:]:
            result = climber.climb()
            if not result:
                completed_climbers.append(climber)
                hill_climbers.remove(climber)
        total_climbers = hill_climbers + completed_climbers
        total_climbers.sort()
        print("Iteration ", i, ": ", total_climbers[-1].score)

    total_climbers = hill_climbers + completed_climbers
    total_climbers.sort()

    max_climber = total_climbers[-1]

    print("TurboMQ = ", max_climber.score)
    for c in max_climber.result:  # print all clusters which are not singleton
        if 1 != len(c.get_nodes()):
            print(c.get_nodes())

    return max_climber.result


def WCA_HC(targetMDG, WCAresult):
    """
    Hill climbing algorithm based on WCA for clustering problem
    :param targetMDG: Dependency graph
    :param WCAresult: Result of WCA algorithm based on dependency graph
    :return: A list of clusters after algorithm
    """
    hill_climber = HillClimber(targetMDG, WCAresult)
    for i in range(NUM_Iteration):
        result = hill_climber.climb()
        print("Iteration ", i, ": ", hill_climber.score)
        if not result:
            break

    print("TurboMQ = ", hill_climber.score)
    for c in hill_climber.result:  # print all clusters which are not singleton
        if 1 != len(c.get_nodes()):
            print(c.get_nodes())

    return hill_climber.result
