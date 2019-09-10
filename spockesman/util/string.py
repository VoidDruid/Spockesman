def upper_and_separate(string):
    """
    Transform ThisNotation to THIS_NOTATION
    :param string: any string
    :return: transformed string from ThisNotation to THIS_NOTATION
    """
    segments = []
    last_upper = 0
    for index, letter in enumerate(string):
        if letter.isupper() and index != 0:
            segments.append(string[last_upper:index])
            last_upper = index
    segments.append(string[last_upper:])
    return '_'.join([segment.upper() for segment in segments])
