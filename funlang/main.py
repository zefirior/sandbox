from lexer import Lexer
from interpreter import Interpreter


def test(text, expect_result):
    lexer = Lexer(text)
    it = Interpreter(lexer)
    result = it.expr()
    print('text          -> ', repr(text))
    print('expect_result -> ', repr(expect_result))
    print('result        -> ', repr(result))
    assert result == expect_result


def main():
    test('2-4+3*4-4', 6)
    test('2-4+  3 *4-4', 6)
    test('2-4/3*  4-4', -6)
    test(' (12- 4 )/3*  4-4', 4)

if __name__ == '__main__':
    main()
