from interpreter import NodeVisitor
import inspect
from symtab_builder import SymbolTable, VarSymbol
from parser import UnaryOp, BinOp

# Semantic Analyzer traverses the syntax tree 
# and checks for invalid variable declarations 
# or invalid use of different types
class SemanticAnalyser(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable()

        # Set a global scope to be able to go through the tree
        self.GLOBAL_SCOPE = {}

    # This is the important part for type checking,
    # Other functions are written so that
    # the Analyser can traverse the tree
    def visit_Assign(self, node):
        # Type which user declared
        var_type = node.type.value

        # Value stored in the variable
        try:
            var_value = node.value.value

        # !! Can also be a BinOp or UnaryOp
        except AttributeError:
            var_value = node.value
            
            if isinstance(var_value, UnaryOp) or isinstance(var_value, BinOp):
                var_value = self.visit(node.value)
            else:
                self.type_error()


        # Type of value stored in variable
        var_value_type = type(var_value).__name__

        # Check if type declaration matches the type of the value
        if var_value_type != var_type:
            self.type_error()


        # Get the matching built-in type
        if var_type == 'int':
            type1 = self.symbol_table.get_symbol('int')
        elif var_type == 'str':
            type1 = self.symbol_table.get_symbol('str')
        elif var_type == 'float':
            type1 = self.symbol_table.get_symbol('float')
        elif var_type == 'bool':
            type1 = self.symbol_table.get_symbol('bool')
        else:
            raise Exception('Unsupported type declaration.')
        
        # Name of the variable
        var_name = node.name.value
        var_symbol = VarSymbol(var_name, type1)

        # Check if this variable was previously declared
        var_in_symtab = self.symbol_table.get_symbol(var_name)
        if var_in_symtab is not None:
            raise Exception(
                'DeclarationError: Duplicate assignment.'
            )
        
        # Insert in symbol table
        self.symbol_table.insert(var_symbol)

        # Global scope?
        var_name = node.name.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.value)


    def visit_BinOp(self, node):
        print(node.left)
        if node.op.type == 'PLUS':
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == 'MINUS':
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == 'MULT':
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == 'DIV':
            return self.visit(node.left) / self.visit(node.right)

    def visit_IfStatement(self, node):
        self.visit(node.value)

        for child in node.block.children:
            self.visit(child)
        if node.elseblock is not None:
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
        if op == 'PLUS':
            return +self.visit(node.expr)
        elif op == 'MINUS':
            return -self.visit(node.expr)

    def visit_Block(self, node):
        for child in node.children:
            self.visit(child)

    def visit_Empty(self, node):
        # If statement is empty, do nothing
        pass

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.symbol_table.get_symbol(var_name)

        if var_symbol is None:
            raise Exception("DeclarationError: Variable not defined.")

        # To keep going through the tree
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
            self.visit(node.expr)
        else:
            pass

    def type_error(self):
        raise Exception("TypeError: Invalid assignment.")