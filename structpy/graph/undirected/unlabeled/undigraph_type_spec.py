
from structpy import specification


@specification
class UndigraphTypeSpec:
    """
    Abstract class for defining an undirected, unlabeled graph like Undigraph.
    """
    pass


if __name__ == '__main__':
    print(UndigraphTypeSpec.verify())