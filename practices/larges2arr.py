def second_largest_one_pass(arr):
    if len(arr) < 2:
        return None
    
    largest = second_largest = float('-inf')
    
    for num in arr:
        if num > largest:
            second_largest = largest
            largest = num
        elif num > second_largest and num != largest:
            second_largest = num
    
    return None if second_largest == float('-inf') else second_largest


x = [3,8,9,0,7,9827864,7272,9090,0]

g = second_largest_one_pass(x)

print(g)