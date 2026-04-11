
def translate(translation, msg):
    """
        >>> translate({'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left', '1':'2'} , '1 UP 2 down left right forward')
        '2 down 2 up right left forward'
        >>> translate({'a':'b', 'candy':'three cookies'}, 'We are in a house of CANDY')
        'we are in b house of three cookies'
    """     
    # -- YOUR CODE STARTS HERE
    msg_lower = msg.lower()
    words = msg_lower.split()

    translated_words = []
    for word in words:
        if word in translation:
            translated_words.append(translation[word])
        
        else:
            translated_words.append(word)

    result = ' '.join(translated_words)
    return result


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    print(translate({'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left', '1':'2'} , '1 UP 2 down left right forward'))