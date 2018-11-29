class Node(object):
    """
    Node is entity for clustering problem
    """
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
        """
        Return a list of node that linked by edge from this node
        :return: A list of node that linked by edge from this node
        """
        return self.from_node

    def get_to_node(self):
        """
        Return a list of node that linked by edge to this node
        :return: A list of node that linked by edge to this node
        """
        return self.to_node

    def get_feature_vector(self):
        """
        Return feature vector of this node
        :return: A list of number which represents feature vector
        """
        return self.feature_vector[:]

    def add_from_node(self, _input):
        """
        Add a node that linked by edge from this node
        :param _input: A node that linked by edge from this node
        :return: None
        """
        self.from_node.append(_input)

    def add_to_node(self, _input):
        """
        Add a node that linked by edge to this node
        :param _input: A node that linked by edge to this node
        :return: None
        """
        self.to_node.append(_input)

    def set_feature_vector(self, _input):
        """
        Add feature vector of this node
        :param _input: A list of number which represents feature vector
        :return: None
        """
        self.feature_vector = _input[:]
