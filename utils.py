# Misc utils
import sys

def get_size(obj, sofar=None):
    size = sys.getsizeof(obj)
    if sofar is None:
        sofar = set()
    obj_id = id(obj)
    if obj_id in sofar:
        return 0

    sofar.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, sofar) for v in obj.values()])
        size += sum([get_size(k, sofar) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, sofar)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, sofar) for i in obj])

    return size

def sizeWords(b: int) -> str:
    if b < 1024:
        return f'{b}B'
    elif b < 1024 * 1024:
        return f'{(b/1024):.2f}KB'
    elif b < 1024 * 1024 * 1024:
        return f'{(b/(1024 * 1024)):.2f}MB'
    return f'{(b/(1024 * 1024 * 1024)):.2f}GB'