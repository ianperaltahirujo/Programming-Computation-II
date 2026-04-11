
import random, os

class Course:
    '''
        >>> c1 = Course('CMPSC132', 'Programming in Python II', 3)
        >>> c2 = Course('CMPSC360', 'Discrete Mathematics', 3)
        >>> c1 == c2
        False
        >>> c3 = Course('CMPSC132', 'Programming in Python II', 3)
        >>> c1 == c3
        True
        >>> c1
        CMPSC132(3): Programming in Python II
        >>> c2
        CMPSC360(3): Discrete Mathematics
        >>> c3
        CMPSC132(3): Programming in Python II
        >>> c1 == None
        False
        >>> print(c1)
        CMPSC132(3): Programming in Python II
    '''
    def __init__(self, cid, cname, credits):
        """Initialize a Course with course id, name, and credits."""
        self.cid = cid
        self.cname = cname
        self.credits = credits

    def __str__(self):
        """Return formatted string representation of the course."""
        return f"{self.cid}({self.credits}): {self.cname}"

    __repr__ = __str__

    def __eq__(self, other):
        """Check equality based on course id."""
        if not isinstance(other, Course):
            return False
        return self.cid == other.cid


class Catalog:
    ''' 
        >>> C = Catalog()
        >>> C.courseOfferings
        {}
        >>> C._loadCatalog("cmpsc_catalog_small.csv")
        >>> C.courseOfferings
        {'CMPSC 132': CMPSC 132(3): Programming and Computation II, 'MATH 230': MATH 230(4): Calculus and Vector Analysis, 'PHYS 213': PHYS 213(2): General Physics, 'CMPEN 270': CMPEN 270(4): Digital Design, 'CMPSC 311': CMPSC 311(3): Introduction to Systems Programming, 'CMPSC 360': CMPSC 360(3): Discrete Mathematics for Computer Science}
        >>> C.removeCourse('CMPSC 360')
        'Course removed successfully'
        >>> C.courseOfferings
        {'CMPSC 132': CMPSC 132(3): Programming and Computation II, 'MATH 230': MATH 230(4): Calculus and Vector Analysis, 'PHYS 213': PHYS 213(2): General Physics, 'CMPEN 270': CMPEN 270(4): Digital Design, 'CMPSC 311': CMPSC 311(3): Introduction to Systems Programming}
        >>> isinstance(C.courseOfferings['CMPSC 132'], Course)
        True
    '''

    def __init__(self):
        """Initialize empty catalog."""
        self.courseOfferings = {}

    def addCourse(self, cid, cname, credits):
        """Add a course to the catalog."""
        if cid in self.courseOfferings:
            return "Course already added"
        self.courseOfferings[cid] = Course(cid, cname, credits)
        return "Course added successfully"

    def removeCourse(self, cid):
        """Remove a course from the catalog."""
        if cid not in self.courseOfferings:
            return "Course not found"
        del self.courseOfferings[cid]
        return "Course removed successfully"

    def _loadCatalog(self, file):
        """Load courses from a CSV file."""
        target_path = os.path.join(os.path.dirname(__file__), file)
        with open(target_path, "r") as f:
            course_info = f.readlines()
        
        for line in course_info:
            line = line.strip()
            if line:  
                parts = line.split(',')
                if len(parts) == 3:
                    cid, cname, credits = parts[0], parts[1], int(parts[2])
                    self.addCourse(cid, cname, credits)


