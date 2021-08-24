def isNaN(string):
    return string != string

def keyCheck(source, keys):
    for k in keys:
        try:
            source[k]
        except KeyError:
            source[k] = None
    return source

