
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        
    def __str__(self):
        return ("Node({})".format(self.value)) 

    __repr__ = __str__


class BinarySearchTree:
    """
        >>> my_tree = BinarySearchTree() 
        >>> my_tree.isEmpty()
        True
        >>> my_tree.isBalanced
        True
        >>> my_tree.insert(9) 
        >>> my_tree.insert(5) 
        >>> my_tree.insert(14) 
        >>> my_tree.insert(4)  
        >>> my_tree.insert(6) 
        >>> my_tree.insert(5.5) 
        >>> my_tree.insert(7)   
        >>> my_tree.insert(25) 
        >>> my_tree.insert(23) 
        >>> my_tree.getMin
        4
        >>> my_tree.getMax
        25
        >>> 67 in my_tree
        False
        >>> 5.5 in my_tree
        True
        >>> my_tree.isEmpty()
        False
        >>> my_tree.getHeight(my_tree.root)   # Height of the tree
        3
        >>> my_tree.getHeight(my_tree.root.left.right)
        1
        >>> my_tree.getHeight(my_tree.root.right)
        2
        >>> my_tree.getHeight(my_tree.root.right.right)
        1
        >>> my_tree.isBalanced
        False
        >>> my_tree.insert(10)
        >>> my_tree.isBalanced
        True
    """
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root=Node(value)
        else:
            self._insert(self.root, value)

    def _insert(self, node, value):
        if(value<node.value):
            if(node.left==None):
                node.left = Node(value)
            else:
                self._insert(node.left, value)
        else:   
            if(node.right==None):
                node.right = Node(value)
            else:
                self._insert(node.right, value)
    

    def isEmpty(self):
        """
        Tests to see whether the tree is empty or not.
        
        Returns:
            bool: True if the tree is empty, False otherwise
        """
        return self.root is None


    @property
    def getMin(self):
        """
        Property method that returns the minimum node value in the tree.
        Uses BST property: minimum value is in the leftmost node.
        
        Returns:
            int or float: The value of the node with minimum value
            None: If the tree is empty
        """
        if self.isEmpty():
            return None
        
        current = self.root
        # Traverse to the leftmost node
        while current.left is not None:
            current = current.left
        return current.value


    @property
    def getMax(self):
        """
        Property method that returns the maximum node value in the tree.
        Uses BST property: maximum value is in the rightmost node.
        
        Returns:
            int or float: The value of the node with maximum value
            None: If the tree is empty
        """
        if self.isEmpty():
            return None
        
        current = self.root
        # Traverse to the rightmost node
        while current.right is not None:
            current = current.right
        return current.value


    def __contains__(self, value):
        """
        Checks if a value is present in the tree by overloading the in operator.
        Uses BST property to efficiently search for the value.
        
        Args:
            value (int or float): The value to check if it exists in the tree
            
        Returns:
            bool: True if the value is in the tree, False otherwise
        """
        return self._contains_helper(self.root, value)
    
    def _contains_helper(self, node, value):
        """
        Recursive helper method for checking if a value exists in the tree.
        
        Args:
            node (Node): Current node being examined
            value (int or float): The value to search for
            
        Returns:
            bool: True if value is found, False otherwise
        """
        # Base case: reached end of branch without finding value
        if node is None:
            return False
        
        # Found the value
        if node.value == value:
            return True
        
        # Search left subtree if value is less than current node
        if value < node.value:
            return self._contains_helper(node.left, value)
        # Search right subtree if value is greater than current node
        else:
            return self._contains_helper(node.right, value)


    def getHeight(self, node):
        """
        Gets the height of a node in the tree.
        Height is the number of edges from the node to the deepest leaf.
        
        Args:
            node (Node): The node to check the height of
            
        Returns:
            int: The height of the node in the tree
        """
        # Base case: empty node has height -1
        if node is None:
            return -1
        
        # Calculate height of left and right subtrees
        left_height = self.getHeight(node.left)
        right_height = self.getHeight(node.right)
        
        # Height is 1 + maximum of left and right subtree heights
        return 1 + max(left_height, right_height)

    @property
    def isBalanced(self):  # Do not modify this method
        return self.isBalanced_helper(self.root)
    
    
    def isBalanced_helper(self, node):
        """
        Checks if the tree is balanced starting from the given node.
        A tree is balanced when for every node, the heights of left and 
        right subtrees differ by at most 1.
        
        Args:
            node (Node): The node to check the balance condition of
            
        Returns:
            bool: True if tree is balanced, False otherwise
        """
        # Base case: empty tree is balanced
        if node is None:
            return True
        
        # Calculate heights of left and right subtrees
        left_height = self.getHeight(node.left)
        right_height = self.getHeight(node.right)
        
        # Check balance condition for current node
        balance = abs(left_height - right_height)
        if balance > 1:
            return False
        
        # Check if left and right subtrees are balanced
        left_balanced = self.isBalanced_helper(node.left)
        right_balanced = self.isBalanced_helper(node.right)
        
        # Tree is balanced if current node is balanced AND both subtrees are balanced
        return left_balanced and right_balanced



def run_tests():
    import doctest
    doctest.testmod(verbose=True)
    
if __name__ == "__main__":
    run_tests()