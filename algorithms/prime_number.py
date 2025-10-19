def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def prime_numbers(limit):
    primes = []
    for num in range(2, limit+1):
        if is_prime(num):
            primes.append(num)
    return primes

# Input and Output
n = int(input("Enter the upper limit: "))
primes = prime_numbers(n)
print(f"Prime numbers up to {n}: {primes}")
