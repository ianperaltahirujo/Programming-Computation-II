

def get_path(file_name):
    """
        Returns a string with the absolute path of a given file_name located in the same directory as this script

        # Do not modify this function in any way

        >>> get_path('words.txt')   # HW1.py and words.txt located in HW1 folder
        'G:\\My Drive\\CMPSC132\\HW1\\words.txt'
    """
    import os
    target_path = os.path.join(os.path.dirname(__file__), file_name)
    return target_path

def rectangle(perimeter, area):
    """
        Returns the longest side of the rectangle with given perimeter and area 
        if both sides are integer lengths, False otherwise.
        Uses the formulas: perimeter = 2w + 2h and area = w * h
        Solves the system of equations to find w and h, then checks if both are integers.
        
        >>> rectangle(14, 10)
        5
        >>> rectangle(12, 5)
        5
        >>> rectangle(25, 25)
        False
        >>> rectangle(50, 100)
        20
        >>> rectangle(11, 5)
        False
        >>> rectangle(11, 4)
        False
    """
    from math import sqrt
    
    # From perimeter = 2w + 2h and area = w * h
    # We get: h = perimeter/2 - w and area = w * (perimeter/2 - w)
    # This gives us: w^2 - (perimeter/2)*w + area = 0
    # Using quadratic formula: w = (perimeter/2 ± sqrt((perimeter/2)^2 - 4*area)) / 2
    
    half_perimeter = perimeter / 2
    discriminant = (half_perimeter * half_perimeter) - (4 * area)
    
    # Check if discriminant is negative (no real solutions)
    if discriminant < 0:
        return False
    
    sqrt_discriminant = sqrt(discriminant)
    
    # Calculate the two possible widths
    w1 = (half_perimeter + sqrt_discriminant) / 2
    w2 = (half_perimeter - sqrt_discriminant) / 2
    
    # Calculate corresponding heights
    h1 = half_perimeter - w1
    h2 = half_perimeter - w2
    
    # Check if both solutions give integer dimensions
    if w1.is_integer() and h1.is_integer():
        return int(max(w1, h1))
    elif w2.is_integer() and h2.is_integer():
        return int(max(w2, h2))
    else:
        return False


def to_decimal(oct_num):
    """
        Converts an octal number (base 8) to decimal (base 10).
        Processes digits from right to left, multiplying each digit by appropriate power of 8.
        
        >>> to_decimal(237) 
        159
        >>> to_decimal(35) 
        29
        >>> to_decimal(600) 
        384
        >>> to_decimal(420) 
        272
    """
    decimal_result = 0
    power = 0
    
    # Process digits from right to left using modulo and floor division
    while oct_num > 0:
        digit = oct_num % 10  # Get rightmost digit
        decimal_result = decimal_result + (digit * (8 ** power))  # Add digit * 8^power
        power = power + 1  # Increment power for next digit
        oct_num = oct_num // 10  # Remove rightmost digit
    
    return decimal_result


def has_hoagie(num):
    """
        Checks if a number has a "hoagie" - a digit surrounded by two identical digits.
        Handles negative numbers by processing them as positive.
        
        >>> has_hoagie(737) 
        True
        >>> has_hoagie(35) 
        False
        >>> has_hoagie(-6060) 
        True
        >>> has_hoagie(-111) 
        True
        >>> has_hoagie(6945) 
        False
    """
    # Handle negative numbers by making them positive
    if num < 0:
        num = -num
    
    # Numbers with less than 3 digits cannot have a hoagie
    if num < 100:
        return False
    
    # Extract first three digits to start checking
    prev_digit = num % 10
    num = num // 10
    curr_digit = num % 10
    num = num // 10
    
    # Check each group of three consecutive digits
    while num > 0:
        next_digit = num % 10
        
        # Check if current digit is surrounded by identical digits
        if prev_digit == next_digit:
            return True
        
        # Move to next position
        prev_digit = curr_digit
        curr_digit = next_digit
        num = num // 10
    
    return False


def is_identical(num_1, num_2):
    """
        Checks if two numbers are identical after removing sequences of repeated digits.
        For each number, replaces consecutive repeated digits with single instances.
        
        >>> is_identical(51111315, 51315)
        True
        >>> is_identical(7006600, 7706000)
        True
        >>> is_identical(135, 765) 
        False
        >>> is_identical(2023, 20) 
        False
    """
    def remove_consecutive_duplicates(num):
        """Helper function to remove consecutive duplicate digits from a number"""
        if num == 0:
            return 0
        
        result = 0
        multiplier = 1
        prev_digit = -1  # Initialize to impossible digit value
        
        # Process digits from right to left
        while num > 0:
            current_digit = num % 10
            
            # Only add digit if it's different from previous digit
            if current_digit != prev_digit:
                result = result + (current_digit * multiplier)
                multiplier = multiplier * 10
            
            prev_digit = current_digit
            num = num // 10
        
        return result
    
    # Remove consecutive duplicates from both numbers and compare
    cleaned_num1 = remove_consecutive_duplicates(num_1)
    cleaned_num2 = remove_consecutive_duplicates(num_2)
    
    return cleaned_num1 == cleaned_num2


