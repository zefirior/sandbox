from interpreter import Interpreter


def main():
    while True:
        text = input('input >>> ')

        if text:
            it = Interpreter(text)
            print(it.expr())
        else:
            break

if __name__ == '__main__':
    main()
