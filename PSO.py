import Cluster
import TurboMQ
import random
import numpy as np
from operator import itemgetter

NUM_Population = 100
# NUM_Iteration = 20


class ParticleSwarm:
    def __init__(self, targetMDG, Num_Cluster=-1, WCAresult=None):
        self.graph = targetMDG
        self.result = []
        if WCAresult is None:  # initialize clusters by random
            if Num_Cluster == -1 or Num_Cluster > len(targetMDG.nodes):
                for i in range(len(targetMDG.nodes)):
                    self.result.append(Cluster.Cluster())
                for i in range(len(targetMDG.nodes)):
                    idx = random.randrange(0, len(self.result))
                    self.result[idx].add_node(targetMDG.nodes[i])
                for cluster in self.result[:]:
                    if len(cluster.get_nodes()) == 0:
                        self.result.remove(cluster)
            else:
                for i in range(Num_Cluster):
                    self.result.append(Cluster.Cluster())
                suffled_node = targetMDG.nodes[:]
                random.shuffle(suffled_node)
                list = range(0, len(targetMDG.nodes))
                out = random.sample(list, Num_Cluster - 1)
                out.sort()

                cut = 0
                for i in range(len(suffled_node)):
                    if cut < Num_Cluster - 1 and i >= out[cut]:
                        cut += 1
                    self.result[cut].add_node(suffled_node[i])

        else:  # based on WCA
            self.result = WCAresult
        self.score = TurboMQ.calculate_fitness(self.result, self.graph)
        self.position = self.cluster_to_position_matrix()
        self.velocity = [[0] * len(self.result)] * len(self.position)
        self.lbest = self.result[:]
        self.gbest = self.result[:]

    def __lt__(self, other):
        return self.score < other.score

    def __le__(self, other):
        return self.score <= other.score

    def cluster_to_position_matrix(self, c=None):
        """
        Change list of clusters to position matrix for binary PSO
        :param c: cluster to be converted
        :return: position_matrix: 2D position matrix for binary PSO
        """
        clusters = self.result
        if c is not None:
            clusters = c
        position_matrix = []
        for node in self.graph.nodes:
            node_in_clusters = []
            for cluster in clusters:
                if node in cluster.get_nodes():
                    node_in_clusters.append(1)
                else:
                    node_in_clusters.append(0)
            position_matrix.append(node_in_clusters)
        return position_matrix

    def position_matrix_to_cluster(self, p=None):
        """
        Change position matrix for binary PSO to list of clusters
        :param p: position to be converted
        :return: list of clusters
        """
        result = []
        position = self.position
        if p is not None:
            position = p
        Num_Node = len(position)
        Num_Cluster = len(position[0])
        for i in range(Num_Cluster):
            result.append(Cluster.Cluster())

        for i in range(Num_Node):
            for j in range(Num_Cluster):
                if position[i][j] == 1:
                    result[j].add_node(self.graph.nodes[i])
        return result

    def distance_between_positions(self, other):
        """
        Difference between two position matrix for binary PSO
        :param : other: Another particle
        :return: differ: number of difference between two matrix
        """
        differ = 0
        Num_Node = len(self.position)
        Num_Cluster = len(self.position[0])
        for i in range(Num_Node):
            for j in range(Num_Cluster):
                if self.position[i][j] + other.position[i][j] == 1:
                    differ += 1
        return differ

    def k_neighberhood(self, others, k):
        """
        Find the k closest neighborhoods from the reference particle.
        :param : others: list of all particles included self
        :param : k: int, number of neighbors to be considered
        :return: neighborhoods: the k closest neighborhoods
        """
        others = others[:]
        others.remove(self)
        particles_with_distance = []
        sorted_particles_with_distance = []
        neighborhoods = []
        for other in others:
            differ = self.distance_between_positions(other)
            particles_with_distance.append([other, differ])

        if k > len(others):
            k = len(others)
        for i in range(k):
            sorted_particles_with_distance.append(max(particles_with_distance, key=itemgetter(1)))
            particles_with_distance.remove(sorted_particles_with_distance[-1])

        for i in range(k):
            neighborhoods.append(sorted_particles_with_distance[i][0])
        return neighborhoods

    def update_score(self):
        """
        Update score with fitness function(TurboMQ).
        :return: None
        """
        self.score = TurboMQ.calculate_fitness(self.result, self.graph)

    def get_score(self):
        """
        Update and Get score with fitness function(TurboMQ).
        :return : self.score: score of the particle with fitness function.
        """
        self.update_score()
        return self.score

    def update_gbest(self, others, k):
        """
        Update global best particle of all iteration with k neighborhoods.
        :param : others: list of all particles included self
        :param : k: int, number of neighbors to be considered
        :return: None
        """
        neighborhoods = self.k_neighberhood(others, k)
        gbest_score = TurboMQ.calculate_fitness(self.gbest, self.graph)
        for position in neighborhoods:
            if gbest_score < position.get_score():
                self.gbest = position.result[:]

    def update_lbest(self):
        """
        Update local best particle of all iteration.
        :return: None
        """
        lbest_score = TurboMQ.calculate_fitness(self.lbest, self.graph)
        if lbest_score < self.get_score():
            self.lbest = self.result[:]

    def update_velocity_and_position(self, w, c1, c2):
        """
        Update velocity and position of particle.
        :param : c1: float, cognitive parameter, 1 - 2
        :param : c2: float, social parameter, 1.5 - 2.5
        :param : w: float, inertia parameter, 0.4 - 0.9
        :return: None
        """
        Num_Node = len(self.position)
        Num_Cluster = len(self.position[0])
        r1 = random.random()
        r2 = random.random()
        lbest_position = self.cluster_to_position_matrix(self.lbest)
        gbest_position = self.cluster_to_position_matrix(self.gbest)
        # print("lbest size:", len(lbest_position), len(lbest_position[0]))
        # print("gbest size:", len(gbest_position), len(gbest_position[0]))
        # print("self.position size:", len(self.position), len(self.position[0]))
        # print("self.velocity size:", len(self.velocity), len(self.velocity[0]))

        velocity = w*np.array(self.velocity)\
                   + c1*r1*(np.array(lbest_position) - np.array(self.position))\
                   + c2*r2*(np.array(gbest_position) - np.array(self.position))
        new_position = np.array(self.position) + velocity
        for i in range(Num_Node):
            max_pos = -10000000000
            Node_num = -1
            for j in range(Num_Cluster):
                if max_pos < new_position[i][j]:
                    max_pos = new_position[i][j]
                    Node_num = j
            for j in range(Num_Cluster):
                new_position[i][j] = 0
            new_position[i][Node_num] = 1

        self.velocity = []
        for i in range(Num_Node):
            velocity_of_node = []
            for j in range(Num_Cluster):
                velocity_of_node.append(velocity[i][j])
            self.velocity.append(velocity_of_node)

        self.position = []
        for i in range(Num_Node):
            node_in_clusters = []
            for j in range(Num_Cluster):
                node_in_clusters.append(new_position[i][j])
            self.position.append(node_in_clusters)

    def update_cluster_with_position(self):
        """
        Update list of clusters with position of the particle.
        :return: None
        """
        result = self.position_matrix_to_cluster()
        self.result = result

    def remove_empty_clusters(self, c=None):
        """
        Remove the empty clusters on the list of clusters
        :param c: the list of clusters
        :return: None
        """
        clusters = self.result
        if c is not None:
            clusters = c
        for cluster in clusters[:]:
            if len(cluster.get_nodes()) == 0:
                clusters.remove(cluster)


