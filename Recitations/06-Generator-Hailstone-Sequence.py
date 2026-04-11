
def hailstone(num):
    '''
        >>> my_gen = hailstone(6) 
        >>> [item for item in my_gen]
        [6, 3, 10, 5, 16, 8, 4, 2, 1]
        >>> my_gen = hailstone(5) 
        >>> next(my_gen) 
        5
        >>> next(my_gen)
        16
        >>> next(my_gen)
        8
        >>> next(my_gen)
        4
        >>> next(my_gen)
        2
        >>> next(my_gen)
        1
        >>> next(my_gen)
        Traceback (most recent call last):
        StopIteration
    '''
    while num >= 1:
        yield num
        if num == 1:
            break
        elif num % 2 == 0:
            num = num // 2
        else:
            num = num * 3 + 1