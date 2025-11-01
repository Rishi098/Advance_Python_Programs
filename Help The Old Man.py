def hanoi(n, source, auxiliary, target):
    if n == 1:
        print(f"{n}:{source}->{target}")
        return
    hanoi(n - 1, source, target, auxiliary)
    print(f"{n}:{source}->{target}")
    hanoi(n - 1, auxiliary, source, target)

N = int(input().strip())
hanoi(N, 'A', 'B', 'C')
