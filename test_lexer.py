from lexer import Lexer, Token


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



    