def PSO(targetMDG):
    """
    Particle Swarm Optimization algorithm for clustering problem
    :param targetMDG: Dependency graph
    :return: A list of clusters after algorithm
    """
    positions = []
    SampleParticle = ParticleSwarm(targetMDG)
    Num_Cluster = len(SampleParticle.result)
    positions.append(SampleParticle)
    for i in range(NUM_Population - 1):
        positions.append(ParticleSwarm(targetMDG, Num_Cluster))

    # Initialize swarm, arbitrary
    # c1: float, cognitive parameter, 1 - 2
    # c2: float, social parameter, 1.5 - 2.5
    # w: float, inertia parameter, 0.4 - 0.9
    # k: int, number of neighbors to be considered
    c1 = random.random() + 1
    c2 = random.random() + 1.5
    w = random.random() * 0.5 + 0.4
    k = 15

    total_positions = positions[:]
    i = 0
    not_increased = 0
    max_score = 0

    while True:
        for position in positions:
            position.update_velocity_and_position(w, c1, c2)
            position.update_cluster_with_position()
            position.update_score()
            position.update_lbest()
            position.update_gbest(positions, k)

        total_positions += positions
        total_positions.sort()
        print("Iteration ", i, ": ", total_positions[-1].score)

        max_completed_particle = ParticleSwarm(targetMDG)
        max_completed_particle.result = total_positions[-1].result[:]
        max_completed_particle.position = total_positions[-1].position[:][:]
        max_completed_particle.velocity = total_positions[-1].velocity[:][:]
        max_completed_particle.lbest = total_positions[-1].lbest[:]
        max_completed_particle.gbest = total_positions[-1].gbest[:]
        max_completed_particle.update_score()
        total_positions.append(max_completed_particle)

        if total_positions[-1].score - max_score != 0:
            not_increased = 0
        else:
            not_increased += 1

        if not_increased == 10:
            break
        i += 1
        max_score = total_positions[-1].score

    max_position = total_positions[-1]

    print("TurboMQ = ", max_position.score)
    for cluster in max_position.result:  # print all clusters which are not singleton
        if 1 < len(cluster.get_nodes()):
            print(cluster.get_nodes())

    return max_position.result


