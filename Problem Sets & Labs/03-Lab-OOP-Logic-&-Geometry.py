
import math

# -------- SECTION 1
class Instructor:
    '''
        >>> t1= Instructor('John Doe')
        >>> t1.get_name()
        'John Doe'
        >>> t1.get_courses()
        []
        >>> t1.add_course('MATH140')
        >>> t1.get_courses()
        ['MATH140']
        >>> t1.add_course('STAT100')
        >>> t1.get_courses()
        ['MATH140', 'STAT100']
        >>> t1.add_course('STAT100')
        >>> t1.get_courses()
        ['MATH140', 'STAT100']
        >>> t1.remove_course('MATH141')
        >>> t1.get_courses()
        ['MATH140', 'STAT100']
        >>> t1.remove_course('MATH140')
        >>> t1.get_courses()
        ['STAT100']
    '''

    def __init__(self, name):
        """Initialize instructor with name and empty courses list."""
        self.name = name
        self.courses = []

    def get_name(self):
        """Return the instructor's name."""
        return self.name

    def set_name(self, new_name):
        """Set instructor's name if new_name is non-empty string."""
        if isinstance(new_name, str) and len(new_name) > 0:
            self.name = new_name

    def get_courses(self):
        """Return list of courses taught by instructor."""
        return self.courses

    def remove_course(self, course):
        """Remove course from list if it exists."""
        if course in self.courses:
            self.courses.remove(course)
        
    def add_course(self, course):
        """Add course to list if not already present."""
        if course not in self.courses:
            self.courses.append(course)


# -------- SECTION 2      
class Pantry:
    """"
        >>> sara_pantry = Pantry()                
        >>> sara_pantry.stock_pantry('Bread', 2)
        'Pantry Stock for Bread: 2.0'
        >>> sara_pantry.stock_pantry('Cookies', 6) 
        'Pantry Stock for Cookies: 6.0'
        >>> sara_pantry.stock_pantry('Chocolate', 4) 
        'Pantry Stock for Chocolate: 4.0'
        >>> sara_pantry.stock_pantry('Pasta', 3)     
        'Pantry Stock for Pasta: 3.0'
        >>> sara_pantry
        I am a Pantry object, my current stock is {'Bread': 2.0, 'Cookies': 6.0, 'Chocolate': 4.0, 'Pasta': 3.0}
        >>> sara_pantry.get_item('Pasta', 2)     
        'You have 1.0 of Pasta left'
        >>> sara_pantry.get_item('Pasta', 6) 
        'Add Pasta to your shopping list!'
        >>> sara_pantry
        I am a Pantry object, my current stock is {'Bread': 2.0, 'Cookies': 6.0, 'Chocolate': 4.0, 'Pasta': 0.0}
        >>> ben_pantry = Pantry()                    
        >>> ben_pantry.stock_pantry('Cereal', 2)
        'Pantry Stock for Cereal: 2.0'
        >>> ben_pantry.stock_pantry('Noodles', 5) 
        'Pantry Stock for Noodles: 5.0'
        >>> ben_pantry.stock_pantry('Cookies', 9) 
        'Pantry Stock for Cookies: 9.0'
        >>> ben_pantry.stock_pantry('Cookies', 8) 
        'Pantry Stock for Cookies: 17.0'
        >>> ben_pantry.get_item('Pasta', 2)       
        "You don't have Pasta"
        >>> ben_pantry.get_item('Cookies', 2.5) 
        'You have 14.5 of Cookies left'
        >>> sara_pantry.transfer(ben_pantry, 'Cookies')
        >>> sara_pantry
        I am a Pantry object, my current stock is {'Bread': 2.0, 'Cookies': 20.5, 'Chocolate': 4.0, 'Pasta': 0.0}
        >>> ben_pantry.transfer(sara_pantry, 'Rice')
        >>> ben_pantry.transfer(sara_pantry, 'Pasta')
        >>> ben_pantry
        I am a Pantry object, my current stock is {'Cereal': 2.0, 'Noodles': 5.0, 'Cookies': 0.0}
        >>> ben_pantry.transfer(sara_pantry, 'Pasta')
        >>> ben_pantry
        I am a Pantry object, my current stock is {'Cereal': 2.0, 'Noodles': 5.0, 'Cookies': 0.0}
        >>> sara_pantry
        I am a Pantry object, my current stock is {'Bread': 2.0, 'Cookies': 20.5, 'Chocolate': 4.0, 'Pasta': 0.0}
    """

    def __init__(self):
        self.items = {}
    
    def __repr__(self):
        """Return string representation of pantry contents."""
        return f"I am a Pantry object, my current stock is {self.items}"

    def stock_pantry(self, item, qty):
        """Add qty amount of item to pantry stock."""
        qty = float(qty)
        if item in self.items:
            self.items[item] += qty
        else:
            self.items[item] = qty
        return f"Pantry Stock for {item}: {self.items[item]}"

    def get_item(self, item, qty):
        """Remove up to qty amount of item from pantry."""
        qty = float(qty)
        
        # Check if item exists in pantry
        if item not in self.items:
            return f"You don't have {item}"
        
        current_stock = self.items[item]
        
        # Check if we have enough stock
        if qty <= current_stock:
            self.items[item] -= qty
            remaining = self.items[item]
            return f"You have {remaining} of {item} left"
        else:
            # Use all remaining stock and alert to buy more
            self.items[item] = 0.0
            return f"Add {item} to your shopping list!"
    
    def transfer(self, other_pantry, item):
        """Transfer entire stock of item from other_pantry to this pantry."""
        if item in other_pantry.items and other_pantry.items[item] > 0:
            transfer_amount = other_pantry.items[item]
            
            # Add to current pantry
            if item in self.items:
                self.items[item] += transfer_amount
            else:
                self.items[item] = transfer_amount
            
            # Set other pantry's stock to 0
            other_pantry.items[item] = 0.0


