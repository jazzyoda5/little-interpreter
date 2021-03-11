# Types
INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
MULT = 'MULT'
DIV = 'DIV'
STRING = 'STRING'
EOF = 'EOF'
ELSE = 'ELSE'
IF = 'IF'
EQUAL = 'EQUAL'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
LBRACE = 'LBRACE'
RBRACE = 'RBRACE'
NAME = 'NAME'
PRINT = 'PRINT'
GRTHAN = 'GRTHAN'


class Token(object):
    def __init__(self, token_type, value):
        self.value = value
        self.type = token_type

    def __str__(self):
        return 'Token(' + str(self.type) + ', ' + str(self.value) + ')'


class Lexer(object):
    def __init__(self, text):
        self.pos = 0
        self.text = text
        self.current_char = self.text[self.pos]

    def get_next_token(self):
        if self.pos > len(self.text) - 1:
            return Token(EOF, None)

        if self.current_char.isspace():
            self.skip_whitespace()

        if self.current_char.isdigit():
            token = self.integer()
            return token

        if self.current_char == '+':
            self.advance()
            return Token(PLUS, '+')

        if self.current_char == '-':
            self.advance()
            return Token(MINUS, '-')

        if self.current_char == '*':
            self.advance()
            return Token(MULT, '*')

        if self.current_char == '/':
            self.advance()
            return Token(DIV, '/')

        if self.current_char == '(':
            self.advance()
            return Token(LPAREN, '(')

        if self.current_char == ')':
            self.advance()
            return Token(RPAREN, ')')

        if self.current_char == '{':
            self.advance()
            return Token(LBRACE, '{')

        if self.current_char == '}':
            self.advance()
            return Token(RBRACE, '}')

        if self.current_char == '=':
            self.advance()
            return Token(EQUAL, '=')
        
        if self.current_char == '>':
            self.advance()
            return Token(GRTHAN, '>')

        if self.current_char == '"':
            token = self.string()
            return token

        if self.current_char.isalpha():
            # Might be ELSE, IF, or NAME
            token = self.name()
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

    def skip_whitespace(self):
        # Skips all the whitespaces
        while True:
            self.advance()
            if not self.current_char.isspace():
                break

    def integer(self):
        # Returns an INTEGER token
        number = ''
        while self.current_char.isdigit():
            number += self.current_char
            self.advance()    
        
        return Token(INTEGER, int(number))

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
            

        if self.current_char == '"' and self.pos < len(self.text) - 1:
            self.advance()
        elif self.pos == len(self.text) - 1:
            # If it is the end of the file
            # Only move the position so lexer 
            # will get EOF for the next token
            self.pos += 1

        return Token(STRING, string)

    def name(self):
        # This language only supports alphabetical 
        # variable names (for now)
        name = ''
        while self.current_char.isalpha():
            name += self.current_char
            self.advance()

        # Check if it is PRINT, ELSE or IF
        if name == 'else':
            return Token(ELSE, 'else')
        if name == 'if':
            return Token(IF, 'if')
        if name == 'print':
            return Token(PRINT, 'print')

        return Token(NAME, name)

    def error(self):
        raise Exception('LexerError')
