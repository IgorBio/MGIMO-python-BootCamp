def foo(n):
    result = 0
    for i in range(n):
        print(i)
        result += i
    return result
print(foo(10))
