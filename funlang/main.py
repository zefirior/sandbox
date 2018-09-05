from interpreter import Interpreter

def main():
    # while True:
    it = Interpreter('3+6')
    print(it.expr())
    it = Interpreter('3+4')
    print(it.expr())


if __name__ == '__main__':
    main()
