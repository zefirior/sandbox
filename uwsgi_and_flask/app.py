from flask import Flask

app = Flask(__name__)


def fib(n):
    if n in (1, 0):
        return n

    return fib(n-1) + fib(n-2)


@app.route('/simple')
def simple():
    # fib(20)
    return "Hello world!"


@app.route('/hard')
def hard():
    fib(30)
    return "Hello world!"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
