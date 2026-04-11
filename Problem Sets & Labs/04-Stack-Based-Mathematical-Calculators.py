
class Node:
    def __init__(self, value):
        self.value = value  
        self.next = None 
    
    def __str__(self):
        return "Node({})".format(self.value) 

    __repr__ = __str__
                          

#=============================================== Part I ==============================================

class Stack:
    '''
        >>> x=Stack()
        >>> x.pop()
        >>> x.push(2)
        >>> x.push(4)
        >>> x.push(6)
        >>> x
        Top:Node(6)
        Stack:
        6
        4
        2
        >>> x.pop()
        6
        >>> x
        Top:Node(4)
        Stack:
        4
        2
        >>> len(x)
        2
        >>> x.peek()
        4
    '''
    def __init__(self):
        self.top = None
    
    def __str__(self):
        temp=self.top
        out=[]
        while temp:
            out.append(str(temp.value))
            temp=temp.next
        out='\n'.join(out)
        return ('Top:{}\nStack:\n{}'.format(self.top,out))

    __repr__=__str__


    def isEmpty(self):
        """Check if the stack is empty"""
        return self.top is None

    def __len__(self):
        """Return the number of elements in the stack"""
        count = 0
        current = self.top
        while current:
            count += 1
            current = current.next
        return count

    def push(self, value):
        """Add a new node with the given value to the top of the stack"""
        new_node = Node(value)
        new_node.next = self.top
        self.top = new_node

    def pop(self):
        """Remove and return the value of the top node"""
        if self.isEmpty():
            return None
        value = self.top.value
        self.top = self.top.next
        return value

    def peek(self):
        """Return the value of the top node without removing it"""
        if self.isEmpty():
            return None
        return self.top.value


#=============================================== Part II ==============================================

