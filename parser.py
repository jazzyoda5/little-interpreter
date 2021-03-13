from lexer import types


class AST(object):
    pass


class Number(AST):
    def __init__(self, token):
        self.value = token.value
        self.token = token


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
        self.token = self.op


class UnaryOp(AST):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class Block(AST):
    def __init__(self):
        self.children = []


class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Empty(AST):
    pass


"""
GRAMMAR ->

block  :  statement_list 
statement_list  :  statement SCOLON
                   statement SCOLON statement_list
statement  =  block
              assignment
              empty
assignment  :  variable EQUAL expr
expr   : term ((PLUS | MINUS) term)*
term   : factor ((MUL | DIV) factor)*
factor : (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN
variable  :  NAME
"""

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.curr_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # Check if curr_token's type matches the passed in type
        if self.curr_token.type == token_type:
            self.curr_token = self.lexer.get_next_token()
        else:
            self.error()

    def block(self):
        node = self.compound_statement()
        return node

    def compound_statement(self):
        """
        compound_statement: BEGIN statement_list END
        """
        nodes = self.statement_list()

        root = Block()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        node = self.statement()
        results = [node]

        while self.curr_token.type == types[';']:
            self.eat(types[';'])
            results.append(self.statement())

        if self.curr_token.type == 'NAME':
            self.error()
        
        return results

    def statement(self):
        if self.curr_token.type == 'NAME':
            node = self.assignment()
        else:
            node = self.empty()
        
        print('statement node: ', node)
        return node

    def assignment(self):
        left = self.variable()
        token = self.curr_token
        self.eat('EQUAL')
        print('right: ', self.curr_token)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def factor(self):
        token = self.curr_token

        if token.type == types['+']:
            self.eat(types['+'])
            node = UnaryOp(token, self.factor())
            return node
        
        elif token.type == types['-']:
            self.eat(types['-'])
            node = UnaryOp(token, self.factor())
            return node

        elif token.type == types['int']:
            self.eat('INTEGER')
            print('factor: ', token)
            return Number(token)
        
        elif token.type == types['(']:
            node = self.expr()
            self.eat(types['('])
            return node
        
        
        else:
            node = self.variable()
            print('factor: ', node)
            return node

    def expr(self):
        node = self.term()

        while self.curr_token.type in ('PLUS', 'MINUS'):
            token = self.curr_token

            if token.type == 'PLUS':
                self.eat('PLUS')
            
            elif token.type == 'MINUS':
                self.eat('MINUS')

            node = BinOp(left=node, op=token, right=self.term())

        return node
            

    def term(self):
        node = self.factor()

        while self.curr_token.type in ('MULT', 'DIV'):
            token = self.curr_token

            if token.type == 'MULT':
                self.eat('MULT')
            
            elif token.type == 'DIV':
                self.eat('DIV')

            node = BinOp(left=node, op=token, right=self.factor())
        
        return node
    
    def variable(self):
        node = Var(self.curr_token)
        self.eat('NAME')
        print('variable node: ', node)
        return node
    
    def empty(self):
        empty = Empty()
        print('empty node: ', empty)
        return empty
    
    def parse(self):
        node = self.block()
        if self.curr_token.type != 'EOF':
            self.error()
        
        print('main parse node: ', node)
        return node
            


            