class Semester:
    '''
        >>> cmpsc131 = Course('CMPSC 131', 'Programming in Python I', 3)
        >>> cmpsc132 = Course('CMPSC 132', 'Programming in Python II', 3)
        >>> math230 = Course("MATH 230", 'Calculus', 4)
        >>> phys213 = Course("PHYS 213", 'General Physics', 2)
        >>> econ102 = Course("ECON 102", 'Intro to Economics', 3)
        >>> phil119 = Course("PHIL 119", 'Ethical Leadership', 3)
        >>> spr22 = Semester()
        >>> spr22
        No courses
        >>> spr22.addCourse(cmpsc132)
        >>> isinstance(spr22.courses['CMPSC 132'], Course)
        True
        >>> spr22.addCourse(math230)
        >>> spr22
        CMPSC 132; MATH 230
        >>> spr22.isFullTime
        False
        >>> spr22.totalCredits
        7
        >>> spr22.addCourse(phys213)
        >>> spr22.addCourse(econ102)
        >>> spr22.addCourse(econ102)
        'Course already added'
        >>> spr22.addCourse(phil119)
        >>> spr22.isFullTime
        True
        >>> spr22.dropCourse(phil119)
        >>> spr22.addCourse(Course("JAPNS 001", 'Japanese I', 4))
        >>> spr22.totalCredits
        16
        >>> spr22.dropCourse(cmpsc131)
        'No such course'
        >>> spr22.courses
        {'CMPSC 132': CMPSC 132(3): Programming in Python II, 'MATH 230': MATH 230(4): Calculus, 'PHYS 213': PHYS 213(2): General Physics, 'ECON 102': ECON 102(3): Intro to Economics, 'JAPNS 001': JAPNS 001(4): Japanese I}
    '''

    def __init__(self):
        """Initialize an empty semester."""
        self.courses = {}

    def __str__(self):
        """Return formatted string of all courses in semester."""
        if not self.courses:
            return "No courses"
        return "; ".join(self.courses.keys())

    __repr__ = __str__

    def addCourse(self, course):
        """Add a course to this semester."""
        if course.cid in self.courses:
            return "Course already added"
        self.courses[course.cid] = course

    def dropCourse(self, course):
        """Remove a course from this semester."""
        if course.cid not in self.courses:
            return "No such course"
        del self.courses[course.cid]

    @property
    def totalCredits(self):
        """Calculate total credits for this semester."""
        return sum(course.credits for course in self.courses.values())

    @property
    def isFullTime(self):
        """Check if this semester is full-time (12+ credits)."""
        return self.totalCredits >= 12

    
class Loan:
    '''
        >>> import random
        >>> random.seed(2)  # Setting seed to a fixed value, so you can predict what numbers the random module will generate
        >>> first_loan = Loan(4000)
        >>> first_loan
        Balance: $4000
        >>> first_loan.loan_id
        17412
        >>> second_loan = Loan(6000)
        >>> second_loan.amount
        6000
        >>> second_loan.loan_id
        22004
        >>> third_loan = Loan(1000)
        >>> third_loan.loan_id
        21124
    '''

    def __init__(self, amount):
        """Initialize a loan with an amount and pseudo-random ID."""
        self.amount = amount
        self.loan_id = self.__getloanID

    def __str__(self):
        """Return formatted string representation of the loan."""
        return f"Balance: ${self.amount}"

    __repr__ = __str__

    @property
    def __getloanID(self):
        """Generate a pseudo-random loan ID."""
        return random.randint(10000, 99999)


class Person:
    '''
        >>> p1 = Person('Jason Lee', '204-99-2890')
        >>> p2 = Person('Karen Lee', '247-01-2670')
        >>> p1
        Person(Jason Lee, ***-**-2890)
        >>> p2
        Person(Karen Lee, ***-**-2670)
        >>> p3 = Person('Karen Smith', '247-01-2670')
        >>> p3
        Person(Karen Smith, ***-**-2670)
        >>> p2 == p3
        True
        >>> p1 == p2
        False
    '''

    def __init__(self, name, ssn):
        """Initialize a person with name and SSN."""
        self.name = name
        self._ssn = ssn

    def __str__(self):
        """Return formatted string with masked SSN."""
        last_four = self._ssn[-4:]
        return f"Person({self.name}, ***-**-{last_four})"

    __repr__ = __str__

    def get_ssn(self):
        """Return the social security number."""
        return self._ssn

    def __eq__(self, other):
        """Check equality based on SSN."""
        if not isinstance(other, Person):
            return False
        return self._ssn == other._ssn


