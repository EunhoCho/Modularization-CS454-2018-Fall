from graphviz import Source


def read_and_render(filename):
    """
    Read file and return source
    :param filename: Filename that wanted to read
    :return: Source of given file
    """
    a = Source.from_file(filename)
    # print(a.source)
    # a.render(filename, view=True)
    return a


def parser(dot, arrow):
    """
    Parse given dot file and make a list of edges
    :param dot: dot file that wanted to parse
    :param arrow: Arrow style of this dot file (ex. "--" or "->")
    :return: A list of edges in given dot file
    """
    def parse_dot(dot):
        """
        Parse given dot file
        :param dot: dot file that wanted to parse
        :return: A list of string from dot file
        """
        par1 = dot.source.split(";\n")
        par2 = []
        for i in par1:
            for j in i.split(" "):
                par2.append(j)
        return par2

    def parse_line(lines):
        """
        Remove line with no information
        :param lines: A list of string from dot file
        :return: A list of string without ""
        """
        result = lines[:]
        num = result.count("")
        for i in range(num):
            result.remove("")
        return result

    def get_edges(data, arrow):
        """
        Make a list of edges based on data
        :param data: A list of string from dot file
        :param arrow: Arrow style of dot file (ex. "--" or "->")
        :return: A list of edges in given dot file
        """
        length = len(data)
        edges = []
        for i in range(length):
            if data[i] == arrow:
                if data[i - 1] == '"not':
                    data[i - 1] = '"not found"'
                if data[i + 1] == '"not':
                    data[i + 1] = '"not found"'
                edges.append([data[i - 1], data[i + 1]])
        return edges

    a = parse_dot(dot)
    b = parse_line(a)
    edges = get_edges(b, arrow)
    return edges
