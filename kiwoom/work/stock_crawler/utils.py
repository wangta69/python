import numpy as np

def isNaN(string):
    return string != string

def keyCheck(source, keys):
    for k in keys:
        try:
            source[k] = source[k] if ~np.isnan(source[k]) else None
        except KeyError as e:
            print('[keyCheck] I got a KeyError - reason "%s"' % str(e))
            source[k] = None
        except ValueError as e:
            print('[keyCheck] I got a ValueError - reason "%s"' % str(e))
        except IndexError as e:
            print('[keyCheck] I got a IndexError  - reason "%s"' % str(e))
        except Exception as e:
            print('source', source, 'keys', keys)
            print('[keyCheck] I got a Exception  - reason "%s"' % str(e))
    return source

