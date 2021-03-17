import sys
from lexer import Lexer
from parser import Parser

##############################################
# Interpreter
##############################################


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.tree = tree
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

    def visit_IfStatement(self, node):
        # IfStatement has two attributes
        # Value: Either a boolean or a comparison
        # to determine whether it's block should be executed
        # Block: Points to it's block of code inside {}
        should_execute = self.visit(node.value)

        if should_execute == True:
            for child in node.block.children:
                self.visit(child)
        elif should_execute == False and node.elseblock is not None:
            for child in node.elseblock.children:
                self.visit(child)

    def visit_Comparison(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op.type == 'LSTHAN':
            return left < right
        elif node.op.type == 'GRTHAN':
            return left > right

    def visit_Number(self, node):
        return node.value

    # example:
    # a = 5;
    # b = -a;
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
        print('type: ', node.type.value)
        var_name = node.name.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.value)

    def visit_Var(self, node):
        var_name = node.value
        value = self.GLOBAL_SCOPE.get(var_name)
        if value is None:
            raise NameError('Variable "{}" is not defined'.format(var_name))
        else:
            return value

    # For values that are not stored
    # in variables
    def visit_Value(self, node):
        return node.value

    def visit_Print(self, node):
        if node.expr is not None:
            print(self.visit(node.expr))
        else:
            print(node.value)

    def interpret(self):
        tree = self.tree
        if tree is None:
            return None

        self.visit(tree)


def main():
    file_path = sys.argv[1]
    try:
        f = open(file_path, 'r')
        text = f.read()
    except:
        print('Something went wrong.')

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
    tree = parser.parse()
    
    from semantic_analizer import SemanticAnalyser
    sem_analyzer = SemanticAnalyser()

    try:
        sem_analyzer.visit(tree)
    except Exception as exc:
        raise exc
        return
    

    interpreter = Interpreter(tree)
    interpreter.interpret() 
    

if __name__ == '__main__':
    main()

