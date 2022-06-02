
import inspect
import ast
import textwrap


class RecompiledFunction:

    def __init__(self, f, globals=None, locals=None, keep_code=False):
        locals = {} if locals is None else locals
        globals = {} if globals is None else globals
        before_source = textwrap.dedent(inspect.getsource(self.before))
        after_source = textwrap.dedent(inspect.getsource(self.after))
        before_tree = ast.parse(before_source).body[0].body
        after_tree = ast.parse(after_source).body[0].body

        class Visitor(ast.NodeVisitor):

            def __init__(self, before=None, after=None):
                ast.NodeVisitor.__init__(self)
                self.before = before
                self.after = after

            def visit_FunctionDef(self, fn):
                if self.before:
                    for line in reversed(self.before):
                        fn.body.insert(0, line)
                if self.after:
                    fn.body.extend(self.after)

            def visit_Return(self, ret):
                ...

        visitor = Visitor(before_tree, after_tree)

        source = textwrap.dedent(inspect.getsource(f))
        tree = ast.parse(source)
        visitor.visit(tree)
        if keep_code:
            self.code = ast.unparse(tree)
        else:
            self.code = None
        target = compile(tree, '<string>', 'exec')
        exec(target, globals, locals)
        self.recompiled_function = locals[f.__name__]
        return

    def before(self, *args, **kwargs):
        ...

    def after(self, *args, **kwargs):
        ...

    def __call__(self, *args, **kwargs):
        return self.recompiled_function(*args, **kwargs)


if __name__ == '__main__':


    def foo(x, y):
        z = x + y
        return z

    class RecompiledFoo(RecompiledFunction):
        def before(self, x):
            print('before:', x)
            x = x + 10
        def after(self, z):
            print('After:', z)

    recompiled_foo = RecompiledFoo(foo)

    result = recompiled_foo(3, 4)
    print(result)