class Calculator:
    def __init__(self):
        self.__expr = None


    @property
    def getExpr(self):
        return self.__expr

    def setExpr(self, new_expr):
        if isinstance(new_expr, str):
            self.__expr=new_expr
        else:
            print('setExpr error: Invalid expression')
            return None

    def _isNumber(self, txt):
        '''
            >>> x=Calculator()
            >>> x._isNumber(' 2.560 ')
            True
            >>> x._isNumber('7 56')
            False
            >>> x._isNumber('2.56p')
            False
        '''
        try:
            float(txt)
            return True
        except ValueError:
            return False

    def _getPostfix(self, txt):
        '''
            Required: _getPostfix must create and use a Stack for expression processing
            >>> x=Calculator()
            >>> x._getPostfix('     2 ^       4')
            '2.0 4.0 ^'
            >>> x._getPostfix('          2 ')
            '2.0'
            >>> x._getPostfix('2.1        * 5        + 3       ^ 2 +         1 +             4.45')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.45 +'
            >>> x._getPostfix('2*5.34+3^2+1+4')
            '2.0 5.34 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('2.1 * 5 + 3 ^ 2 + 1 + 4')
            '2.1 5.0 * 3.0 2.0 ^ + 1.0 + 4.0 +'
            >>> x._getPostfix('( .5 )')
            '0.5'
            >>> x._getPostfix ('( ( 2 ) )')
            '2.0'
            >>> x._getPostfix ('2 * (           ( 5 +-3 ) ^ 2 + (1 + 4 ))')
            '2.0 5.0 -3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('(2 * ( ( 5 + 3) ^ 2 + (1 + 4 )))')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix ('((2 *((5 + 3) ^ 2 + (1 +4 ))))')
            '2.0 5.0 3.0 + 2.0 ^ 1.0 4.0 + + *'
            >>> x._getPostfix('2* (       -5 + 3 ) ^2+ ( 1 +4 )')
            '2.0 -5.0 3.0 + 2.0 ^ * 1.0 4.0 + +'

            # In invalid expressions, you might print an error message, adjust doctest accordingly
            # If you are veryfing the expression in calculate before passing to postfix, this cases are not necessary

            >>> x._getPostfix('2 * 5 + 3 ^ + -2 + 1 + 4')
            >>> x._getPostfix('     2 * 5 + 3  ^ * 2 + 1 + 4')
            >>> x._getPostfix('2    5')
            >>> x._getPostfix('25 +')
            >>> x._getPostfix(' 2 * ( 5      + 3 ) ^ 2 + ( 1 +4 ')
            >>> x._getPostfix(' 2 * ( 5 + 3 ) ^  2 + ) 1 + 4 (')
            >>> x._getPostfix('2 *      5% + 3       ^ + -2 +1 +4')
        '''
        postfixStack = Stack()
        
        # Define operator precedence
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
        
        # Tokenize the expression
        tokens = []
        i = 0
        while i < len(txt):
            if txt[i].isspace():
                i += 1
            elif txt[i] in '()*/^':
                tokens.append(txt[i])
                i += 1
            elif txt[i] in '+-':
                
                # Looking ahead to see what follows
                j = i + 1
                while j < len(txt) and txt[j].isspace():
                    j += 1
                
                # Check if what follows is a digit (potential number)
                next_is_digit = j < len(txt) and (txt[j].isdigit() or txt[j] == '.')
                
                # Check if what follows is an operator (including +/- which are ambiguous)
                next_is_operator = j < len(txt) and txt[j] in '*/^'
                next_is_plus_minus = j < len(txt) and txt[j] in '+-'
                
                if not tokens or tokens[-1] == '(':
                    # After ( or at start, this can be a unary sign for a number
                    if next_is_digit:
                        # Extract the signed number
                        start_digit = j
                        while j < len(txt) and (txt[j].isdigit() or txt[j] == '.'):
                            j += 1
                        num_str = txt[i] + txt[start_digit:j]
                        tokens.append(num_str)
                        i = j
                    else:
                        # Just a standalone operator
                        tokens.append(txt[i])
                        i += 1
                elif tokens[-1] in '+-*/^':
                    if txt[i] == '-' and next_is_digit:
                        # Extract the negative number
                        start_digit = j
                        while j < len(txt) and (txt[j].isdigit() or txt[j] == '.'):
                            j += 1
                        num_str = txt[i] + txt[start_digit:j]
                        tokens.append(num_str)
                        i = j
                    else:
                        # Treat as standalone operator (will be caught as invalid)
                        tokens.append(txt[i])
                        i += 1
                else:
                    # It's a binary operator
                    tokens.append(txt[i])
                    i += 1
            elif txt[i].isdigit() or txt[i] == '.':
                # Extract number
                j = i
                while j < len(txt) and (txt[j].isdigit() or txt[j] == '.'):
                    j += 1
                tokens.append(txt[i:j])
                i = j
            else:
                # Unknown character, skip it or handle as error
                i += 1
        
        # Validate and convert to postfix
        output = []
        paren_count = 0
        prev_token = None
        
        for i, token in enumerate(tokens):
            # Check for invalid operator
            if token not in precedence and token not in '()' and not self._isNumber(token):
                return None
            
            # Check for consecutive operators 
            # Two operators in a row is invalid unless the second token is a number 
            if prev_token in precedence and token in precedence:
                return None
            
            # Check for missing operators (two consecutive numbers)
            if prev_token and self._isNumber(prev_token) and self._isNumber(token):
                return None
            
            # Check for implied multiplication like 3(5)
            if prev_token and self._isNumber(prev_token) and token == '(':
                return None
            if prev_token == ')' and (self._isNumber(token) or token == '('):
                return None
            
            if self._isNumber(token):
                output.append(str(float(token)))
            elif token == '(':
                postfixStack.push(token)
                paren_count += 1
            elif token == ')':
                paren_count -= 1
                if paren_count < 0:
                    return None
                while not postfixStack.isEmpty() and postfixStack.peek() != '(':
                    output.append(postfixStack.pop())
                if postfixStack.isEmpty():
                    return None
                postfixStack.pop()
            elif token in precedence:
                # Check for missing operands at the end
                if i == len(tokens) - 1:
                    return None
                
                # Check if next token exists and is valid
                # If current is an operator and next is also an operator, that's invalid
                if i + 1 < len(tokens):
                    next_token = tokens[i + 1]
                    # If next token is an operator, check if it's valid
                    if next_token in precedence and not self._isNumber(next_token):
                        return None
                
                # Handle exponentiation
                if token == '^':
                    while not postfixStack.isEmpty() and postfixStack.peek() in precedence and precedence[postfixStack.peek()] > precedence[token]:
                        output.append(postfixStack.pop())
                else:
                    while not postfixStack.isEmpty() and postfixStack.peek() in precedence and precedence[postfixStack.peek()] >= precedence[token]:
                        output.append(postfixStack.pop())
                postfixStack.push(token)
            
            prev_token = token
        
        # Check for unbalanced parentheses
        if paren_count != 0:
            return None
        
        # Pop remaining operators
        while not postfixStack.isEmpty():
            op = postfixStack.pop()
            if op == '(' or op == ')':
                return None
            output.append(op)
        
        # Check if output is empty
        if not output:
            return None
        
        return ' '.join(output)


    @property
    def calculate(self):
        '''
            calculate must call _getPostfix
            calculate must create and use a Stack to compute the final result as shown in the video lecture
            
            >>> x=Calculator()
            >>> x.setExpr('4        + 3 -       2')
            >>> x.calculate
            5.0
            >>> x.setExpr('-2 +          3.5')
            >>> x.calculate
            1.5
            >>> x.setExpr('      4 +           3.65  - 2        / 2')
            >>> x.calculate
            6.65
            >>> x.setExpr('23 / 12 - 223 + 5.25      * 4 * 3423')
            >>> x.calculate
            71661.91666666667
            >>> x.setExpr('2-3*4')
            >>> x.calculate
            -10.0
            >>> x.setExpr('7^2^3')
            >>> x.calculate
            5764801.0
            >>> x.setExpr(' 3 * ((( 10 - 2*3 )) )')
            >>> x.calculate
            12.0
            >>> x.setExpr('      8 / 4 * (3 - 2.45 * ( 4   - 2 ^ 3 )       ) + 3')
            >>> x.calculate
            28.6
            >>> x.setExpr('2 * ( 4 +        2 * (         5 - 3 ^ 2 ) + 1 ) + 4')
            >>> x.calculate
            -2.0
            >>> x.setExpr(' 2.5 +         3 * (2 + ( 3.0) * ( 5^2-2 * 3 ^ ( 2 )         ) * ( 4 ) ) * ( 2 / 8 + 2 * ( 3 - 1 /3 ) ) - 2 / 3^ 2')
            >>> x.calculate
            1442.7777777777778
            

            # In invalid expressions, you might print an error message, but code must return None, adjust doctest accordingly
            >>> x.setExpr(" 4 ++ 3+ 2") 
            >>> x.calculate
            >>> x.setExpr("4  3 +2")
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 *( 2 - 3 * 2 ) )')
            >>> x.calculate
            >>> x.setExpr('( 2 ) * 10 - 3 * / ( 2 - 3 * 2 )')
            >>> x.calculate
            >>> x.setExpr(' ) 2 ( *10 - 3 * ( 2 - 3 * 2 ) ')
            >>> x.calculate
            >>> x.setExpr('(    3.5 ) ( 15 )') 
            >>> x.calculate
            >>> x.setExpr('3 ( 5) - 15 + 85 ( 12)') 
            >>> x.calculate
            >>> x.setExpr("( -2/6) + ( 5 ( ( 9.4 )))") 
            >>> x.calculate
        '''

        if not isinstance(self.__expr,str) or len(self.__expr)<=0:
            print("Argument error in calculate")
            return None

        calcStack = Stack()
        
        # Get postfix expression
        postfix = self._getPostfix(self.__expr)
        
        if postfix is None:
            return None
        
        # Evaluate postfix expression
        tokens = postfix.split()
        
        for token in tokens:
            if self._isNumber(token):
                calcStack.push(float(token))
            else:
                # It's an operator
                if len(calcStack) < 2:
                    return None
                
                operand2 = calcStack.pop()
                operand1 = calcStack.pop()
                
                if token == '+':
                    result = operand1 + operand2
                elif token == '-':
                    result = operand1 - operand2
                elif token == '*':
                    result = operand1 * operand2
                elif token == '/':
                    if operand2 == 0:
                        return None
                    result = operand1 / operand2
                elif token == '^':
                    result = operand1 ** operand2
                
                calcStack.push(result)
        
        if len(calcStack) != 1:
            return None
        
        return calcStack.pop()

