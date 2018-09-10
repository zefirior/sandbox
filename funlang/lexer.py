from utils import error

INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
STAR = 'STAR'
DIVISION = 'DIVISION'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
EOF = 'EOF'


class Lexer:
    token_type = []

    def __init__(self, text):
        self.text = text
        self.pos = -1
        # self.tokens = []
        self._current_token = None
        self._next_token = None
        self.get_next_token()

    def _try_next_char(self):
        if self.pos + 2 > len(self.text):
            return None
        else:
            return self.text[self.pos + 1]

    def _shift_parse_token(self):

        while True:
            next_char = self._try_next_char()
            if next_char is not None and next_char.isspace():
                self.pos += 1
            else:
                break

        next_char = self._try_next_char()
        token = None

        if next_char is None:
            token = TokenEOF(None)
        else:

            for token_class in self.token_type:
                if token_class.validate_first_char(next_char):
                    token = token_class(next_char)
                    break

            if token is None:
                print(next_char)
                error()

            self.pos += 1

            while True:
                char = self._try_next_char()
                if char is None:
                    break

                if token.validate_char(char):
                    self.pos += 1
                    token.add_char(char)
                else:
                    break

        token.prepare_value()
        # self.tokens.append(token)

        return token

    @property
    def next_token(self):
        return self._next_token

    def get_next_token(self):
        self._current_token = self._next_token
        self._next_token = self._shift_parse_token()
        return self._current_token


class Token:
    """
        класс токенов имеет тип и содержит значение
    """

    def __init__(self, token_type, token_value):

        self._type = token_type
        self._value = token_value

    def __str__(self):
        return '<Token type={}, value={}>'.format(self._type, repr(self._value))

    def __repr__(self):
        return self.__str__()

    def add_char(self, char):
        self._value += char

    def prepare_value(self):
        pass

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type


class TokenInt(Token):

    def __init__(self, value):
        super().__init__(INTEGER, value)

    def prepare_value(self):
        self._value = int(self._value)

    @staticmethod
    def validate_first_char(char):
        if char.isdigit():
            return True
        else:
            return False

    @staticmethod
    def validate_char(char):
        if char.isdigit():
            return True
        else:
            return False
Lexer.token_type.append(TokenInt)


class TokenOp(Token):
    expect_char = None

    @classmethod
    def validate_first_char(cls, char):
        if char in cls.expect_char:
            return True
        else:
            return False

    @staticmethod
    def validate_char(char):
        return False


class TokenPlus(TokenOp):
    expect_char = '+'

    def __init__(self, value):
        super().__init__(PLUS, value)
Lexer.token_type.append(TokenPlus)


class TokenMinus(TokenOp):
    expect_char = '-'

    def __init__(self, value):
        super().__init__(MINUS, value)
Lexer.token_type.append(TokenMinus)


class TokenStar(TokenOp):
    expect_char = '*'

    def __init__(self, value):
        super().__init__(STAR, value)
Lexer.token_type.append(TokenStar)


class TokenDivision(TokenOp):
    expect_char = '/'

    def __init__(self, value):
        super().__init__(DIVISION, value)
Lexer.token_type.append(TokenDivision)


class TokenParen(Token):
    expect_char = None

    @classmethod
    def validate_first_char(cls, char):
        if char in cls.expect_char:
            return True
        else:
            return False

    @staticmethod
    def validate_char(char):
        return False


class TokenLParen(TokenParen):
    expect_char = '('

    def __init__(self, value):
        super().__init__(LPAREN, value)
Lexer.token_type.append(TokenLParen)


class TokenRParen(TokenParen):
    expect_char = ')'

    def __init__(self, value):
        super().__init__(RPAREN, value)
Lexer.token_type.append(TokenRParen)


class TokenEOF(Token):

    def __init__(self, value):
        super().__init__(EOF, value)

    @staticmethod
    def validate_first_char(char):
        if char is None:
            return True
        else:
            return False

    @staticmethod
    def validate_char(char):
        return False
Lexer.token_type.append(TokenEOF)
