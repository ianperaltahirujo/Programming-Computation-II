

class Node:
    def __init__(self, content):
        self.value = content
        self.next = None
        self.previous = None

    def __str__(self):
        return ('CONTENT:{}\n'.format(self.value))

    __repr__=__str__


class ContentItem:
    '''
        >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
        >>> content2 = ContentItem(1004, 50, "Content-Type: 1", "110010")
        >>> content3 = ContentItem(1005, 18, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
        >>> content4 = ContentItem(1005, 18, "another header", "111110")
        >>> hash(content1)
        0
        >>> hash(content2)
        1
        >>> hash(content3)
        2
        >>> hash(content4)
        1
    '''
    def __init__(self, cid, size, header, content):
        self.cid = cid
        self.size = size
        self.header = header
        self.content = content

    def __str__(self):
        return f'CONTENT ID: {self.cid} SIZE: {self.size} HEADER: {self.header} CONTENT: {self.content}'

    __repr__=__str__

    def __eq__(self, other):
        if isinstance(other, ContentItem):
            return self.cid == other.cid and self.size == other.size and self.header == other.header and self.content == other.content
        return False

    def __hash__(self):
        # Sum all ASCII values in header and modulo 3
        total = sum(ord(c) for c in self.header)
        return total % 3


class CacheList:
    ''' 
        >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
        >>> content2 = ContentItem(1004, 50, "Content-Type: 1", "110010")
        >>> content3 = ContentItem(1005, 180, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
        >>> content4 = ContentItem(1006, 18, "another header", "111110")
        >>> content5 = ContentItem(1008, 2, "items", "11x1110")
        >>> lst=CacheList(200)
        >>> lst
        REMAINING SPACE:200
        ITEMS:0
        LIST:
        <BLANKLINE>
        >>> lst.put(content1, 'mru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> lst.put(content2, 'lru')
        'INSERTED: CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010'
        >>> lst.put(content4, 'mru')
        'INSERTED: CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110'
        >>> lst.put(content5, 'mru')
        'INSERTED: CONTENT ID: 1008 SIZE: 2 HEADER: items CONTENT: 11x1110'
        >>> lst.put(content3, 'lru')
        "INSERTED: CONTENT ID: 1005 SIZE: 180 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>"
        >>> lst.put(content1, 'mru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> 1006 in lst
        True
        >>> contentExtra = ContentItem(1034, 2, "items", "other content")
        >>> lst.update(1008, contentExtra)
        'UPDATED: CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content'
        >>> lst
        REMAINING SPACE:170
        ITEMS:3
        LIST:
        [CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content]
        [CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        <BLANKLINE>
        >>> lst.tail.value
        CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA
        >>> lst.tail.previous.value
        CONTENT ID: 1006 SIZE: 18 HEADER: another header CONTENT: 111110
        >>> lst.tail.previous.previous.value
        CONTENT ID: 1034 SIZE: 2 HEADER: items CONTENT: other content
        >>> lst.tail.previous.previous is lst.head
        True
        >>> lst.tail.previous.previous.previous is None
        True
        >>> lst.clear()
        'Cleared cache!'
        >>> lst
        REMAINING SPACE:200
        ITEMS:0
        LIST:
        <BLANKLINE>
    '''
    def __init__(self, size):
        self.head = None
        self.tail = None
        self.maxSize = size
        self.remainingSpace = size
        self.numItems = 0

    def __str__(self):
        listString = ""
        current = self.head
        while current is not None:
            listString += "[" + str(current.value) + "]\n"
            current = current.next
        return 'REMAINING SPACE:{}\nITEMS:{}\nLIST:\n{}'.format(self.remainingSpace, self.numItems, listString)  

    __repr__=__str__

    def __len__(self):
        return self.numItems
    
    def put(self, content, evictionPolicy):
        # Check if content is larger than max size
        if content.size > self.maxSize:
            return 'Insertion not allowed'
        
        # Check if content id already exists
        if content.cid in self:
            return f'Content {content.cid} already in cache, insertion not allowed'
        
        # Evict items if necessary
        while self.remainingSpace < content.size:
            if evictionPolicy == 'lru':
                self.lruEvict()
            else:  
                self.mruEvict()
        
        # Create new node and add at beginning
        new_node = Node(content)
        
        if self.head is None:
            # Empty list
            self.head = new_node
            self.tail = new_node
        else:
            # Add at beginning
            new_node.next = self.head
            self.head.previous = new_node
            self.head = new_node
        
        self.remainingSpace -= content.size
        self.numItems += 1
        
        return f'INSERTED: {content}'

    def __contains__(self, cid):
        current = self.head
        
        while current is not None:
            if current.value.cid == cid:
                # Move to front if not already there
                if current != self.head:
                    # Remove from current position
                    if current == self.tail:
                        self.tail = current.previous
                        self.tail.next = None
                    else:
                        current.previous.next = current.next
                        current.next.previous = current.previous
                    
                    # Add at beginning
                    current.previous = None
                    current.next = self.head
                    self.head.previous = current
                    self.head = current
                
                return True
            current = current.next
        
        return False

    def update(self, cid, content):
        current = self.head
        
        while current is not None:
            if current.value.cid == cid:
                old_size = current.value.size
                new_size = content.size
                size_diff = new_size - old_size
                
                # Check if update would exceed maxSize
                if size_diff > self.remainingSpace:
                    # Move to front but don't update
                    if current != self.head:
                        # Remove from current position
                        if current == self.tail:
                            self.tail = current.previous
                            self.tail.next = None
                        else:
                            current.previous.next = current.next
                            current.next.previous = current.previous
                        
                        # Add at beginning
                        current.previous = None
                        current.next = self.head
                        self.head.previous = current
                        self.head = current
                    
                    return 'Cache miss!'
                
                # Update the content
                current.value = content
                self.remainingSpace -= size_diff
                
                # Move to front if not already there
                if current != self.head:
                    # Remove from current position
                    if current == self.tail:
                        self.tail = current.previous
                        self.tail.next = None
                    else:
                        current.previous.next = current.next
                        current.next.previous = current.previous
                    
                    # Add at beginning
                    current.previous = None
                    current.next = self.head
                    self.head.previous = current
                    self.head = current
                
                return f'UPDATED: {content}'
            
            current = current.next
        
        return 'Cache miss!'

    def mruEvict(self):
        if self.head is None:
            return
        
        # Remove first item
        removed = self.head
        self.remainingSpace += removed.value.size
        self.numItems -= 1
        
        if self.head == self.tail:
            # Only one item
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.previous = None

    def lruEvict(self):
        if self.tail is None:
            return
        
        # Remove last item 
        removed = self.tail
        self.remainingSpace += removed.value.size
        self.numItems -= 1
        
        if self.head == self.tail:
            # Only one item
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.previous
            self.tail.next = None

    def clear(self):
        # Unlink all nodes
        current = self.head
        while current is not None:
            next_node = current.next
            current.previous = None
            current.next = None
            current = next_node
        
        self.head = None
        self.tail = None
        self.remainingSpace = self.maxSize
        self.numItems = 0
        
        return 'Cleared cache!'


