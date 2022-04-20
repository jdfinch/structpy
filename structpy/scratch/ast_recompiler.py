
import inspect
import ast


def foo(x, y):
    """
    my comment
    """
    z = x + y
    a = z + x + y
    return z


class MyVisitor(ast.NodeVisitor):

    def __init__(self):
        ast.NodeVisitor.__init__(self)
        code = 'x = x + 10'
        self.ast = ast.parse(code)

    def visit_FunctionDef(self, fn):
        fn.body.insert(0, self.ast)


visitor = MyVisitor()
source = inspect.getsource(foo)
source_tree = ast.parse(source)
visitor.visit(source_tree)
target = ast.unparse(source_tree)
print(target)
recompiled = compile(target, '<string>', 'exec')
exec(recompiled)
result = foo(3, 4)
print(result)