# -------- SECTION 3
class Player:
    """
        >>> p1 = Player('Susy')
        >>> print(p1)
        No game records for Susy
        >>> p1.update_loss()
        >>> p1
        *Game records for Susy*
        Total games: 1
        Games won: 0
        Games lost: 1
        Best game: None
        >>> p1.update_win(5)
        >>> p1.update_win(2)
        >>> p1
        *Game records for Susy*
        Total games: 3
        Games won: 2
        Games lost: 1
        Best game: 2 attempts
    """
    def __init__(self, name):
        """Initialize player with name and zero game stats."""
        self.player_name = name
        self.games_won = 0
        self.games_lost = 0
        self.best_game = None

    def update_win(self, att):
        """Update player stats for a win with given attempts."""
        self.games_won += 1
        
        # Update best game if this is first win or fewer attempts
        if self.best_game is None or att < self.best_game:
            self.best_game = att
    
    def update_loss(self):
        """Update player stats for a loss."""
        self.games_lost += 1

    def __str__(self):
        """Return formatted string of player statistics."""
        total_games = self.games_won + self.games_lost
        
        # Return no records message if no games played
        if total_games == 0:
            return f"No game records for {self.player_name}"
        
        # Format best game display
        best_display = f"{self.best_game} attempts" if self.best_game is not None else "None"
        
        # Return formatted statistics
        return (f"*Game records for {self.player_name}*\n"
                f"Total games: {total_games}\n"
                f"Games won: {self.games_won}\n"
                f"Games lost: {self.games_lost}\n"
                f"Best game: {best_display}")

    __repr__ = __str__

class Wordle:
    """
        >>> p1 = Player('Susy')
        >>> p2 = Player('Taylor')
        >>> w1 = Wordle(p1, 'water')
        >>> w2 = Wordle(p2, 'cloud')
        >>> w3 = Wordle(p1, 'jewel')
        >>> w1.play('camel')
        '_A_E_'
        >>> w1.play('ranes')
        'rA_E_'
        >>> w1.play('baner')
        '_A_ER'
        >>> w1.play('pacer')
        '_A_ER'
        >>> w1.play('water')
        'You won the game'
        >>> w1.play('rocks')
        'Game over'
        >>> w1.play('other')
        'Game over'
        >>> w3.play('beast')
        '_E___'
        >>> w3.play('peace')
        '_E__e'
        >>> w3.play('keeks')
        '_Ee__'
        >>> w3.play('jewel')
        'You won the game'
        >>> w2.play('classes')
        'Guess must be 5 letters long'
        >>> w2.play('cs132')
        'Guess must be all letters'
        >>> w2.play('audio')
        '_ud_o'
        >>> w2.play('kudos')
        '_udo_'
        >>> w2.play('would')
        '_oulD'
        >>> w2.play('bound')
        '_ou_D'
        >>> w2.play('could')
        'CoulD'
        >>> w2.play('pound')
        'The word was cloud'
        >>> w2.play('final')
        'Game over'
        >>> p1
        *Game records for Susy*
        Total games: 2
        Games won: 2
        Games lost: 0
        Best game: 4 attempts
        >>> p2
        *Game records for Taylor*
        Total games: 1
        Games won: 0
        Games lost: 1
        Best game: None
    """

    # Class variable for max attempts
    max_attempts = 6

    def __init__(self, player, word):
        """Initialize Wordle game with player and target word."""
        self.user = player
        self.word = word.lower()
        self.attempts_used = 0
        self.game_over = False
        self.won = False

    def process_guess(self, guess):
        """Process guess and return feedback string."""
        # Validate guess length
        if len(guess) != 5:
            return "Guess must be 5 letters long"
        
        # Validate all characters are letters
        if not guess.isalpha():
            return "Guess must be all letters"
        
        guess = guess.lower()
        feedback = ""
        
        # Generate feedback for each letter position
        for i in range(5):
            guess_letter = guess[i]
            target_letter = self.word[i]
            
            if guess_letter == target_letter:
                # Correct letter in correct position - uppercase
                feedback += guess_letter.upper()
            elif guess_letter in self.word:
                # Correct letter in wrong position - lowercase
                feedback += guess_letter.lower()
            else:
                # Letter not in word - underscore
                feedback += "_"
        
        return feedback

    def play(self, guess):
        """Handle player guess and manage game state."""
        # First, check if the game is already finished
        if self.game_over:
            return "Game over"

        # 1. Increment the attempt counter immediately
        self.attempts_used += 1

        # 2. Validate the guess
        feedback = self.process_guess(guess)

        # 3. Check for a win (only possible with a valid guess)
        if guess.lower() == self.word:
            self.game_over = True
            self.user.update_win(self.attempts_used)
            return "You won the game"

        # 4. Check if the player is out of attempts (this covers all cases)
        if self.attempts_used >= self.max_attempts:
            self.game_over = True
            self.user.update_loss()
            return f"The word was {self.word}"
        
        # 5. If the game is not over, return the feedback (which could be a validation error)
        return feedback