#=============================================== Part III ==============================================

class AdvancedCalculator:
    '''
        >>> C = AdvancedCalculator()
        >>> C.states == {}
        True
        >>> C.setExpression('a = 5;b = 7 + a;a = 7;c = a + b;c = a * 0;return c')
        >>> C.calculateExpressions() == {'a = 5': {'a': 5.0}, 'b = 7 + a': {'a': 5.0, 'b': 12.0}, 'a = 7': {'a': 7.0, 'b': 12.0}, 'c = a + b': {'a': 7.0, 'b': 12.0, 'c': 19.0}, 'c = a * 0': {'a': 7.0, 'b': 12.0, 'c': 0.0}, '_return_': 0.0}
        True
        >>> C.states == {'a': 7.0, 'b': 12.0, 'c': 0.0}
        True
        >>> C.setExpression('x1 = 5;x2 = 7 * ( x1 - 1 );x1 = x2 - x1;return x2 + x1 ^ 3')
        >>> C.states == {}
        True
        >>> C.calculateExpressions() == {'x1 = 5': {'x1': 5.0}, 'x2 = 7 * ( x1 - 1 )': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        True
        >>> print(C.calculateExpressions())
        {'x1 = 5': {'x1': 5.0}, 'x2 = 7 * ( x1 - 1 )': {'x1': 5.0, 'x2': 28.0}, 'x1 = x2 - x1': {'x1': 23.0, 'x2': 28.0}, '_return_': 12195.0}
        >>> C.states == {'x1': 23.0, 'x2': 28.0}
        True
        >>> C.setExpression('x1 = 5 * 5 + 97;x2 = 7 * ( x1 / 2 );x1 = x2 * 7 / x1;return x1 * ( x2 - 5 )')
        >>> C.calculateExpressions() == {'x1 = 5 * 5 + 97': {'x1': 122.0}, 'x2 = 7 * ( x1 / 2 )': {'x1': 122.0, 'x2': 427.0}, 'x1 = x2 * 7 / x1': {'x1': 24.5, 'x2': 427.0}, '_return_': 10339.0}
        True
        >>> C.states == {'x1': 24.5, 'x2': 427.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;C = A + B;A = 20;D = A + B + C;return D - A')
        >>> C.calculateExpressions() == {'A = 1': {'A': 1.0}, 'B = A + 9': {'A': 1.0, 'B': 10.0}, 'C = A + B': {'A': 1.0, 'B': 10.0, 'C': 11.0}, 'A = 20': {'A': 20.0, 'B': 10.0, 'C': 11.0}, 'D = A + B + C': {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}, '_return_': 21.0}
        True
        >>> C.states == {'A': 20.0, 'B': 10.0, 'C': 11.0, 'D': 41.0}
        True
        >>> C.setExpression('A = 1;B = A + 9;2C = A + B;A = 20;D = A + B + C;return D + A')
        >>> C.calculateExpressions() is None
        True
        >>> C.states == {}
        True
    '''
    def __init__(self):
        self.expressions = ''
        self.states = {}

    def setExpression(self, expression):
        self.expressions = expression
        self.states = {}

    def _isVariable(self, word):
        '''
            >>> C = AdvancedCalculator()
            >>> C._isVariable('volume')
            True
            >>> C._isVariable('4volume')
            False
            >>> C._isVariable('volume2')
            True
            >>> C._isVariable('vol%2')
            False
        '''
        if not word or len(word) == 0:
            return False
        if not word[0].isalpha():
            return False
        return word.isalnum()
       

    def _replaceVariables(self, expr):
        '''
            >>> C = AdvancedCalculator()
            >>> C.states = {'x1': 23.0, 'x2': 28.0}
            >>> C._replaceVariables('1')
            '1'
            >>> C._replaceVariables('105 + x')
            >>> C._replaceVariables('7 * ( x1 - 1 )')
            '7 * ( 23.0 - 1 )'
            >>> C._replaceVariables('x2 - x1')
            '28.0 - 23.0'
        '''
        tokens = expr.split()
        result = []
        
        for token in tokens:
            if self._isVariable(token):
                if token in self.states:
                    result.append(str(self.states[token]))
                else:
                    return None
            else:
                result.append(token)
        
        return ' '.join(result)

    
    def calculateExpressions(self):
        # Start fresh - clear states at the beginning
        self.states = {} 
        calcObj = Calculator()
        
        # Split by semicolons to get individual lines
        lines = self.expressions.split(';')
        result_dict = {}
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('return'):
                # Handle return statement
                expr_part = line.split('return', 1)[1].strip()
                replaced_expr = self._replaceVariables(expr_part)
                
                if replaced_expr is None:
                    self.states = {}
                    return None
                
                calcObj.setExpr(replaced_expr)
                return_value = calcObj.calculate
                
                if return_value is None:
                    self.states = {}
                    return None
                
                result_dict['_return_'] = return_value
            else:
                # Handle variable assignment
                parts = line.split('=', 1)
                
                if len(parts) != 2:
                    self.states = {}
                    return None
                
                var_name = parts[0].strip()
                expr_part = parts[1].strip()
                
                # Check if variable name is valid before doing anything else
                if not self._isVariable(var_name):
                    self.states = {}
                    return None
                
                # Replace variables in the expression
                replaced_expr = self._replaceVariables(expr_part)
                
                if replaced_expr is None:
                    self.states = {}
                    return None
                
                # Calculate the expression
                calcObj.setExpr(replaced_expr)
                value = calcObj.calculate
                
                if value is None:
                    self.states = {}
                    return None
                
                # Only update states after all validation passes
                self.states[var_name] = value
                result_dict[line] = dict(self.states)
        
        return result_dict


def run_tests():
    import doctest

    # Run tests in all docstrings
    doctest.testmod(verbose=True)
    
    # Run tests per function - Uncomment the next line to run doctest by function. Replace Stack with the name of the function you want to test
    doctest.run_docstring_examples(Stack, globals(), name='HW3',verbose=True)   

if __name__ == "__main__":
    run_tests()