import ast
import inspect
from typing import Callable

# Проверка на то, используется ли функция func_name в функции func
def checkUsageFunction(func: Callable, func_name: str):
    try:
        source = inspect.getsource(func)
        tree = ast.parse(source)
        
        class VaSpeakCallVisitor(ast.NodeVisitor):
            def __init__(self):
                self.found = False
            
            def visit_Call(self, node):
                if (isinstance(node.func, ast.Name) and 
                    node.func.id == func_name):
                    self.found = True
                self.generic_visit(node)
        
        visitor = VaSpeakCallVisitor()
        visitor.visit(tree)
        return visitor.found
        
    except Exception as e:
        print(f"Ошибка AST анализа {func.__name__}: {e}")
        return False