def hailstone(num):
    """
        Generates the hailstone sequence starting from num until reaching 1.
        If num is even: next = num/2, if num is odd: next = 3*num + 1
        
        >>> hailstone(10)
        [10, 5, 16, 8, 4, 2, 1]
        >>> hailstone(1)
        [1]
        >>> hailstone(27)
        [27, 82, 41, 124, 62, 31, 94, 47, 142, 71, 214, 107, 322, 161, 484, 242, 121, 364, 182, 91, 274, 137, 412, 206, 103, 310, 155, 466, 233, 700, 350, 175, 526, 263, 790, 395, 1186, 593, 1780, 890, 445, 1336, 668, 334, 167, 502, 251, 754, 377, 1132, 566, 283, 850, 425, 1276, 638, 319, 958, 479, 1438, 719, 2158, 1079, 3238, 1619, 4858, 2429, 7288, 3644, 1822, 911, 2734, 1367, 4102, 2051, 6154, 3077, 9232, 4616, 2308, 1154, 577, 1732, 866, 433, 1300, 650, 325, 976, 488, 244, 122, 61, 184, 92, 46, 23, 70, 35, 106, 53, 160, 80, 40, 20, 10, 5, 16, 8, 4, 2, 1]
        >>> hailstone(7)
        [7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
        >>> hailstone(19)
        [19, 58, 29, 88, 44, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
    """
    sequence = [num]
    
    # Continue until we reach 1
    while num != 1:
        if num % 2 == 0:  # Even number
            num = num // 2
        else:  # Odd number
            num = 3 * num + 1
        sequence.append(num)
    
    return sequence


def overloaded_add(d, key, value):
    """
        Adds key-value pair to dictionary. If key exists, converts value to list
        and appends new value. If key already has a list, appends to existing list.
        
        >>> d = {"Alice": "Engineer"}
        >>> overloaded_add(d, "Bob", "Manager")
        >>> overloaded_add(d, "Alice", "Sales")
        >>> d == {"Alice": ["Engineer", "Sales"], "Bob": "Manager"}
        True
    """
    if key in d:
        # Key already exists
        if type(d[key]) == list:
            # Value is already a list, append to it
            d[key].append(value)
        else:
            # Value is not a list, convert to list and add new value
            d[key] = [d[key], value]
    else:
        # Key doesn't exist, add it normally
        d[key] = value


def by_department(d):
    """
        Reorganizes employee dictionary by department.
        Input: {emp_id: {'name': name, 'position': pos, 'department': dept}}
        Output: {dept: [{'emp_id': id, 'name': name, 'position': pos}]}
        
        >>> employees = {
        ...    1: {'name': 'John Doe', 'position': 'Manager', 'department': 'Sales'},
        ...    2: {'position': 'Budget Advisor', 'name': 'Sara Miller', 'department': 'Finance'},
        ...    3: {'name': 'Jane Smith', 'position': 'Engineer', 'department': 'Engineering'},
        ...    4: {'name': 'Bob Johnson', 'department': 'Finance', 'position': 'Analyst'},
        ...    5: {'position': 'Senior Developer', 'department': 'Engineering', 'name': 'Clark Wayne'}
        ...    }

        >>> by_department(employees)
        {'Sales': [{'emp_id': 1, 'name': 'John Doe', 'position': 'Manager'}], 'Finance': [{'emp_id': 2, 'name': 'Sara Miller', 'position': 'Budget Advisor'}, {'emp_id': 4, 'name': 'Bob Johnson', 'position': 'Analyst'}], 'Engineering': [{'emp_id': 3, 'name': 'Jane Smith', 'position': 'Engineer'}, {'emp_id': 5, 'name': 'Clark Wayne', 'position': 'Senior Developer'}]}
    """
    result = {}
    
    # Process each employee
    for emp_id, emp_info in d.items():
        department = emp_info['department']
        
        # Create new employee record without department
        new_emp = {
            'emp_id': emp_id,
            'name': emp_info['name'],
            'position': emp_info['position']
        }
        
        # Add employee to appropriate department list
        if department in result:
            result[department].append(new_emp)
        else:
            result[department] = [new_emp]
    
    return result


