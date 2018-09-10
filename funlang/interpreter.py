from utils import error
from lexer import (
    Lexer, EOF, PLUS, MINUS, STAR, DIVISION, INTEGER, LPAREN, RPAREN
)


class Interpreter:

    def __init__(self, lexer):
        self.lexer = lexer

    def check_token(self, type_):
        token = self.lexer.get_next_token()
        if token.type != type_:
            error()
        else:
            return token

    def factor(self):
        if self.lexer.next_token.type == INTEGER:
            return self.lexer.get_next_token().value
        elif self.lexer.next_token.type == LPAREN:
            self.lexer.get_next_token()
            result = self.expr()
            self.check_token(RPAREN)
            return result
        error(self.lexer.next_token)

    def term(self):
        result = self.factor()

        while True:
            if self.lexer.next_token.type == STAR:
                self.lexer.get_next_token()
                result *= self.factor()
            elif self.lexer.next_token.type == DIVISION:
                self.lexer.get_next_token()
                result //= self.factor()
            else:
                break

        return result

    def expr(self):

        result = self.term()

        while True:
            if self.lexer.next_token.type == MINUS:
                self.lexer.get_next_token()
                result -= self.term()
            elif self.lexer.next_token.type == PLUS:
                self.lexer.get_next_token()
                result += self.term()
            else:
                break

        return result
