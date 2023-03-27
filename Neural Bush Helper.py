#Bush helper
import everything as ev

# basic math:
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a/b

def exponent(a, b):
    return a ** b

def root(a, b):
    return a ** (1/b)

def main():
    print(add(2, 2))
    print(multiply(2, 3))
    print(divide(4, 2))
    print(exponent(4, 2))
    print(root(9, 2))

main()