def successors(file_name):
    """
        Reads a text file and creates a dictionary mapping each word/punctuation
        to a list of its successors (words that follow it).
        
        >>> expected = {'.': ['We', 'Maybe'], 'We': ['came'], 'came': ['to'], 'to': ['learn', 'have', 'make'], 'learn': [',', 'how'], ',': ['eat'], 'eat': ['some'], 'some': ['pizza'], 'pizza': ['and', 'too'], 'and': ['to'], 'have': ['fun'], 'fun': ['.'], 'Maybe': ['to'], 'how': ['to'], 'make': ['pizza'], 'too': ['!']}
        >>> returnedDict = successors('items.txt')
        >>> expected == returnedDict
        True
        >>> returnedDict['.']
        ['We', 'Maybe']
        >>> returnedDict['to']
        ['learn', 'have', 'make']
        >>> returnedDict['fun']
        ['.']
        >>> returnedDict[',']
        ['eat']
    """
    file_path = get_path(file_name)
    with open(file_path, 'r') as file:   
        contents = file.read()
    
    # Parse text into tokens (words and punctuation)
    tokens = []
    current_word = ""
    
    for char in contents:
        if char.isalnum():
            current_word = current_word + char
        else:
            if current_word:
                tokens.append(current_word)
                current_word = ""
            if char != ' ' and char != '\n' and char != '\t':
                tokens.append(char)
    
    # Add final word if exists
    if current_word:
        tokens.append(current_word)
    
    # Build successors dictionary
    successors_dict = {}
    
    # Start with "." pointing to first word of each sentence
    successors_dict['.'] = []
    
    # Add first word as successor to "."
    if tokens:
        successors_dict['.'].append(tokens[0])
    
    # Process all consecutive token pairs
    for i in range(len(tokens) - 1):
        current_token = tokens[i]
        next_token = tokens[i + 1]
        
        # Add successor relationship
        if current_token in successors_dict:
            if next_token not in successors_dict[current_token]:
                successors_dict[current_token].append(next_token)
        else:
            successors_dict[current_token] = [next_token]
    
    # Handle sentence boundaries - find sentence-ending punctuation
    for i in range(len(tokens)):
        if tokens[i] in ['.', '!', '?']:
            # Check if there's a next sentence starting after this punctuation
            if i + 1 < len(tokens):
                if tokens[i + 1] not in successors_dict['.']:
                    successors_dict['.'].append(tokens[i + 1])
    
    return successors_dict


def addToTrie(trie, word):
    """
        Adds a word to the trie data structure. Modifies the trie in place.
        Each level represents a letter, with 'word': True marking complete words.
       
        >>> trie_dict = {'a' : {'word' : True, 'p' : {'p' : {'l' : {'e' : {'word' : True}}}}, 'i' : {'word' : True}}} 
        >>> addToTrie(trie_dict, 'art')
        >>> trie_dict
        {'a': {'word': True, 'p': {'p': {'l': {'e': {'word': True}}}}, 'i': {'word': True}, 'r': {'t': {'word': True}}}}
        >>> addToTrie(trie_dict, 'moon') 
        >>> trie_dict
        {'a': {'word': True, 'p': {'p': {'l': {'e': {'word': True}}}}, 'i': {'word': True}, 'r': {'t': {'word': True}}}, 'm': {'o': {'o': {'n': {'word': True}}}}}
    """
    current = trie
    
    # Traverse/create path for each letter in the word
    for letter in word:
        if letter not in current:
            current[letter] = {}
        current = current[letter]
    
    # Mark the end of the word
    current['word'] = True


def createDictionaryTrie(file_name):
    """
        Creates a trie from words in a text file. Each word is on a separate line.
        Converts all words to lowercase and uses addToTrie function.
        
        >>> trie = createDictionaryTrie("words.txt")
        >>> trie == {'b': {'a': {'l': {'l': {'word': True}}, 't': {'s': {'word': True}}}, 'i': {'r': {'d': {'word': True}},\
                     'n': {'word': True}}, 'o': {'y': {'word': True}}}, 't': {'o': {'y': {'s': {'word': True}}},\
                     'r': {'e': {'a': {'t': {'word': True}}, 'e': {'word': True}}}}}
        True
    """
    file_path = get_path(file_name)
    with open(file_path, 'r') as file:   
        contents = file.read()
    
    # Initialize empty trie
    trie = {}
    
    # Split contents into individual words and process each
    words = contents.split('\n')
    for word in words:
        word = word.strip().lower()  # Remove whitespace and convert to lowercase
        if word:  # Only process non-empty words
            addToTrie(trie, word)
    
    return trie


def wordExists(trie, word):
    """
        Checks if a word exists in the trie data structure.
        Returns True if the word exists and is marked as complete, False otherwise.
        
        >>> trie_dict = {'a' : {'word' : True, 'p' : {'p' : {'l' : {'e' : {'word' : True}}}}, 'i' : {'word' : True}}} 
        >>> wordExists(trie_dict, 'armor')
        False
        >>> wordExists(trie_dict, 'apple')
        True
        >>> wordExists(trie_dict, 'apples')
        False
        >>> wordExists(trie_dict, 'a')
        True
        >>> wordExists(trie_dict, 'as')
        False
        >>> wordExists(trie_dict, 'tt')
        False
    """
    current = trie
    
    # Traverse the trie following the letters of the word
    for letter in word:
        if letter not in current:
            return False  # Letter not found, word doesn't exist
        current = current[letter]
    
    # Check if this path represents a complete word
    return 'word' in current and current['word'] == True


def run_tests():
    import doctest
    # Run start tests in all docstrings
    doctest.testmod(verbose=True)
    
    # Run start tests per function - Uncomment the next line to run doctest by function. Replace rectangle with the name of the function you want to test
    doctest.run_docstring_examples(rectangle, globals(), name='HW1',verbose=True)   

if __name__ == "__main__":
    run_tests()