import pytest
import os
from lexer import Lexer, Token
import parser
from interpreter import Interpreter


##################################
# LEXER METHODS
##################################

def test_skip_whitespace():
    lexer = Lexer('awd   d l p   ')

    # Go to 3rd position
    for _ in range(3):
        lexer.advance()
    
    # Skip the whitespaces
    lexer.skip_whitespace()
    assert lexer.pos == 6
    assert lexer.current_char == 'd'

    # Now at 7th pos
    lexer.advance()
    lexer.skip_whitespace()
    assert lexer.pos == 8
    assert lexer.current_char == 'l'

def test_advance():
    lexer = Lexer('a8s64g')
    assert lexer.pos == 0
    assert lexer.current_char == 'a'

    lexer.advance()
    assert lexer.pos == 1
    assert lexer.current_char == '8'

    lexer.advance()
    assert lexer.pos == 2
    assert lexer.current_char == 's'

    lexer.advance()
    assert lexer.pos == 3
    assert lexer.current_char == '6'

def test_string():
    lexer = Lexer('"Some string" + a')
    token = lexer.get_next_token()
    assert token.type == 'STRING'
    assert token.value == 'Some string'
    assert lexer.pos == 13
    assert lexer.current_char == ' '

    lexer = Lexer('   whatever    "Some Stringggg"')
    for _ in range(12):
        lexer.advance()
    assert lexer.current_char == ' '
    token = lexer.get_next_token()
    assert token.type == 'STRING'
    assert token.value == 'Some Stringggg'
    token = lexer.get_next_token()
    assert token.type == 'EOF'

    lexer = Lexer('"Some string" + a')
    token = lexer.get_next_token()
    assert token.type == 'STRING'
    assert token.value == 'Some string'
    assert lexer.pos == 13
    assert lexer.current_char == ' '

def test_name():
    lexer = Lexer('else if a')

    token1 = lexer.get_next_token()
    assert token1.type == 'ELSE'
    assert token1.value == 'else'

    token2 = lexer.get_next_token()
    assert token2.type == 'IF'
    assert token2.value == 'if'

    token3 = lexer.get_next_token()
    assert token3.type == 'NAME'
    assert token3.value == 'a'


##################################
# PARSER TESTS
##################################

def get_ast(text):
    lexer = Lexer(text)
    parser_obj = parser.Parser(lexer)
    tree = parser_obj.parse()
    return tree


def get_parser(text):
    lexer = Lexer(text)
    parser_obj = parser.Parser(lexer)
    return parser_obj


# Opens and reads an example file
def get_example(id):
    file_name = str(id) + '.txt'
    f = open(os.path.dirname(os.path.abspath(__file__)) + '/test_examples/' + file_name, 'r')
    return f.read()


def test_parser_print(file_id=1):
    text = get_example(file_id)
    tree = get_ast(text)
    
    assert isinstance(tree, parser.Block)
    assert tree.children is not None

    node = tree.children[0]
    assert  isinstance(node, parser.Print)

    # Print object has an expr attribute -> item or expression you want to output
    expr = node.expr
    assert expr


    




