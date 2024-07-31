import ast
import dis
import json
import os
import random
from abc import ABC, abstractmethod
import importlib
import inspect
import subprocess
import sys

val = 114514

def f(x):
    return f1(x)

def f1(x):
    f2(x)
    if True:
        return f2(x)

def f2(x):
    return { "key": f3(x) }["key"]

def f3(x):
    return f4(f4(f4((x))))

def f4(x):
    a = x
    b = a
    return b

def g(x):
    return g1(g2(x))

def g1(x):
    if random.randint(0, 10) == 0:
        return x
    else:
        return g1(x)

def g2(x):
    if random.randint(0, 10) == 0:
        return x
    else:
        return g3(x)

def g3(x):
    if random.randint(0, 10) == 0:
        return x
    else:
        return g2(x)

def h(x):
    return h1(x)

def h1(x):
    try:
        raise Exception
    except Exception:
        return h2(x)()

def h2(x):
    def wrapped():
        return h3(x).get()
    return wrapped

def h3(x):
    class Class:
        def __init__(self):
            self.x = None
        def set(self, x):
            self.x = h4(x)
        def get(self):
            return h4(self.x)
    obj = Class()
    obj.set(x)
    return obj

def h4(x):
    command = ["python3", "-c", f"print({x})"]
    ret = subprocess.check_output(command).decode("utf-8")
    return json.loads(json.dumps({ "key": ret }))["key"]

def i(x):
    i1 = replaced_i1
    return i1(x)

def i1(x):
    assert False

def replaced_i1(x):
    return i2(x)

class ISomething(ABC):
    @abstractmethod
    def get():
        raise NotImplementedError

def i2(x):
    class OnlyOneInheritFromIt(ISomething):
        def __init__(self, x):
            super().__init__()
            self.x = x
        def get(self):
            return self.x
    obj = OnlyOneInheritFromIt(x)
    assert isinstance(obj, ISomething)
    return i3(obj.get()).get()

def i3(x):
    class Class1:
        def __init__(self, x):
            self.l = [x]
        def get(self):
            return self.l[0]
    class Class2:
        def __init__(self, x):
            self.d = { "key": x }
        def get(self):
            return self.d["key"]
    if random.randint(0, 10) == 0:
        return Class1(x)
    else:
        return Class2(x)

def j(x):
    return j1(x)

def j1(x):
    return j2(eval(str(x)))

def j2(x):
    class Class:
        def __init__(self, x):
            self.x = x
        def __getattr__(self, _):
            return self.__dict__["x"]
    obj = Class(x)
    return obj.y

def k(x):
    return k1(x)

def k1(x):
    name = os.path.basename(os.path.splitext(__file__)[0])
    module = importlib.import_module(name)
    assert x == module.val
    return k2(module.val)

def k2(x):
    assert x == globals()["val"]
    return k3(globals()["val"])

def k3(x):
    source = inspect.getsource(k3)
    unparsed = ast.unparse(ast.parse(source))
    vars = {}
    exec(compile(unparsed, '<string>', 'exec'), globals(), vars)
    k3_1 = vars["k3"]
    codes = [dis.Bytecode(x).dis().strip() for x in [k3, k3_1]]
    assert all(code.endswith("RETURN_VALUE") for code in codes)
    if random.randint(0, 10) == 0:
        return x
    else:
        return k3_1(x)

def hook(frame, event, arg):
    if event == "call" and frame.f_code.co_filename == __file__:
        print('Calling', frame.f_code.co_name,
                'with', ', '.join(frame.f_locals.keys()))
    return hook

if __name__ == "__main__":
    """
    WARNING:
        Please do not write any formal code like this stuff.
        It's just for fun.  ovo
    """
    # sys.settrace(hook)
    for func in [f, g, h, i, j, k]:
        val = func(val)
    print(val)
    sys.settrace(None)