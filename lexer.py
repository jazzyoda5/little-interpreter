# Types
types = {
    'int': 'INTEGER',
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MULT',
    '/': 'DIV',
    'str': 'STRING',
    'EOF': 'EOF',
    'else': 'ELSE',
    'if': 'IF',
    '=': 'EQUAL',
    '(': 'LPAREN',
    ')': 'RPAREN',
    '{': 'LBRACE',
    '}': 'RBRACE',
    'name': 'NAME',
    'print': 'PRINT',
    'bool': 'BOOL',
    ';': 'SCOLON',
    '>': 'GRTHAN',
    '<': 'LSTHAN',
    'id': 'ID'
}


class Token(object):
    def __init__(self, token_type, value):
        self.value = value
        self.type = token_type

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Lexer(object):
    def __init__(self, text):
        self.pos = 0
        self.text = text
        self.current_char = self.text[self.pos]

    def get_next_token(self):
        if self.pos > len(self.text) - 1:
            return Token('EOF', None)
        
        if self.current_char.isspace():
            self.skip_whitespace()

            # Check for EOF
            if self.current_char == None and self.pos > len(self.text) - 1:
                return Token('EOF', None)


        if self.current_char == '/' and self.peek() == '*':
            self.skip_comment()

        if self.current_char.isdigit():
            token = self.integer()
            return token

        if self.current_char == '"':
            token = self.string()
            return token

        if self.current_char.isalpha():
            # Might be ELSE, IF, or NAME
            token = self.name()
            return token

        if self.current_char in types:
            token = Token(types[self.current_char], self.current_char)
            self.advance()
            return token

        print(self.current_char)
        self.error()

    def advance(self):
        # Moves to next position and sets
        # the next current character
        if self.pos < len(self.text) - 1:
            self.pos += 1
            self.current_char = self.text[self.pos]
        else:
            self.pos += 1
            self.current_char = None

    def peek(self):
        if self.pos < len(self.text) - 1:
            new_pos = self.pos + 1
            next_char = self.text[new_pos]
            return next_char
        return None

    def skip_whitespace(self):
        # Skips all the whitespaces
        while True:
            self.advance()
            if self.current_char is None:
                break
            if not self.current_char.isspace():
                break

    def skip_comment(self):
        # Skip everything until comment is closed off
        # With */
        while True:
            self.advance()
            if self.current_char == '*' and self.peek() == '/':
                self.advance()
                break
        
        if self.current_char == '/':
            self.advance()
        if self.current_char.isspace():
            self.skip_whitespace()


    def integer(self):
        # Returns an INTEGER token
        number = ''
        while self.current_char.isdigit():
            number += self.current_char
            self.advance()   

            if self.current_char == None:
                break 

        return Token('INTEGER', int(number))

    def string(self):
        # Returns a STRING token
        if self.current_char == '"':
            self.advance()
        else:
            self.error()

        string = ''

        while self.current_char != '"':
            string += self.current_char
            self.advance()
            
            if self.current_char == '"':
                self.advance()
                break

        return Token('STRING', string)

    def name(self):
        # This language only supports alphabetical 
        # variable names (for now)
        name = ''
        while self.current_char.isalpha():
            name += self.current_char
            self.advance()

            if self.current_char == None:
                break

        # Check if it is PRINT, ELSE or IF
        if name == 'else':
            return Token('ELSE', 'else')
        if name == 'if':
            return Token('IF', 'if')
        if name == 'print':
            return Token('PRINT', 'print')
        if name == 'True':
            return Token('BOOL', True)
        if name == 'False':
            return Token('BOOL', False)

        return Token('NAME', name)

    def error(self):
        raise Exception('SyntaxError')
