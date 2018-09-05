INTEGER = 'INTEGER'
PLUS = 'PLUS'
EOF = 'EOF'

class Token:
    """
        класс токенов имеет тиип и содержит значение
    """

    define_types = {
        INTEGER,
        PLUS,
        EOF,
    }

    def __init__(self, token_type, token_value):
        if token_type not in self.define_types:
            raise Exception('Токен не зарезервирован')

        self._type = token_type
        self._value = token_value

    def __str__(self):
        return '<Token type={}, value={}>'.format(self._type, repr(self._value))

    @property
    def value(self):
        return self._value

    @property
    def type(self):
        return self._type


class TokenInt(Token):

    def __init__(self, value):
        super().__init__(INTEGER, value)

    def validate_first_char(self, char):
        if char.isdigit():
            return True
        else:
            return False

    def validate_char(self, char):
        if char.isdigit():
            return True
        else:
            return False


class TokenOp(Token):

    def __init__(self, type_, value):
        super().__init__(type_, value)

    def validate_first_char(self, char):
        if char in '+-':
            return True
        else:
            return False

    def validate_char(self, char):
        if char in '+-':
            return True
        else:
            return False

