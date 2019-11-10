
from structpy.graph.net import Network
import structpy.model.logic_net.logic_node as logic


class LogicNet(Network):

    def update(self, node, value):
        node *= value
        for source, target, label in self.arcs_out(node):
            label.update(source, target)
        for source, target, label in self.arcs_in(node):
            label.update_reverse(target, source)


