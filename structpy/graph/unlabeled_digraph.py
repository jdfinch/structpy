

from structpy.language import Specification


class UnlabeledDigraph(Specification):

    @Specification.example
    def digraph_access_patterns(self, Struct):
        graph = Struct()
        graph.add_arcs([
            ('a', 'b'),
            ('a', 'b'),
            ('b', 'c'),
            ('c', 'a'),
            ('a', 'c'),
            ('b', 'd'),
            ('d', 'a')
        ])

        assert graph.targets('a') == {'b', 'c'}
        assert graph.targets('a', 2) == {'b'}

        assert graph.sources('a') == {'c', 'd'}
        assert graph.sources('a', 5) == {'d'}

        assert graph.labels_out('a') == {1, 2, 4}
        assert graph.labels_out('a', 'b') == {1, 2}

        assert graph.labels_in('a') == {3, 5}
        assert graph.labels_in('a', 'd') == {5}

        assert graph.arcs_out('a') == {('a', 'b', 1), ('a', 'b', 2), ('a', 'c', 4)}
        assert graph.arcs_out('a', 'b') == {('a', 'b', 1), ('a', 'b', 2)}
        assert graph.arcs_out('a', label=1) == {('a', 'b', 1)}

        assert graph.arcs('a') == {('a', 'b', 1), ('a', 'b', 2), ('a', 'c', 4),
                                   ('c', 'a', 3), ('d', 'a', 5)}
        assert graph.arcs('a', 'b') == {('a', 'b', 1), ('a', 'b', 2)}
        assert graph.arcs('a', label=5) == {('d', 'a', 5)}



    @Specification.definition
    def this_is_my_method(self, Struct):
        """

        """
        struct = Struct()

