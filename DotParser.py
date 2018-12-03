from graphviz import Source
import os


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


def write_file(filepath, method, clusters, targetMDG):
    # if file exists, remove and create new file.
    result_path = "test/result/" + filepath[0:-4] + "_" + method + "_result.gv"
    if os.path.exists(result_path):
        os.remove(result_path)

    f = open(result_path, "w")
    f.write('digraph "summary" {\n')
    for edge in targetMDG.edges:
        f.write('  ' + str(edge[0]) + '                       -> ' + str(edge[1]) + ';\n')

    f.write("\n\n")
    cluster_num = len(clusters)

    for i in range(cluster_num):
        data = "  subgraph cluster_" + str(i) + " {\n"
        f.write(data)
        for node in clusters[i].get_nodes():
            data = "    " + str(node) + "; "
            f.write(data)
        f.write("\n")
        f.write("  }\n")

    f.write("}")
    f.close()

    a = Source.from_file(result_path)
    a.render(result_path, view=True)
