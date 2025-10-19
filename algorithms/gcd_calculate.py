#Description: This program calculates the GCD of two numbers using Euclid's algorithm.
#Features: Efficient method to find the greatest common divisor.

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# Input and Output
a = int(input("Enter the first number: "))
b = int(input("Enter the second number: "))

print(f"The GCD of {a} and {b} is {gcd(a, b)}")
