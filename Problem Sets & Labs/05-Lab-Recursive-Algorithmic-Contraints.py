
def is_power_of(base, num):
    """
        >>> is_power_of(5, 625)  # pow(5, 4) = 5 * 5 * 5 * 5 = 625
        True
        >>> is_power_of(5, 1)    # pow(5, 0) = 1
        True
        >>> is_power_of(5, 5)    # pow(5, 1) = 5
        True
        >>> is_power_of(5, 15)   # 15 is not a power of 5 (it's a multiple)
        False
        >>> is_power_of(3, 9)
        True
        >>> is_power_of(3, 8)
        False
        >>> is_power_of(3, 10)
        False
        >>> is_power_of(1, 8)
        False
        >>> is_power_of(2, 0)    # 0 is not a power of any positive base.
        False
        >>> is_power_of(4, 16)
        True
        >>> is_power_of(4, 64)
        True
        >>> is_power_of(4, 63)
        False
        >>> is_power_of(4, 65)
        False
        >>> is_power_of(4, 32)
        False
    """
    ## YOUR CODE STARTS HERE
    # If num is 1, it's base^0 for any base
    if num == 1:
        return True
    # Return false if num is 0 or base is 1
    # 1 can only produce 1, so if num != 1, it's False
    if num == 0 or base == 1:
        return False
    # If num is less than base and not 1, it can't be a power
    if num < base:
        return False
    # If num is not divisible by base, it can't be a power of base
    if num % base != 0:
        return False
    # Check if num/base is a power of base
    return is_power_of(base, num // base)


def cut(a_list):
    """
        >>> cut([7, 4, 0])
        [7, 4, 0]
        >>> myList=[7, 4, -2, 1, 9]
        >>> cut(myList)   # Found(-2) Delete -2 and 1
        [7, 4, 9]
        >>> myList
        [7, 4, -2, 1, 9]
        >>> cut([-4, -7, -2, 1, 9]) # Found(-4) Delete -4, -7, -2 and 1
        [9]
        >>> cut([-3, -4, 5, -4, 1])  # Found(-3) Delete -2, -4 and 5. Found(-4) Delete -4 and 1
        []
        >>> cut([5, 7, -1, 6, -3, 1, 8, 785, 5, -2, 1, 0, 42]) # Found(-1) Delete -1. Found(-3) Delete -3, 1 and 8. Found(-2) Delete -2 and 0
        [5, 7, 6, 785, 5, 0, 42]
	"""
    ## YOUR CODE STARTS HERE
    # Empty list returns empty list
    if len(a_list) == 0:
        return []
    
    # Check if first element is negative
    if a_list[0] < 0:
        # Check how many elements to skip
        # where x is absolute value of negative number
        skip_count = abs(a_list[0])
        # Skip the negative number and the next (skip_count - 1) elements
        # Total elements to skip = skip_count
        return cut(a_list[skip_count:])
    
    else:
        return [a_list[0]] + cut(a_list[1:])


def right_max(num_list):
    """
        >>> right_max([3, 7, 2, 8, 6, 4, 5])
        [8, 8, 8, 8, 6, 5, 5]
        >>> right_max([1, 2, 3, 4, 5, 6])
        [6, 6, 6, 6, 6, 6]
        >>> right_max([1, 25, 3, 48, 5, 6, 12, 14, 89, 3, 2])
        [89, 89, 89, 89, 89, 89, 89, 89, 89, 3, 2]
    """
    ## YOUR CODE STARTS HERE
    # If list has only one element, return that element in a list
    if len(num_list) == 1:
        return [num_list[0]]
    
    # Process the rest of the list first
    rest_result = right_max(num_list[1:])
    
    # The maximum for current position is max of current element and first element of rest_result
    current_max = max(num_list[0], rest_result[0])
    
    # Return current_max and the result from the rest
    return [current_max] + rest_result


def consecutive_digits(num):
    """
        >>> consecutive_digits(2222466666678)
        True
        >>> consecutive_digits(12345684562)
        False
        >>> consecutive_digits(122)
        True
    """
    ## YOUR CODE STARTS HERE
    # Single digit number has no consecutive digits
    if num < 10:
        return False
    
    # Get last two digits
    last_digit = num % 10
    second_last_digit = (num // 10) % 10
    
    # Check if last two digits are the same
    if last_digit == second_last_digit:
        return True
    
    # Check the remaining digits and remove last digit
    return consecutive_digits(num // 10)


def only_evens(num):
    """
        >>> only_evens(4386112)
        4862
        >>> only_evens(0)
        0
        >>> only_evens(357997555531)
        0
        >>> only_evens(13847896213354889741236) 
        84862488426
    """
    ## YOUR CODE STARTS HERE
    # If num is 0, return 0
    if num == 0:
        return 0
    
    # Get the last digit
    last_digit = num % 10
    # Get the remaining number w/o last digit
    remaining = num // 10
    
    # Process the remaining digits
    result_from_rest = only_evens(remaining)
    
    # If last digit is even, append it to the result
    if last_digit % 2 == 0:
        # Count how many digits are in result_from_rest to determine multiplier
        # Shift result_from_rest left by one digit and add last_digit
        if result_from_rest == 0 and remaining != 0:
            # result_from_rest is 0 but there were odd digits
            return last_digit
        else:
            # Shift result left by multiplying by 10 and add last digit
            return result_from_rest * 10 + last_digit
    else:
        # Last digit is odd, just return result from rest
        return result_from_rest



def run_tests():
    import doctest

    #- Run tests in all docstrings
    doctest.testmod(verbose=True)
    
    #- Run tests per function - Uncomment the next line to run doctest by function. Replace is_power_of with the name of the function you want to test
    #doctest.run_docstring_examples(is_power_of, globals(), name='LAB3',verbose=True)

if __name__ == "__main__":
    run_tests()