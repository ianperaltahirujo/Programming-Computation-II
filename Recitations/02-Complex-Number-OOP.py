class Complex:
    def __init__(self, r, i):
        self._real = r
        self._imag = i
 
    def __str__(self):
        """Display complex number"""
        if self._imag >= 0:
            return f"{self._real} + {self._imag}i"
        else:
            return f"{self._real} - {abs(self._imag)}i"
 
    __repr__ = __str__
 
    def conjugate(self):
        return Complex(self._real, -1 * self._imag)
 
    def __mul__(self, other):
        if isinstance(other, Complex):
            real_part = self._real * other._real - self._imag * other._imag
            imag_part = self._imag * other._real + self._real * other._imag
            ans = Complex(real_part, imag_part)
        else:
            real_part = self._real * other
            imag_part = self._imag * other
            ans = Complex(real_part, imag_part)
        return ans
 
    def __rmul__(self, other):
        return self * other


class Real(Complex):
    def __init__(self, value):
        super().__init__(value, 0)
    
    def __mul__(self, other):
        result = super().__mul__(other)
        
        if isinstance(other, Complex) and not isinstance(other, Real):
            return result
        if result._imag == 0:
            return Real(result._real)
        
        return result
    
    def __eq__(self, other):
        ''' Returns True if other is a Real object that has the same value or if other is
            a Complex object with _imag=0 and same value for _real, False otherwise

            >>> Real(4) == Real(4)
            True
            >>> Real(4) == Real(4.0)
            True
            >>> Real(5) == Complex(5, 0)
            True
            >>> Real(5) == Complex(5, 12)
            False
            >>> Real(5) == 5.5
            False
        '''
        if isinstance(other, Real):
            return self._real == other._real
        elif isinstance(other, Complex):
            return self._real == other._real and other._imag == 0
        else:
            return False
    
    def __int__(self):
        return int(self._real)
    
    def __float__(self):
        return float(self._real)
        

if __name__ == "__main__":
    print(f"Real(4) == Real(4): {Real(4) == Real(4)}")
    print(f"Real(4) == Real(4.0): {Real(4) == Real(4.0)}")
    print(f"Real(5) == Complex(5, 0): {Real(5) == Complex(5, 0)}")
    print(f"Real(5) == Complex(5, 12): {Real(5) == Complex(5, 12)}")
    print(f"Real(5) == 5.5: {Real(5) == 5.5}")