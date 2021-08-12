class CONSTANTS:
    KEY_FIELD = 0
    VALUE_FIELD = 1
    TYPE_FIELD = 2

    DT_DICT = "dict"
    DT_LIST = "list"
    DT_TUPLE = "tuple"

    DT_UNICODE = "unicode"
    DT_BYTES = "bytes"
    DT_FLOAT = "float"
    DT_INT = "int"

    ALL_DATA_TYPES = [DT_DICT, DT_LIST, DT_TUPLE, DT_BYTES, DT_FLOAT, DT_INT]
    CHILD_ALLOWED = [DT_DICT, DT_LIST, DT_TUPLE]
    LIST_TYPES = [DT_LIST, DT_TUPLE]
    NOT_CHILD_ALLOWED = [DT_BYTES, DT_FLOAT, DT_INT]