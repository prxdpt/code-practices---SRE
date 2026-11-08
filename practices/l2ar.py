def second_largester(arr):
    if len(arr) < 2 :
        return None


    largest = 0
    second_largest = 0


    for num in arr:
        if num > largest:
            second_largest = largest
            largest = num

        elif num > second_largest and num != largest :
            second_largest = num 


    return second_largest


x = [1,3,37,376437,29,2,232]

j = second_largester(x)

print(j)