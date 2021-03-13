from lexer import Lexer
from parser import Parser


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.GLOBAL_SCOPE = {}
    
    def visit_BinOp(self, node):
        if node.op.type == 'PLUS':
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == 'MINUS':
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == 'MULT':
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == 'DIV':
            return self.visit(node.left) / self.visit(node.right)

    def visit_Number(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)

    def visit_Block(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Empty(self, node):
        # If statement is empty, do nothing
        pass

    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)
        

    def visit_Var(self, node):
        var_name = node.value
        value = self.GLOBAL_SCOPE.get(var_name)
        if value is None:
            raise NameError('Variable "{}" is not defined'.format(var_name))
        else:
            return value

    def visit_Value(self, node):
        return node.value

    def visit_Print(self, node):
        if node.expr is not None:
            print(self.visit(node.expr))
        else:
            print(node.value)

    def interpret(self):
        tree = self.parser.parse()
        self.visit(tree)


def main():
    while True:
        file_path = input('File Path: ')
        try:
            f = open(file_path, 'r')
            text = f.read()
        except:
            break

        """
        lexer_check = Lexer(text)
        while True:
            token = lexer_check.get_next_token()
            print(token)
            if token.type == 'EOF':
                break
        """
        
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        interpreter.interpret()
        
    
    

if __name__ == '__main__':
    main()

