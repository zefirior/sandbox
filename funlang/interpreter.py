from token import TokenInt, TokenMinus, TokenPlus, TokenEOF, EOF

class Interpreter:

    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.tokens = []
        self.current_token = None
        self.token_type = [TokenInt, TokenMinus, TokenPlus, TokenEOF]

    def error(self):
        raise Exception('Что-то не так')

    def try_next_char(self):
        if self.pos + 2 > len(self.text):
            return None
        else:
            return self.text[self.pos + 1]

    def get_next_token(self):
        next_char = self.try_next_char()
        token = None

        if next_char is None:
            token = TokenEOF(None)
        else:

            for token_class in self.token_type:
                if token_class.validate_first_char(next_char):
                    token = token_class(next_char)

            if token is None:
                print(next_char)
                self.error()

            self.pos += 1

            while True:
                char = self.try_next_char()
                if char is None:
                    break

                if token.validate_char(char):
                    self.pos += 1
                    token.add_char(char)
                else:
                    break

        self.tokens.append(token)

        return token

    def expr(self):

        while True:
            token = self.get_next_token()
            if token.type == EOF:
                break

        