class Staff(Person):
    '''
        >>> C = Catalog()
        >>> C._loadCatalog("cmpsc_catalog_small.csv")
        >>> s1 = Staff('Jane Doe', '214-49-2890')
        >>> s1.getSupervisor
        >>> s2 = Staff('John Doe', '614-49-6590', s1)
        >>> s2.getSupervisor
        Staff(Jane Doe, 905jd2890)
        >>> s1 == s2
        False
        >>> s2.id
        '905jd6590'
        >>> p = Person('Jason Smith', '221-11-2629')
        >>> st1 = s1.createStudent(p)
        >>> isinstance(st1, Student)
        True
        >>> s2.applyHold(st1)
        'Completed!'
        >>> st1.registerSemester()
        'Unsuccessful operation'
        >>> s2.removeHold(st1)
        'Completed!'
        >>> st1.registerSemester()
        >>> st1.enrollCourse('CMPSC 132', C)
        'Course added successfully'
        >>> st1.semesters
        {1: CMPSC 132}
        >>> s1.applyHold(st1)
        'Completed!'
        >>> st1.enrollCourse('CMPSC 360', C)
        'Unsuccessful operation'
        >>> st1.semesters
        {1: CMPSC 132}
    '''
    def __init__(self, name, ssn, supervisor=None):
        """Initialize staff member with optional supervisor."""
        super().__init__(name, ssn)
        self._supervisor = supervisor

    def __str__(self):
        """Return formatted string representation of staff member."""
        return f"Staff({self.name}, {self.id})"

    __repr__ = __str__

    @property
    def id(self):
        """Generate staff ID from initials and last 4 digits of SSN."""
        initials = ''.join([word[0].lower() for word in self.name.split()])
        last_four = self._ssn[-4:]
        return f"905{initials}{last_four}"

    @property   
    def getSupervisor(self):
        """Get the supervisor of this staff member."""
        return self._supervisor

    def setSupervisor(self, new_supervisor):
        """Set a new supervisor for this staff member."""
        if isinstance(new_supervisor, Staff):
            self._supervisor = new_supervisor
            return "Completed!"

    def applyHold(self, student):
        """Apply a hold to a student account."""
        if isinstance(student, Student):
            student.hold = True
            return "Completed!"

    def removeHold(self, student):
        """Remove a hold from a student account."""
        if isinstance(student, Student):
            student.hold = False
            return "Completed!"

    def unenrollStudent(self, student):
        """Unenroll a student (set active to False)."""
        if isinstance(student, Student):
            student.active = False
            return "Completed!"

    def createStudent(self, person):
        """Create a Student object from a Person object."""
        return Student(person.name, person.get_ssn(), "Freshman")


class Student(Person):
    '''
        >>> C = Catalog()
        >>> C._loadCatalog("cmpsc_catalog_small.csv")
        >>> s1 = Student('Jason Lee', '204-99-2890', 'Freshman')
        >>> s1
        Student(Jason Lee, jl2890, Freshman)
        >>> s2 = Student('Karen Lee', '247-01-2670', 'Freshman')
        >>> s2
        Student(Karen Lee, kl2670, Freshman)
        >>> s1 == s2
        False
        >>> s1.id
        'jl2890'
        >>> s2.id
        'kl2670'
        >>> s1.registerSemester()
        >>> s1.enrollCourse('CMPSC 132', C)
        'Course added successfully'
        >>> s1.semesters
        {1: CMPSC 132}
        >>> s1.enrollCourse('CMPSC 360', C)
        'Course added successfully'
        >>> s1.enrollCourse('CMPSC 465', C)
        'Course not found'
        >>> s1.semesters
        {1: CMPSC 132; CMPSC 360}
        >>> s2.semesters
        {}
        >>> s1.enrollCourse('CMPSC 132', C)
        'Course already enrolled'
        >>> s1.dropCourse('CMPSC 360')
        'Course dropped successfully'
        >>> s1.dropCourse('CMPSC 360')
        'Course not found'
        >>> s1.semesters
        {1: CMPSC 132}
        >>> s1.registerSemester()
        >>> s1.semesters
        {1: CMPSC 132, 2: No courses}
        >>> s1.enrollCourse('CMPSC 360', C)
        'Course added successfully'
        >>> s1.semesters
        {1: CMPSC 132, 2: CMPSC 360}
        >>> s1.registerSemester()
        >>> s1.semesters
        {1: CMPSC 132, 2: CMPSC 360, 3: No courses}
        >>> s1
        Student(Jason Lee, jl2890, Sophomore)
        >>> s1.classCode
        'Sophomore'
    '''
    def __init__(self, name, ssn, year):
        random.seed(1)
        super().__init__(name, ssn)
        self.classCode = year
        self.semesters = {}
        self.hold = False
        self.active = True
        self.account = self.__createStudentAccount()

    def __str__(self):
        """Return formatted string representation of student."""
        return f"Student({self.name}, {self.id}, {self.classCode})"

    __repr__ = __str__

    def __createStudentAccount(self):
        """Create a StudentAccount object for this student."""
        if self.active:
            return StudentAccount(self)

    @property
    def id(self):
        """Generate student ID from initials and last 4 digits of SSN."""
        initials = ''.join([word[0].lower() for word in self.name.split()])
        last_four = self._ssn[-4:]
        return f"{initials}{last_four}"

    def registerSemester(self):
        """Register for a new semester if active and no holds."""
        if not self.active or self.hold:
            return "Unsuccessful operation"
        
        if not self.semesters:
            semester_num = 1
        else:
            semester_num = max(self.semesters.keys()) + 1
        
        self.semesters[semester_num] = Semester()
        
        if semester_num <= 2:
            self.classCode = "Freshman"
        elif semester_num <= 4:
            self.classCode = "Sophomore"
        elif semester_num <= 6:
            self.classCode = "Junior"
        else:
            self.classCode = "Senior"

    def enrollCourse(self, cid, catalog):
        """Enroll in a course from the catalog."""
        if not self.active or self.hold:
            return "Unsuccessful operation"
        
        if cid not in catalog.courseOfferings:
            return "Course not found"
        
        if not self.semesters:
            return "Unsuccessful operation"
        
        current_semester_key = max(self.semesters.keys())
        current_semester = self.semesters[current_semester_key]
        
        if cid in current_semester.courses:
            return "Course already enrolled"
        
        course = catalog.courseOfferings[cid]
        current_semester.addCourse(course)
        
        cost = course.credits * self.account.CREDIT_PRICE
        self.account.chargeAccount(cost)
        
        return "Course added successfully"

    def dropCourse(self, cid):
        """Drop a course from current semester."""
        if not self.active or self.hold:
            return "Unsuccessful operation"
        
        if not self.semesters:
            return "Course not found"
        
        current_semester_key = max(self.semesters.keys())
        current_semester = self.semesters[current_semester_key]
        
        if cid not in current_semester.courses:
            return "Course not found"
        
        course = current_semester.courses[cid]
        current_semester.dropCourse(course)
        
        refund = (course.credits * self.account.CREDIT_PRICE) / 2
        self.account.makePayment(refund)
        
        return "Course dropped successfully"

    def getLoan(self, amount):
        """Get a loan if active and enrolled full-time."""
        if not self.active:
            return "Unsuccessful operation"
        
        if not self.semesters:
            return "Not full-time"
        
        current_semester_key = max(self.semesters.keys())
        current_semester = self.semesters[current_semester_key]
        
        if not current_semester.isFullTime:
            return "Not full-time"
        
        loan = Loan(amount)
        self.account.loans[loan.loan_id] = loan
        self.account.makePayment(amount)


