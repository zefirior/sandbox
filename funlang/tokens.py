INTEGER = 'INTEGER'
PLUS = 'PLUS'
MINUS = 'MINUS'
STAR = 'STAR'
DIVISION = 'DIVISION'
EOF = 'EOF'


class Token:
    """
        класс токенов имеет тип и содержит значение
    """

    define_types = {
        INTEGER,
        PLUS,
        MINUS,
        STAR,
        DIVISION,
        EOF,
    }

    def __init__(self, token_type, token_value):
        if token_type not in self.define_types:
            raise Exception('Токен не зарезервирован')

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


class TokenMinus(TokenOp):
    expect_char = '-'

    def __init__(self, value):
        super().__init__(MINUS, value)


class TokenStar(TokenOp):
    expect_char = '*'

    def __init__(self, value):
        super().__init__(STAR, value)


class TokenDivision(TokenOp):
    expect_char = '/'

    def __init__(self, value):
        super().__init__(DIVISION, value)


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

