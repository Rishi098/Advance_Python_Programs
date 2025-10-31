import time
start = time.time()

sum = 0
for i in range(1000000):
    sum += i

end = time.time()
print(f"Execution time: {end - start:.5f} sec")
