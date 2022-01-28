
import inspect, ast
from pprint import pprint


def foo(x, y):
    z = x + y
    l = [x, y, z]
    assert len(l) == 3
    return l


def dynafunc(obj, *affixes, sep='_'):
    method_name = sep.join(affixes)
    if hasattr(obj, method_name):
        attr = getattr(obj, method_name)
        if callable(attr):
            return attr


class Rewriter(ast.NodeTransformer):

    def visit_Assert(self, node):
        replacer = dynafunc(self, 'replace', node.__class__.__name__)
        if replacer:
            return replacer(node)
        else:
            self.generic_visit(node)
            return node

    def replace_Compare(self, node):
        print('Replacing', node)
        return node



def recode(f):
    tree = ast.parse(inspect.getsource(f)).body[0]
    new_tree = Rewriter().visit(tree)
    print()
    print(ast.dump(tree))
    print()
    print(ast.dump(new_tree))
    return foo


if __name__ == '__main__':
    bar = recode(foo)