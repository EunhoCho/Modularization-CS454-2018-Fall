class _node(object):  # node class
    def __init__(self, name):
        self.name = name
        self.from_node = []
        self.to_node = []
        self.feature_vector = []  # each node(class) has own feature vector

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def get_from_node(self):
        return self.from_node

    def get_to_node(self):
        return self.to_node

    def get_feature_vector(self):
        return self.feature_vector[:]

    def add_from_node(self, _input):
        self.from_node.append(_input)

    def add_to_node(self, _input):
        self.to_node.append(_input)

    def set_feature_vector(self, _input):
        self.feature_vector = _input[:]


def search_node(nodes, name):
    for node in nodes:
        if node.name == name:
            return node
    return None


def make_nodes(edges):  # make 'nodes' list composed of node class
    nodes = []
    for edge in edges:
        from_node = search_node(nodes, edge[0])
        to_node = search_node(nodes, edge[1])
        if from_node is None:
            from_node = _node(edge[0])
        if to_node is None:
            to_node = _node(edge[1])

        from_node.add_from_node(to_node)
        to_node.add_to_node(from_node)

    return nodes


def make_dependency_graph(nodes, node_names):  # make dependency graph using edge information
    MDG = []
    for i in range(len(nodes)):
        MDG.append([0] * len(nodes))
    # MDG = zeros(nodes_num, nodes_num) (n x n matrix)

    for i in range(len(nodes)):
        curr_node = nodes[i]
        from_node = curr_node.get_from_node()
        j = 0
        for node_name in node_names:
            if node_name in from_node:
                MDG[i][j] = 1
            else:
                MDG[i][j] = 0
            j += 1
    return MDG
