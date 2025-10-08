import math
import random
import time
import datetime
from functools import reduce

def ms_print(*args):
    print(*args)

def ms_input(prompt=""):
    try:
        return input(str(prompt))
    except EOFError:
        return ""

def ms_len(x):
    return len(x)

def ms_type(x):
    if isinstance(x, bool):
        return "bool"
    if isinstance(x, int) or isinstance(x, float):
        return "number"
    if isinstance(x, str):
        return "string"
    if isinstance(x, list):
        return "list"
    if isinstance(x, dict):
        return "dict"
    return "object"

def ms_str(x):   return str(x)
def ms_int(x):   return int(x)
def ms_float(x): return float(x)
def ms_bool(x):  return bool(x)

def ms_abs(x):   return abs(x)
def ms_min(*xs): return min(*xs)
def ms_max(*xs): return max(*xs)
def ms_sum(xs):  return sum(xs)

def ms_pow(a, b):   return pow(a, b)
def ms_sqrt(x):     return math.sqrt(x)
def ms_floor(x):    return math.floor(x)
def ms_ceil(x):     return math.ceil(x)
def ms_round(x, n=0): return round(x, n)

def ms_range(a, b=None, step=1):
    if b is None:
        start, stop = 0, a
    else:
        start, stop = a, b
    return list(range(int(start), int(stop), int(step)))

def ms_enumerate(xs):
    return list(enumerate(xs))

def ms_map(fn, xs):
    return [fn(v) for v in xs]

def ms_filter(fn, xs):
    return [v for v in xs if fn(v)]

def ms_reduce(fn, xs, initial=None):
    return reduce(fn, xs, initial) if initial is not None else reduce(fn, xs)

def ms_sorted(xs, reverse=False):
    return sorted(xs, reverse=reverse)

def ms_reversed(xs):
    return list(reversed(xs))

def ms_join(sep, xs):
    return str(sep).join(str(x) for x in xs)

def ms_split(s, sep=None):
    return str(s).split(sep)

def ms_upper(s): return str(s).upper()
def ms_lower(s): return str(s).lower()
def ms_startswith(s, prefix): return str(s).startswith(prefix)
def ms_endswith(s, suffix):   return str(s).endswith(suffix)
def ms_strip(s, chars=None):  return str(s).strip(chars) if chars is not None else str(s).strip()

def ms_time():      return time.time()
def ms_now():       return datetime.datetime.now().isoformat(timespec="seconds")
def ms_sleep(sec):  time.sleep(float(sec)); return None

def ms_random():    return random.random()
def ms_randint(a, b): return random.randint(int(a), int(b))
def ms_choice(xs):  return random.choice(xs)
def ms_shuffle(xs): random.shuffle(xs); return xs

def ms_push(xs, v):
    xs.append(v); return xs

def ms_pop(xs):
    return xs.pop() if xs else None

def ms_extend(xs, ys):
    xs.extend(ys); return xs

def ms_insert(xs, i, v):
    xs.insert(int(i), v); return xs

def ms_remove(xs, v):
    xs.remove(v); return xs

def ms_keys(d):    return list(d.keys())
def ms_values(d):  return list(d.values())
def ms_items(d):   return list(d.items())
def ms_get(d, k, default=None): return d.get(k, default)
def ms_setdefault(d, k, default=None): return d.setdefault(k, default)
def ms_update(d, other): d.update(other); return d
def ms_has(d, k): return k in d

BUILTINS = {
    # I/O
    "print": ms_print,
    "input": ms_input,

    # conversions / introspection
    "len": ms_len,
    "type": ms_type,
    "str": ms_str,
    "int": ms_int,
    "float": ms_float,
    "bool": ms_bool,

    # maths
    "abs": ms_abs,
    "min": ms_min,
    "max": ms_max,
    "sum": ms_sum,
    "pow": ms_pow,
    "sqrt": ms_sqrt,
    "floor": ms_floor,
    "ceil": ms_ceil,
    "round": ms_round,

    # séquences & fonctionnel
    "range": ms_range,
    "enumerate": ms_enumerate,
    "map": ms_map,
    "filter": ms_filter,
    "reduce": ms_reduce,
    "sorted": ms_sorted,
    "reversed": ms_reversed,
    "join": ms_join,
    "split": ms_split,
    "upper": ms_upper,
    "lower": ms_lower,
    "startswith": ms_startswith,
    "endswith": ms_endswith,
    "strip": ms_strip,

    # temps & aléatoire
    "time": ms_time,
    "now": ms_now,
    "sleep": ms_sleep,
    "random": ms_random,
    "randint": ms_randint,
    "choice": ms_choice,
    "shuffle": ms_shuffle,

    # listes
    "push": ms_push,
    "pop": ms_pop,
    "extend": ms_extend,
    "insert": ms_insert,
    "remove": ms_remove,

    # dictionnaires
    "keys": ms_keys,
    "values": ms_values,
    "items": ms_items,
    "get": ms_get,
    "setdefault": ms_setdefault,
    "update": ms_update,
    "has": ms_has,
}