class Cache:
    """
        >>> cache = Cache(205)
        >>> content1 = ContentItem(1000, 10, "Content-Type: 0", "0xA")
        >>> content2 = ContentItem(1003, 13, "Content-Type: 0", "0xD")
        >>> content3 = ContentItem(1008, 242, "Content-Type: 0", "0xF2")
        >>> content4 = ContentItem(1004, 50, "Content-Type: 1", "110010")
        >>> content5 = ContentItem(1001, 51, "Content-Type: 1", "110011")
        >>> content6 = ContentItem(1007, 155, "Content-Type: 1", "10011011")
        >>> content7 = ContentItem(1005, 23, "Content-Type: 2", "<html><p>'CMPSC132'</p></html>")
        >>> content8 = ContentItem(1002, 14, "Content-Type: 2", "<html><h2>'PSU'</h2></html>")
        >>> content9 = ContentItem(1006, 170, "Content-Type: 2", "<html><button>'Click Me'</button></html>")

        >>> cache.insert(content1, 'lru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> cache.insert(content2, 'lru')
        'INSERTED: CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD'
        >>> cache.insert(content3, 'lru')
        'Insertion not allowed'

        >>> cache.insert(content4, 'lru')
        'INSERTED: CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010'
        >>> cache.insert(content5, 'lru')
        'INSERTED: CONTENT ID: 1001 SIZE: 51 HEADER: Content-Type: 1 CONTENT: 110011'
        >>> cache.insert(content6, 'lru')
        'INSERTED: CONTENT ID: 1007 SIZE: 155 HEADER: Content-Type: 1 CONTENT: 10011011'

        >>> cache.insert(content7, 'lru')
        "INSERTED: CONTENT ID: 1005 SIZE: 23 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>"
        >>> cache.insert(content8, 'lru')
        "INSERTED: CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>"
        >>> cache.insert(content9, 'lru')
        "INSERTED: CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>"
        >>> cache
        L1 CACHE:
        REMAINING SPACE:182
        ITEMS:2
        LIST:
        [CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        <BLANKLINE>
        L2 CACHE:
        REMAINING SPACE:50
        ITEMS:1
        LIST:
        [CONTENT ID: 1007 SIZE: 155 HEADER: Content-Type: 1 CONTENT: 10011011]
        <BLANKLINE>
        L3 CACHE:
        REMAINING SPACE:21
        ITEMS:2
        LIST:
        [CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>]
        [CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>]
        <BLANKLINE>
        <BLANKLINE>
        >>> cache.hierarchy[0].clear()
        'Cleared cache!'
        >>> cache.hierarchy[1].clear()
        'Cleared cache!'
        >>> cache.hierarchy[2].clear()
        'Cleared cache!'
        >>> cache
        L1 CACHE:
        REMAINING SPACE:205
        ITEMS:0
        LIST:
        <BLANKLINE>
        L2 CACHE:
        REMAINING SPACE:205
        ITEMS:0
        LIST:
        <BLANKLINE>
        L3 CACHE:
        REMAINING SPACE:205
        ITEMS:0
        LIST:
        <BLANKLINE>
        <BLANKLINE>
        >>> cache.insert(content1, 'mru')
        'INSERTED: CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA'
        >>> cache.insert(content2, 'mru')
        'INSERTED: CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD'
        >>> cache[content1].value
        CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA
        >>> cache[content2].value
        CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD
        >>> cache[content3]
        'Cache miss!'
        >>> cache.insert(content5, 'lru')
        'INSERTED: CONTENT ID: 1001 SIZE: 51 HEADER: Content-Type: 1 CONTENT: 110011'
        >>> content6 = ContentItem(1007, 160, "Content-Type: 1", "10011011")
        >>> cache.insert(content6, 'lru')
        'INSERTED: CONTENT ID: 1007 SIZE: 160 HEADER: Content-Type: 1 CONTENT: 10011011'
        >>> cache.insert(content4, 'lru')
        'INSERTED: CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010'
        >>> cache.insert(content7, 'mru')
        "INSERTED: CONTENT ID: 1005 SIZE: 23 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>"
        >>> cache.insert(content8, 'mru')
        "INSERTED: CONTENT ID: 1002 SIZE: 14 HEADER: Content-Type: 2 CONTENT: <html><h2>'PSU'</h2></html>"
        >>> cache.insert(content9, 'mru')
        "INSERTED: CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>"
        >>> cache
        L1 CACHE:
        REMAINING SPACE:182
        ITEMS:2
        LIST:
        [CONTENT ID: 1003 SIZE: 13 HEADER: Content-Type: 0 CONTENT: 0xD]
        [CONTENT ID: 1000 SIZE: 10 HEADER: Content-Type: 0 CONTENT: 0xA]
        <BLANKLINE>
        L2 CACHE:
        REMAINING SPACE:155
        ITEMS:1
        LIST:
        [CONTENT ID: 1004 SIZE: 50 HEADER: Content-Type: 1 CONTENT: 110010]
        <BLANKLINE>
        L3 CACHE:
        REMAINING SPACE:12
        ITEMS:2
        LIST:
        [CONTENT ID: 1006 SIZE: 170 HEADER: Content-Type: 2 CONTENT: <html><button>'Click Me'</button></html>]
        [CONTENT ID: 1005 SIZE: 23 HEADER: Content-Type: 2 CONTENT: <html><p>'CMPSC132'</p></html>]
        <BLANKLINE>
        <BLANKLINE>
        >>> cache.clear()
        'Cache cleared!'
        >>> contentA = ContentItem(2000, 52, "Content-Type: 2", "GET https://www.pro-football-reference.com/boxscores/201802040nwe.htm HTTP/1.1")
        >>> contentB = ContentItem(2001, 76, "Content-Type: 2", "GET https://giphy.com/gifs/93lCI4D0murAszeyA6/html5 HTTP/1.1")
        >>> contentC = ContentItem(2002, 11, "Content-Type: 2", "GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1")
        >>> cache.insert(contentA, 'lru')
        'INSERTED: CONTENT ID: 2000 SIZE: 52 HEADER: Content-Type: 2 CONTENT: GET https://www.pro-football-reference.com/boxscores/201802040nwe.htm HTTP/1.1'
        >>> cache.insert(contentB, 'lru')
        'INSERTED: CONTENT ID: 2001 SIZE: 76 HEADER: Content-Type: 2 CONTENT: GET https://giphy.com/gifs/93lCI4D0murAszeyA6/html5 HTTP/1.1'
        >>> cache.insert(contentC, 'lru')
        'INSERTED: CONTENT ID: 2002 SIZE: 11 HEADER: Content-Type: 2 CONTENT: GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1'
        >>> cache.hierarchy[2]
        REMAINING SPACE:66
        ITEMS:3
        LIST:
        [CONTENT ID: 2002 SIZE: 11 HEADER: Content-Type: 2 CONTENT: GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1]
        [CONTENT ID: 2001 SIZE: 76 HEADER: Content-Type: 2 CONTENT: GET https://giphy.com/gifs/93lCI4D0murAszeyA6/html5 HTTP/1.1]
        [CONTENT ID: 2000 SIZE: 52 HEADER: Content-Type: 2 CONTENT: GET https://www.pro-football-reference.com/boxscores/201802040nwe.htm HTTP/1.1]
        <BLANKLINE>
        >>> cache[contentC].value
        CONTENT ID: 2002 SIZE: 11 HEADER: Content-Type: 2 CONTENT: GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1
        >>> cache.hierarchy[2]
        REMAINING SPACE:66
        ITEMS:3
        LIST:
        [CONTENT ID: 2002 SIZE: 11 HEADER: Content-Type: 2 CONTENT: GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1]
        [CONTENT ID: 2001 SIZE: 76 HEADER: Content-Type: 2 CONTENT: GET https://giphy.com/gifs/93lCI4D0murAszeyA6/html5 HTTP/1.1]
        [CONTENT ID: 2000 SIZE: 52 HEADER: Content-Type: 2 CONTENT: GET https://www.pro-football-reference.com/boxscores/201802040nwe.htm HTTP/1.1]
        <BLANKLINE>
        >>> cache[contentA].next.previous.value
        CONTENT ID: 2000 SIZE: 52 HEADER: Content-Type: 2 CONTENT: GET https://www.pro-football-reference.com/boxscores/201802040nwe.htm HTTP/1.1
        >>> cache.hierarchy[2]
        REMAINING SPACE:66
        ITEMS:3
        LIST:
        [CONTENT ID: 2000 SIZE: 52 HEADER: Content-Type: 2 CONTENT: GET https://www.pro-football-reference.com/boxscores/201802040nwe.htm HTTP/1.1]
        [CONTENT ID: 2002 SIZE: 11 HEADER: Content-Type: 2 CONTENT: GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1]
        [CONTENT ID: 2001 SIZE: 76 HEADER: Content-Type: 2 CONTENT: GET https://giphy.com/gifs/93lCI4D0murAszeyA6/html5 HTTP/1.1]
        <BLANKLINE>
        >>> cache[contentC].next.previous.value
        CONTENT ID: 2002 SIZE: 11 HEADER: Content-Type: 2 CONTENT: GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1
        >>> cache.hierarchy[2]
        REMAINING SPACE:66
        ITEMS:3
        LIST:
        [CONTENT ID: 2002 SIZE: 11 HEADER: Content-Type: 2 CONTENT: GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1]
        [CONTENT ID: 2000 SIZE: 52 HEADER: Content-Type: 2 CONTENT: GET https://www.pro-football-reference.com/boxscores/201802040nwe.htm HTTP/1.1]
        [CONTENT ID: 2001 SIZE: 76 HEADER: Content-Type: 2 CONTENT: GET https://giphy.com/gifs/93lCI4D0murAszeyA6/html5 HTTP/1.1]
        <BLANKLINE>
        >>> contentD = ContentItem(2002, 11, "Content-Type: 2", "GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1")
        >>> cache.insert(contentD, 'lru')
        'Content 2002 already in cache, insertion not allowed'
        >>> contentE = ContentItem(2000, 103, "Content-Type: 2", "GET https://www.pro-football-reference.com/boxscores/201801210phi.htm HTTP/1.1")
        >>> cache[2000] = contentE
        >>> cache.hierarchy[2]
        REMAINING SPACE:15
        ITEMS:3
        LIST:
        [CONTENT ID: 2000 SIZE: 103 HEADER: Content-Type: 2 CONTENT: GET https://www.pro-football-reference.com/boxscores/201801210phi.htm HTTP/1.1]
        [CONTENT ID: 2002 SIZE: 11 HEADER: Content-Type: 2 CONTENT: GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1]
        [CONTENT ID: 2001 SIZE: 76 HEADER: Content-Type: 2 CONTENT: GET https://giphy.com/gifs/93lCI4D0murAszeyA6/html5 HTTP/1.1]
        <BLANKLINE>
        >>> cache.hierarchy[2].tail.value
        CONTENT ID: 2001 SIZE: 76 HEADER: Content-Type: 2 CONTENT: GET https://giphy.com/gifs/93lCI4D0murAszeyA6/html5 HTTP/1.1
        >>> cache.hierarchy[2].tail.previous.value
        CONTENT ID: 2002 SIZE: 11 HEADER: Content-Type: 2 CONTENT: GET https://media.giphy.com/media/YN7akkfUNQvT1zEBhO/giphy-downsized.gif HTTP/1.1
        >>> cache.hierarchy[2].tail.previous.previous.value
        CONTENT ID: 2000 SIZE: 103 HEADER: Content-Type: 2 CONTENT: GET https://www.pro-football-reference.com/boxscores/201801210phi.htm HTTP/1.1
        >>> cache.hierarchy[2].tail.previous.previous is cache.hierarchy[2].head
        True
        >>> cache.hierarchy[2].tail.previous.previous.previous is None
        True
    """

    def __init__(self, lst_capacity):
        self.hierarchy = [CacheList(lst_capacity), CacheList(lst_capacity), CacheList(lst_capacity)]
        self.size = 3
    
    def __str__(self):
        return ('L1 CACHE:\n{}\nL2 CACHE:\n{}\nL3 CACHE:\n{}\n'.format(self.hierarchy[0], self.hierarchy[1], self.hierarchy[2]))
    
    __repr__=__str__

    def clear(self):
        for item in self.hierarchy:
            item.clear()
        return 'Cache cleared!'

    def insert(self, content, evictionPolicy):
        # Get the hash value to determine which cache list
        hash_val = hash(content)
        # Call the put method on the appropriate CacheList
        return self.hierarchy[hash_val].put(content, evictionPolicy)

    def __getitem__(self, content):
        # Get the hash value to determine which cache list
        hash_val = hash(content)
        cache_list = self.hierarchy[hash_val]
        
        # Search for the content by cid
        if content.cid in cache_list:
            # Find and return the node
            current = cache_list.head
            while current is not None:
                if current.value.cid == content.cid:
                    return current
                current = current.next
        
        return 'Cache miss!'

    def __setitem__(self, cid, content):
        # Get the hash value to determine which cache list
        hash_val = hash(content)
        # Call the update method on the appropriate CacheList
        self.hierarchy[hash_val].update(cid, content)