import math


def _decompose(n, rest):
    if rest == 0:
        return []
    if rest < 1:
        return None

    n = min(n, int(math.sqrt(rest)) + 1)
    for i in range(n-1, 0, -1):
        stack = _decompose(i, rest - i**2)
        if stack is not None:
            return stack + [i]

    return None


def decompose(n):
    return _decompose(n, n**2)

print(decompose(20))