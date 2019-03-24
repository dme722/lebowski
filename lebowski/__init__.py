import builtins
from lebowski.lebowski import _import_decorator

def enable():
    builtins.__import__ = _import_decorator(builtins.__import__)

def disable():
    builtins.__import__ = _import_decorator(builtins.__import__)(get_orig=True)