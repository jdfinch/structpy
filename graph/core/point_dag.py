from structpy.graph.core.point_graph import PointGraph

class PointDag(PointGraph):

    def roots(self):
        """

        :return:
        """
        pass

    def leaves(self):
        """

        :return:
        """
        pass

    def sequences(self):
        """

        :return:
        """

    def traverse_reverse_postorder(self, start):
        for pro in self.pros(start):
            yield from self.traverse_reverse_postorder(pro)
        yield start

    def traverse_reverse_preorder(self, start):
        yield start
        for pro in self.pros(start):
            yield from self.traverse_reverse_preorder(pro)

    def traverse_postorder(self, start):
        for epi in self.epis(start):
            yield from self.traverse_postorder(epi)
        yield start

    def traverse_preorder(self, start):
        """
        (Preorder) Traverse the tree, starting at node `start`
        """
        yield start
        for epi in self.epis(start):
            yield from self.traverse_preorder(epi)
