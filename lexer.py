# Types
types = {
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'MULT',
    '/': 'DIV',
    'EOF': 'EOF',
    '=': 'EQUAL',
    '(': 'LPAREN',
    ')': 'RPAREN',
    '{': 'LBRACE',
    '}': 'RBRACE',
    'name': 'NAME',
    'bool': 'BOOL',
    ';': 'SCOLON',
    '>': 'GRTHAN',
    '<': 'LSTHAN',
    'id': 'ID',
    ':': 'COLON',
    'type_decl': 'TYPE'
}

# Special reserved words
reserved_names = {
    'print': 'PRINT',
    'else': 'ELSE',
    'if': 'IF',
    'str': 'TYPE',
    'int': 'TYPE',
    'bool': 'TYPE',
    'True': 'BOOL',
    'False': 'BOOL',
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

        # Check if it is one of the reserved words
        res_name_type = reserved_names.get(name)
        if res_name_type is not None:

            # For booleans assign boolean value 
            # instead of string
            if name == 'True':
                return Token(res_name_type, True)
            if name == 'False':
                return Token(res_name_type, False)

            return Token(res_name_type, name)

        return Token('NAME', name)

    def error(self):
        raise Exception('SyntaxError')
