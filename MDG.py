import Node

class MDG:
    def __init__(self, edges):
        self.edges = []
        self.nodes = []
        self.graph = []

        for edge in edges:
            from_node, from_idx = self.search_node(edge[0])
            to_node, to_idx = self.search_node(edge[1])
            if from_node is None:
                from_node = Node.Node(edge[0])
                self.add_node(from_node)
                from_idx = len(self.nodes) - 1
            if to_node is None:
                to_node = Node.Node(edge[1])
                self.add_node(to_node)
                to_idx = len(self.nodes) - 1

            from_node.add_from_node(to_node)
            to_node.add_to_node(from_node)
            self.graph[from_idx][to_idx] = 1
            self.graph[to_idx][from_idx] = 1
            self.edges.append([from_node, to_node])

            self.set_feature_vector()

    def search_node(self, name):
        """
        Search node with given name
        :param name: Name of target node
        :return: A node and its index that the name is the same or None
        """
        for i in range(len(self.nodes)):
            if self.nodes[i].name == name:
                return self.nodes[i], i
        return None, None

    def add_node(self, node):
        """
        Add given node to this dependency graph
        :param node: A node that wanted to add to this graph
        :return: None
        """
        self.nodes.append(node)
        for i in range(len(self.graph)):
            self.graph[i].append(0)
        self.graph.append([0] * (len(self.graph) + 1))

    def set_feature_vector(self):
        """
        Set feature vector to nodes based on dependency graph
        :return: None
        """
        for i in range(len(self.nodes)):
            self.nodes[i].set_feature_vector(self.graph[i])
