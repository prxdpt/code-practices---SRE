def rev(x):
    result = 0
    while x!= 0:
        digit = x % 10
        x //= 10

        result = result * 10 + digit 

    return result 

x = 123

j = rev(x)

print(j)