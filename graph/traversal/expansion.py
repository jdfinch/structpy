
def expand_targets(graph, step):
    yield from graph.targets(step.node)


