from token import Token, INTEGER, PLUS, EOF

class Interpreter:

    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_token = None

    def error(self):
        raise Exception('Что-то не так')

    def try_next_char(self):
        return self.text[self.pos + 1]

    def get_next_token(self):
        token = None

        if self.pos + 2 > len(self.text):
            self.current_token = token.type
            token = Token(EOF, EOF)


        self.pos += 1

        else:
            char = self.text[self.pos]
            if char.isdigit():
                token = Token(INTEGER, int(char))
            elif char == '+':
                token = Token(PLUS, char)
            else:
                self.error()

        self.current_token = token.type
        return token

    def chank(self, expect_token_type):
        token = self.get_next_token()
        if token.type == expect_token_type:
            return token
        else:
            self.error()

    def expr(self):

        left = self.chank(INTEGER)
        op = self.chank(PLUS)
        right = self.chank(INTEGER)
        self.chank(EOF)

        return left.value + right.value