# -------- SECTION 4
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line: 
    ''' 
        >>> p1 = Point2D(-7, -9)
        >>> p2 = Point2D(1, 5.6)
        >>> line1 = Line(p1, p2)
        >>> line1.getDistance
        16.648
        >>> line1.getSlope
        1.825
        >>> line1
        y = 1.825x + 3.775
        >>> line2 = line1*4
        >>> line2.getDistance
        66.592
        >>> line2.getSlope
        1.825
        >>> line2
        y = 1.825x + 15.1
        >>> line1
        y = 1.825x + 3.775
        >>> line3 = line1*4
        >>> line3
        y = 1.825x + 15.1
        >>> line5=Line(Point2D(6,48),Point2D(9,21))
        >>> line5
        y = -9.0x + 102.0
        >>> Point2D(45,3) in line5
        False
        >>> Point2D(34,-204) in line5
        True
        >>> line6=Line(Point2D(2,6), Point2D(2,3))
        >>> line6.getDistance
        3.0
        >>> line6.getSlope
        inf
        >>> isinstance(line6.getSlope, float)
        True
        >>> line6
        Undefined
        >>> line7=Line(Point2D(6,5), Point2D(9,5))
        >>> line7.getSlope
        0.0
        >>> line7
        y = 5.0
        >>> Point2D(9,5) in line7
        True
        >>> Point2D(89,5) in line7
        True
        >>> Point2D(12,8) in line7
        False
        >>> (9,5) in line7
        False
    '''
    def __init__(self, point1, point2):
        """Initialize line with two Point2D objects."""
        self.point1 = point1
        self.point2 = point2

    @property
    def getDistance(self):
        """Calculate distance between two points."""
        dx = self.point2.x - self.point1.x
        dy = self.point2.y - self.point1.y
        distance = math.sqrt(dx * dx + dy * dy)
        return round(distance, 3)
       
    @property
    def getSlope(self):
        """Calculate slope of the line."""
        dx = self.point2.x - self.point1.x
        dy = self.point2.y - self.point1.y
        
        # Handle vertical line (undefined slope)
        if dx == 0:
            return float('inf')
        
        # Calculate slope
        slope = dy / dx
        return round(slope, 3)

    @property
    def getIntercept(self):
        """Calculate y-intercept of the line."""
        slope = self.getSlope
        if slope == float('inf'):
            return None
        
        # Use point-slope form: b = y - mx
        intercept = self.point1.y - (slope * self.point1.x)
        return round(intercept, 3)

    def __str__(self):
        """Return string representation of line equation."""
        return self.__repr__()

    def __repr__(self):
        """Return line equation in slope-intercept form."""
        slope = self.getSlope
        
        # Handle undefined slope (vertical line)
        if slope == float('inf'):
            return "Undefined"
        
        intercept = self.getIntercept
        
        # Since we already handled vertical lines above, intercept should not be None here
        # But let's be safe and check anyway
        if intercept is None:
            return "Undefined"
        
        # Handle horizontal line (slope = 0)
        if slope == 0:
            return f"y = {intercept}"
        
        # Handle positive or zero intercept
        if intercept >= 0:
            return f"y = {slope}x + {intercept}"
        else:
            # Handle negative intercept - show as subtraction
            # Convert negative intercept to positive for display
            return f"y = {slope}x - {abs(intercept)}"

    def __mul__(self, other):
        """Multiply line by scalar, scaling both points."""
        if not isinstance(other, int):
            return None
        
        # Create new points by scaling coordinates
        new_point1 = Point2D(self.point1.x * other, self.point1.y * other)
        new_point2 = Point2D(self.point2.x * other, self.point2.y * other)
        
        return Line(new_point1, new_point2)

    def __contains__(self, point):
        """Check if point lies on the line."""
        if not isinstance(point, Point2D):
            return False
        
        slope = self.getSlope
        
        # Return False for vertical lines as specified
        if slope == float('inf'):
            return False
        
        # Check if point satisfies line equation
        intercept = self.getIntercept
        expected_y = slope * point.x + intercept
        
        # Use math.isclose to handle floating-point precision
        return math.isclose(point.y, expected_y)


def run_tests():
    import doctest

    # Run tests in all docstrings
    doctest.testmod(verbose=True)
    
    # Run tests per function - Uncomment the next line to run doctest by function. Replace Pantry with the name of the class you want to test
    doctest.run_docstring_examples(Pantry, globals(), name='LAB2',verbose=True)

if __name__ == "__main__":
    run_tests()