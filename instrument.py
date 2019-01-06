import ast
import astor
import os
import astunparse


def get_instrument_decorator(type_):
    return ast.Call(func=ast.Name(id='instrument_decorator', ctx=ast.Load()), args=[ast.Call(func=ast.Attribute(value=ast.Attribute(value=ast.Name(id='os', ctx=ast.Load()), attr='path', ctx=ast.Load()), attr='realpath', ctx=ast.Load()), args=[ast.Name(id='__file__', ctx=ast.Load())], keywords=[]), ast.Str(s=type_)], keywords=[])


class Instrumenter(ast.NodeTransformer):
    def visit_Module(self, node):
        for n in node.body:
            if isinstance(n, [ast.FunctionDef, ast.AsyncFunctionDef]):
                n.decorator_list = [get_instrument_decorator(
                    "function")] + n.decorator_list
            elif isinstance(n, ast.ClassDef):
                for subn in n.body:
                    if isinstance(subn, [ast.FunctionDef, ast.AsyncFunctionDef]):
                        args = [nn.arg for nn in subn.args.args]
                        if 'self' in args:
                            subn.decorator_list = [get_instrument_decorator(
                                "method")] + subn.decorator_list
        node.body = [ast.Import(names=[ast.alias(name='os', asname=None)]), ast.ImportFrom(
            module='instrument_decorator', names=[ast.alias(name='instrument_decorator', asname=None)], level=0)] + node.body


def collect_py_files(path):
    files = []

    def travel(path):
        if os.path.isdir(path):
            names = os.listdir(path)
            for name in names:
                new_path = os.path.join(path, name)
                travel(new_path)
        elif os.path.isfile(path) and path.endswith('.py'):
            files.append(path)

    travel(path)
    return files


def instrument_one(file):
    root = astor.parse_file(file)


def instrument(files):
    for file in files:
        instrument_one(file)


def main():
    files = collect_py_files('pydantic')
    for file in files:
        root = astor.parse_file(file)
        transformer = Instrumenter()
        transformer.visit(root)
        with open(file, mode='w', encoding='utf-8') as wf:
            wf.write(astunparse.unparse(root))


if __name__ == '__main__':
    main()
