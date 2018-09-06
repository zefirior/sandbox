from interpreter import Interpreter


def main():
    while True:
        text = input('input >>> ')

        if text:
            it = Interpreter(text)
            it.expr()
            print(it.tokens)
        else:
            break

if __name__ == '__main__':
    main()