def WCA_PSO(targetMDG, WCAresult):
    """
    Particle Swarm Optimization algorithm based on WCA for clustering problem
    :param targetMDG: Dependency graph
    :param WCAresult: Result of WCA algorithm based on dependency graph
    :return: A list of clusters after algorithm
    """
    positions = []
    SampleParticle = ParticleSwarm(targetMDG, WCAresult=WCAresult)
    Num_Cluster = len(SampleParticle.result)
    positions.append(SampleParticle)
    for i in range(NUM_Population - 1):
        positions.append(ParticleSwarm(targetMDG, Num_Cluster))

    # Initialize swarm, arbitrary
    # c1: float, cognitive parameter, 1 - 2
    # c2: float, social parameter, 1.5 - 2.5
    # w: float, inertia parameter, 0.4 - 0.9
    # k: int, number of neighbors to be considered
    c1 = random.random() + 1
    c2 = random.random() + 1.5
    w = random.random() * 0.5 + 0.4
    k = 15

    total_positions = positions[:]
    i = 0
    not_increased = 0
    max_score = 0

    while True:
        for position in positions:
            position.update_velocity_and_position(w, c1, c2)
            position.update_cluster_with_position()
            position.update_score()
            position.update_lbest()
            position.update_gbest(positions, k)

        total_positions += positions
        total_positions.sort()
        print("Iteration ", i, ": ", total_positions[-1].score)

        max_completed_particle = ParticleSwarm(targetMDG)
        max_completed_particle.result = total_positions[-1].result[:]
        max_completed_particle.position = total_positions[-1].position[:][:]
        max_completed_particle.velocity = total_positions[-1].velocity[:][:]
        max_completed_particle.lbest = total_positions[-1].lbest[:]
        max_completed_particle.gbest = total_positions[-1].gbest[:]
        max_completed_particle.update_score()
        total_positions.append(max_completed_particle)

        if total_positions[-1].score - max_score != 0:
            not_increased = 0
        else:
            not_increased += 1

        if not_increased == 10:
            break
        i += 1
        max_score = total_positions[-1].score

    max_position = total_positions[-1]

    print("TurboMQ = ", max_position.score)
    for cluster in max_position.result:  # print all clusters which are not singleton
        if 1 < len(cluster.get_nodes()):
            print(cluster.get_nodes())

    return max_position.result
