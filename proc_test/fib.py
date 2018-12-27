import sys


def fib(n):
    if n in [0, 1]:
        return n

    return fib(n - 1) + fib(n - 2)


if __name__ == '__main__':
    for _ in range(int(sys.argv[1])):
        fib(37)

