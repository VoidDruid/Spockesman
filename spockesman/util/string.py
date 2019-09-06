def upper_and_separate(name):
    segments = []
    last_upper = 0
    for index, letter in enumerate(name):
        if letter.isupper() and index != 0:
            segments.append(name[last_upper:index])
            last_upper = index
    segments.append(name[last_upper:])
    return '_'.join([segment.upper() for segment in segments])
