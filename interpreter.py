from lexer import Lexer, Token


class Interpreter(object):
    def __init__(self, text):
        self.text = text
        self.lexer = Lexer(text)

    def all_tokens(self):
        tokens = []

        while True:
            token = self.lexer.get_next_token()
            tokens.append(token)

            if token.type == 'EOF':
                break
        
        return tokens


def main():
    file_path = input('File Path: ')
    f = open(file_path, 'r')
    text = f.read()
    interpreter = Interpreter(text)
    all_tokens = interpreter.all_tokens()
    for token in all_tokens:
        print(token.__str__())
    

if __name__ == '__main__':
    main()

