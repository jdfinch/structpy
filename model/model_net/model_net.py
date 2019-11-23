
from structpy.graph.net import Net
from types import MethodType
from structpy.graph.traversal import Traversal, rings

class ModelNet(Net):

    class Node(Net.Node):

        def __init__(self, value, pull_val_fptr=None, push_val_fptr=None):
            Net.Node.__init__(self, value)
            if pull_val_fptr is not None:
                self.pull_val = MethodType(pull_val_fptr, self)
            elif not hasattr(self, 'pull_val'):
                self.pull_val = None
            if push_val_fptr is not None:
                self.push_val = MethodType(push_val_fptr, self)
            elif not hasattr(self, 'push_val'):
                self.push_val = None

        def pull(self):
            self.value().set_ptr(self.pull_val())

        def push(self, value=None):
            if value is not None:
                self.value().set_ptr(value)
            update = {target: None for target in self.targets()}
            for target in self.targets():
                update[target] = self.push_val(target)
            for target, val in update.items():
                target.value().set_ptr(val)

    def __init__(self):
        Net.__init__(self)

        # dict<Pointer, float> representing new values
        self._next_values = {}

    def push(self, node, value):
        node = self.node(node)
        node.push(value)

    def pull(self, node):
        self.node(node).pull()

    def add(self, node, target=None, label=None):
        if target is None:
            return self.add_node(node)
        else:
            self.add_arc(node, target, label)


