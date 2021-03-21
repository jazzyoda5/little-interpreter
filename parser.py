from lexer import types, Token


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


class Comparison(AST):
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
    def __init__(self, name, value, type=None):
        self.name = name
        self.type = type
        self.value = value

class Var(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Value(AST):
    # Something that has only a value
    # Like a boolean or a string
    def __init__(self, value):
        self.value = value


class Print(AST):
    def __init__(self, expr):
        self.expr = expr


class IfStatement(AST):
    def __init__(self, value, block, elseblock=None):
        self.value = value
        self.block = block
        self.elseblock = elseblock


class Empty(AST):
    pass


"""
GRAMMAR ->

block  :  compound_statement
compound_statement  :  statement_list
statement_list  :  statement SCOLON
                   statement SCOLON statement_list
statement  =  block
              assignment
              empty
assignment  :  variable COLON TYPE EQUAL expr
var_value_change  :  variable EQUAL VALUE | expr
expr   : term ((PLUS | MINUS) term)*
term   : factor ((MUL | DIV) factor)*
factor : (PLUS | MINUS) factor | INTEGER | LPAREN expr RPAREN | variable
variable  :  NAME
print  :  PRINT (expr | STRING | BOOL)
ifelse  :  IF comparison LBRACE block RBRACE (ELSE LBRACE block RBRACE)
comparison  :  variable | VALUE | expr op expr
op  :  GRTHAN | LSTHAN
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
        nodes = self.statement_list()

        root = Block()
        for node in nodes:
            root.children.append(node)

        return root

    def statement_list(self):
        node = self.statement()
        results = [node]
        self.eat('SCOLON')

        while True:
            statement = self.statement()
            results.append(statement)

            if isinstance(statement, IfStatement):
                # if-else block doesn't require
                # a closing semicolon -> ';'
                pass
            elif self.curr_token.type != 'SCOLON':
                break
            else:
                self.eat('SCOLON')
            

        if self.curr_token.type == 'NAME':
            self.error()
        
        return results

    def statement(self):
        if self.curr_token.type == 'NAME':  
            node = self.assignment()

        elif self.curr_token.type == 'PRINT':
            node = self.print()
            
        elif self.curr_token.type == 'IF':
            node = self.ifelse()
            
        else:
            node = self.empty()
        
        return node

    def assignment(self):
        name = self.variable()
        # If next token is = 
        # This means (in correct syntax)
        # That variable was already previously defined
        # and that this statement only changes the value and not the type
        if self.curr_token.type == 'EQUAL':
            self.eat('EQUAL')

            if self.curr_token.type == 'BOOL':
                value = Value(self.curr_token.value)
                type_token = Token(value='bool', token_type='TYPE')
                node = Assign(name=name, value=value, type=type_token)
                self.eat('BOOL')
            else:
                node = self.expr()

            return node


        # Type must be declared ->
        self.eat('COLON')

        if self.curr_token.type == 'TYPE':
            var_type = self.curr_token
            self.eat('TYPE')
        else:
            self.error()

        self.eat('EQUAL')
        if self.curr_token.type == 'STRING':
            value = Value(value=self.curr_token.value)
            self.eat('STRING')
        elif self.curr_token.type == 'BOOL':
            value = Value(value=self.curr_token.value)
            self.eat('BOOL')
        else:
            value = self.expr()

        node = Assign(name, value, var_type)
        return node

    def factor(self):
        token = self.curr_token

        if token.type == 'PLUS':
            self.eat(types['+'])
            node = UnaryOp(token, self.factor())
            return node
        
        elif token.type == 'MINUS':
            self.eat(types['-'])
            node = UnaryOp(token, self.factor())
            return node

        elif token.type == 'INTEGER':
            self.eat('INTEGER')
            return Number(token)
        
        elif token.type == 'LPAREN':
            node = self.expr()
            self.eat(types['('])
            return node
        
        
        else:
            node = self.variable()
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
        return node
    
    def empty(self):
        empty = Empty()
        return empty

    def print(self):
        self.eat('PRINT')

        # Print has to be followed by
        # (). If not, raise a SyntaxError.
        if self.curr_token.type == 'LPAREN':
            self.eat('LPAREN')
            token = self.curr_token
            
            # Can contain a string, a boolean, or an expression
            if token.type == 'STRING':
                bellow_node = Value(value=self.curr_token.value)
                node = Print(expr=bellow_node)
                self.eat('STRING')

            elif token.type == 'BOOL':
                bellow_node = Value(value=self.curr_token.value)
                node = Print(expr=bellow_node)
                self.eat('BOOL')

            else:
                node = Print(expr=self.expr())
            
            self.eat('RPAREN')
            return node
        else:
            print('ERROR: ', self.curr_token)
            self.error()

    def ifelse(self):
        self.eat('IF')
        value = self.ifstatement()

        # if block is wrapped in {}
        self.eat('LBRACE')
        block=self.block()
        self.eat('RBRACE')
        
        if self.curr_token.type == 'ELSE':
            self.eat('ELSE')
            self.eat('LBRACE')
            elseblock = self.block()
            self.eat('RBRACE')
        else:
            elseblock = None

        node = IfStatement(value=value, block=block, elseblock=elseblock)
        return node  

    # Statement wrapped in ()
    # that determines if the if block
    # should run
    def ifstatement(self):
        self.eat('LPAREN')
        if self.curr_token.type == 'BOOL':
            node = Value(value=self.curr_token.value)
            self.eat('BOOL')
        elif self.curr_token.type == 'NAME':
            node = self.variable()
        else:
            print('hir')
            node = self.comparison()

        print('token: ', self.curr_token)
        self.eat('RPAREN')

        return node

    def comparison(self):
        left = self.expr()

        if self.curr_token.type == 'LSTHAN':
            op = self.curr_token
            self.eat('LSTHAN')
        elif self.curr_token.type == 'GRTHAN':
            op = self.curr_token
            self.eat('GRTHAN')
        else:
            self.error()

        node = Comparison(left=left, op=op, right=self.expr())
        return node
        

    
    def parse(self):
        node = self.block()
        if self.curr_token.type != 'EOF':
            self.error()
        
        return node
            


            