
from structpy.graph.core.point_graph import PointGraph

class MapPointGraph(PointGraph):
    """
    `self._nodes`: dict<pro:set<epi>>
    `:self._reverse`:dict<epi:set<pro>>
    """

    def __init__(self):
        self._nodes = {}
        self._reverse = {}

    def arcs(self):
        for node in self._nodes:
            for epi in self._nodes[node]:
                yield (node, epi)

    def has_arc(self, pro, epi):
        return pro in self._nodes and epi in self._nodes[pro]

    def nodes_number(self):
        return len(self._nodes)

    def arcs_number(self):
        i = 0
        for _, epis in self._nodes.items():
            i += len(epis)
        return i

    def add_node(self, node):
        self._nodes[node] = set()
        self._reverse[node] = set()

    def add_arc(self, pro, epi, arc=None):
        self._nodes[pro].add(epi)
        self._reverse[epi].add(pro)

    def remove_node(self, node):
        for epi in self._nodes[node]:
            self._reverse[epi].remove(node)
        del self._nodes[node]
        for pro in self._reverse[node]:
            self._nodes[pro].remove(node)
        del self._reverse[node]

    def remove_arc(self, pro, epi):
        self._nodes[pro].remove(epi)
        self._reverse[epi].remove(pro)

    def epis(self, node):
        if node in self._nodes:
            for epi in self._nodes[node]:
                yield epi

    def epis_number(self, node):
        if node in self._nodes:
            return len(self._nodes[node])
        else:
            return 0

    def pros(self, node):
        if node in self._reverse:
            for pro in self._reverse[node]:
                yield pro

    def pros_number(self, node):
        if node in self._reverse:
            return len(self._reverse[node])
        else:
            return 0

    def load(self, filename, node_fun=None):
        if filename[-4:] != '.lgt':
            filename += '.lgt'

        with open(filename) as file:
            pro = None
            for line in file:
                if line.strip() != "":
                    tabs = 0
                    while line[tabs] == '\t':
                        tabs += 1
                    if len(line) == 0 or line[tabs] == '#':
                        continue
                    if line[tabs] == '\\' and len(line) > 1 \
                            and line[tabs + 1] == '#':
                        line = line[:tabs] + line[tabs + 1:]
                    if tabs == 0:
                        pro = line.strip()
                    elif tabs == 1:
                        epi = line.strip()
                        if node_fun is not None:
                            pro = node_fun(pro)
                            epi = node_fun(epi)
                        self.add(pro, epi)
        return self

    def save(self, filename, node_fun=None):
        if filename[-4:] != '.lgt':
            filename += '.lgt'
        with open(filename, 'w') as file:
            for pro in self.nodes():
                if self.epis_number(pro) > 0:
                    file.write(pro + '\n')
                    for epi in self.epis(pro):
                        file.write('\t' + epi + '\n')
                    file.write('\n')