class StudentAccount:
    '''
        >>> C = Catalog()
        >>> C._loadCatalog("cmpsc_catalog_small.csv")
        >>> s1 = Student('Jason Lee', '204-99-2890', 'Freshman')
        >>> s1.registerSemester()
        >>> s1.enrollCourse('CMPSC 132', C)
        'Course added successfully'
        >>> s1.account.balance
        3000
        >>> s1.enrollCourse('CMPSC 360', C)
        'Course added successfully'
        >>> s1.account.balance
        6000
        >>> s1.enrollCourse('MATH 230', C)
        'Course added successfully'
        >>> s1.account.balance
        10000
        >>> s1.enrollCourse('PHYS 213', C)
        'Course added successfully'
        >>> print(s1.account)
        Name: Jason Lee
        ID: jl2890
        Balance: $12000
        >>> s1.account.chargeAccount(100)
        12100
        >>> s1.account.balance
        12100
        >>> s1.account.makePayment(200)
        11900
        >>> s1.getLoan(4000)
        >>> s1.account.balance
        7900
        >>> s1.getLoan(8000)
        >>> s1.account.balance
        -100
        >>> s1.enrollCourse('CMPEN 270', C)
        'Course added successfully'
        >>> s1.account.balance
        3900
        >>> s1.dropCourse('CMPEN 270')
        'Course dropped successfully'
        >>> s1.account.balance
        1900.0
        >>> s1.account.loans
        {27611: Balance: $4000, 84606: Balance: $8000}
        >>> StudentAccount.CREDIT_PRICE = 1500
        >>> s2 = Student('Thomas Wang', '123-45-6789', 'Freshman')
        >>> s2.registerSemester()
        >>> s2.enrollCourse('CMPSC 132', C)
        'Course added successfully'
        >>> s2.account.balance
        4500
        >>> s1.enrollCourse('CMPEN 270', C)
        'Course added successfully'
        >>> s1.account.balance
        7900.0
    '''
    
    CREDIT_PRICE = 1000  
    
    def __init__(self, student):
        """Initialize student account."""
        self.student = student
        self.balance = 0
        self.loans = {}

    def __str__(self):
        """Return formatted string representation of account."""
        return f"Name: {self.student.name}\nID: {self.student.id}\nBalance: ${self.balance}"

    __repr__ = __str__

    def makePayment(self, amount):
        """Make a payment towards the balance."""
        self.balance -= amount
        return self.balance

    def chargeAccount(self, amount):
        """Charge an amount to the account."""
        self.balance += amount
        return self.balance


def run_tests():
    import doctest

    # Run tests in all docstrings
    doctest.testmod(verbose=True)
    
    # Run tests per function - Uncomment the next line to run doctest by function. Replace Course with the name of the function you want to test
    doctest.run_docstring_examples(Course, globals(), name='HW2',verbose=True)   

if __name__ == "__main__":
    run_tests()