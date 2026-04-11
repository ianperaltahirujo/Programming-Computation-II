
class Node:   # You are not allowed to modify this class
    def __init__(self, value=None):  
        self.next = None
        self.value = value
    
    def __str__(self):
        return f"Node({self.value})"

    __repr__ = __str__

class Malloc_Library:

    """
    ** This is NOT a comprehensive test sample, test beyond this doctest
        >>> lst = Malloc_Library()
        >>> lst
        <BLANKLINE>
        >>> lst.malloc(5)
        >>> lst
        None -> None -> None -> None -> None
        >>> lst[0] = 23
        >>> lst
        23 -> None -> None -> None -> None
        >>> lst[0]
        23
        >>> lst[1]
        >>> lst.realloc(1)
        >>> lst
        23
        >>> lst.calloc(5)
        >>> lst
        0 -> 0 -> 0 -> 0 -> 0
        >>> lst.calloc(10)
        >>> lst[3] = 5
        >>> lst[8] = 23
        >>> lst
        0 -> 0 -> 0 -> 5 -> 0 -> 0 -> 0 -> 0 -> 23 -> 0
        >>> lst.realloc(5)
        >>> lst
        0 -> 0 -> 0 -> 5 -> 0
        >>> other_lst = Malloc_Library()
        >>> other_lst.realloc(9)
        >>> other_lst[0] = 12
        >>> other_lst[5] = 56
        >>> other_lst[8] = 6925
        >>> other_lst[10] = 78
        Traceback (most recent call last):
            ...
        IndexError
        >>> other_lst.memcpy(2, lst, 0, 5)
        >>> lst
        None -> None -> None -> 56 -> None
        >>> other_lst
        12 -> None -> None -> None -> None -> 56 -> None -> None -> 6925
        >>> temp = lst.head.next.next
        >>> lst.free()
        >>> temp.next is None
        True
    """

    def __init__(self): # You are not allowed to modify the constructor
        self.head = None
    
    def __repr__(self):  # You are not allowed to modify this method
        current = self.head
        out = []
        while current != None:
            out.append(str(current.value))
            current = current.next
        return " -> ".join(out)

    __str__ = __repr__
    
    def __len__(self):
        """Returns the number of nodes in the linked list"""
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.next
        return count

    
    def __setitem__(self, pos, value):
        """Sets the node at the given position to the value specified"""
        if pos < 0 or pos >= len(self):
            raise IndexError
        
        current = self.head
        index = 0
        while index < pos:
            current = current.next
            index += 1
        current.value = value


    def __getitem__(self, pos):
        """Returns the value of the node at the given position"""
        if self.head is None:
            return None
        
        if pos < 0 or pos >= len(self):
            raise IndexError
        
        current = self.head
        index = 0
        while index < pos:
            current = current.next
            index += 1
        return current.value
    

    def malloc(self, size):
        """Creates a linked list with length specified by size parameter.
        Initializes all values of each Node to None"""
        self.head = None
        
        if size <= 0:
            return
        
        # Create first node
        self.head = Node(None)
        current = self.head
        
        # Create remaining nodes
        count = 1
        while count < size:
            current.next = Node(None)
            current = current.next
            count += 1


    def calloc(self, size):
        """Creates a linked list with length specified by size parameter.
        Initializes all values of each Node to 0"""
        self.head = None
        
        if size <= 0:
            return
        
        # Create first node
        self.head = Node(0)
        current = self.head
        
        # Create remaining nodes
        count = 1
        while count < size:
            current.next = Node(0)
            current = current.next
            count += 1


    def free(self):
        """Clears the linked list by unlinking all nodes in the list"""
        current = self.head
        while current is not None:
            next_node = current.next
            current.next = None
            current = next_node
        self.head = None


    def realloc(self, size):
        """Reallocates the memory (resizes list) to be of the size specified"""
        current_length = len(self)
        
        # If size is 0, deallocate memory
        if size == 0:
            self.free()
            return
        
        # If list is empty, act as malloc
        if self.head is None:
            self.malloc(size)
            return
        
        # If size is greater than current length, extend the list
        if size > current_length:
            current = self.head
            while current.next is not None:
                current = current.next
            
            # Add new nodes
            count = current_length
            while count < size:
                current.next = Node(None)
                current = current.next
                count += 1
        
        # If size is smaller than current length, remove nodes from end
        elif size < current_length:
            if size == 1:
                # Special case: keep only head node
                current = self.head.next
                self.head.next = None
                # Unlink remaining nodes
                while current is not None:
                    next_node = current.next
                    current.next = None
                    current = next_node
            else:
                # Go to the node before the cutoff point
                current = self.head
                count = 1
                while count < size:
                    current = current.next
                    count += 1
                
                # Unlink and free the rest
                to_delete = current.next
                current.next = None
                while to_delete is not None:
                    next_node = to_delete.next
                    to_delete.next = None
                    to_delete = next_node



    def memcpy(self, ptr1_start_idx, pointer_2, ptr2_start_idx, size):
        """Copies values from one list (self) to another (pointer_2)
        starting at specified positions and up to a given number of nodes"""
        # If either list has no memory allocated, do nothing
        if self.head is None or pointer_2.head is None:
            return
        
        # Get lengths of both lists
        len1 = len(self)
        len2 = len(pointer_2)
        
        # Check if starting indices are valid
        if ptr1_start_idx < 0 or ptr1_start_idx >= len1:
            return
        if ptr2_start_idx < 0 or ptr2_start_idx >= len2:
            return
        
        # Adjust size if it's larger than the source list's available elements
        available_in_source = len1 - ptr1_start_idx
        if size > available_in_source:
            size = available_in_source
        
        # Navigate to starting position in source list (self)
        current_src = self.head
        index = 0
        while index < ptr1_start_idx:
            current_src = current_src.next
            index += 1
        
        # Navigate to starting position in destination list (pointer_2)
        current_dest = pointer_2.head
        index = 0
        while index < ptr2_start_idx:
            current_dest = current_dest.next
            index += 1
        
        copied = 0
        while copied < size and current_src is not None and current_dest is not None:
            current_dest.value = current_src.value
            current_src = current_src.next
            current_dest = current_dest.next
            copied += 1
    


def run_tests():
    import doctest
    doctest.testmod(verbose=True)
     

if __name__ == "__main__":
     run_tests()