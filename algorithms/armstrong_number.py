#Description: This program checks if a given number is an Armstrong number. A number is an Armstrong number if the sum of its digits raised to the power of the number of digits is equal to the number itself.
#Features: Works for both small and large numbers.
def is_armstrong(number):
    num_str = str(number)
    num_digits = len(num_str)
    sum_of_powers = sum(int(digit) ** num_digits for digit in num_str)
    return sum_of_powers == number

# Input and Output
num = int(input("Enter a number: "))
if is_armstrong(num):
    print(f"{num} is an Armstrong number.")
else:
    print(f"{num} is not an Armstrong number.")
