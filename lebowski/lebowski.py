"""A LazyLoader class."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import importlib
import types
import builtins
import sys
import pdb
import copy

from functools import wraps

class _LazyLoader(types.ModuleType):
    """Lazily import a module, mainly to avoid pulling in large dependencies.

    `contrib`, and `ffmpeg` are examples of modules that are large and not always
    needed, and this allows them to only be loaded when they are used.
    """

    # The lint error here is incorrect.
    def use_default_import(self, func):
        @wraps(func)
        def decorated(*args,**kwargs):
            builtins.__import__ = self.import_func
            ret_val = func(*args,**kwargs)
            builtins.__import__ = _import_decorator(builtins.__import__)
            return ret_val
        return decorated

    def __init__(self, import_func, name, globals=None, locals=None, fromlist=(), level=0):  # pylint: disable=super-on-old-class
        self.import_func = import_func
        self.init = self.use_default_import(self.init)
        self._load = self.use_default_import(self._load)
        self.__getattr__ = self.use_default_import(self.__getattr__)
        self.init(import_func, name, globals, locals, fromlist, level)

    def init(self, import_func, name, globals, locals, fromlist, level):
        super(_LazyLoader, self).__init__(name)

        if importlib.util.find_spec(name) is None:
            print("Spec: ")
            print(importlib.util.find_spec(name))
            raise ModuleNotFoundError(f"No module named '{name}'.")

        self.full_name = name
        self.globals = globals
        self.locals = locals
        self.fromlist = fromlist
        self.level = level
        self.base_name = name.split('.')[0]

    def _load(self):
        module = self.import_func(self.full_name, self.globals, self.locals, self.fromlist, self.level)
        base_parts = self.base_name.split('.')
        if len(base_parts) > 1:
            submods = base_parts[1:]
            for submod in submods:
                module = getattr(module, submod)

        return module

    def __getattr__(self, item):
        if item == '__path__':
            return sys.path

        try:
            full_parts = self.full_name.split('.')
            base_parts = self.base_name.split('.')
            if (len(full_parts) > len(base_parts)) and full_parts[len(base_parts)] == str(item):
                new_base = self.base_name + '.' + item
                new_loader = copy.copy(self)
                new_loader.base_name = new_base

                return new_loader
        except Exception:
            pass

        module = self._load()
        return getattr(module, item)

    def __dir__(self):
        module = self._load()
        return dir(module)

def _import_decorator(original_import):
    @wraps(original_import)
    def decorated(name=None, globals=None, locals=None, fromlist=(), level=0, get_orig=False):
        if get_orig:
            return original_import
        return _LazyLoader(original_import, name,globals,locals,fromlist,level)

    return decorated