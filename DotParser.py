from graphviz import Source


def read_and_render(filename):  # return source
    a = Source.from_file(filename)
    # print(a.source)
    # a.render(filename, view=True)
    return a


def parser(dot, arrow):  # parse .dot file and generate dependency(A->B) list
    def parse_dot(dot):
        par1 = dot.source.split(";\n")
        par2 = []
        for i in par1:
            for j in i.split(" "):
                par2.append(j)
        return par2

    def parse_line(lines):
        # remove "\n"
        result = lines[:]
        num = result.count("")
        for i in range(num):
            result.remove("")
        return result

    def get_edges(data, arrow):  # arrow = " -- " or " -> "
        length = len(data)
        edges = []
        for i in range(length):
            if data[i] == arrow:
                edges.append([data[i - 1], data[i + 1]])
        return edges

    a = parse_dot(dot)
    b = parse_line(a)
    edges = get_edges(b, arrow)
    edges[-1][1] = '"not found"'
    return edges