print("Hello World!")

for i in range(10):
    print(i, end = |)

    

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

print("the fib sequence is ", fib(3))

