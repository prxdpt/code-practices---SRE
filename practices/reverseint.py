def reverse(x: int) -> int:
    INT_MIN = -2147483648  # -2^31
    INT_MAX = 2147483647   #  2^31 - 1
    
    result = 0
    sign = 1 if x > 0 else -1
    x = abs(x)
    
    while x != 0:
        digit = x % 10
        x //= 10
        
        # Check overflow before multiplying by 10
        # result * 10 + digit > INT_MAX
        # => result > (INT_MAX - digit) / 10
        if result > (INT_MAX - digit) // 10:
            return 0
        
        result = result * 10 + digit
    
    return sign * result

x = 234

ans = reverse(x)

print(ans)