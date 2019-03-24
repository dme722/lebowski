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
    def __init__(self, import_func, name, globals=None, locals=None, fromlist=(), level=0):  # pylint: disable=super-on-old-class
        super(_LazyLoader, self).__init__(name)

        self.name = name
        self.globals = globals
        self.locals = locals
        self.fromlist = fromlist
        self.level = level
        self.import_func = import_func
        self.base_name = name.split('.')[0]

    def _load(self):
        builtins.__import__ = self.import_func
        
        module = self.import_func(self.name, self.globals, self.locals, self.fromlist, self.level)
        base_parts = self.base_name.split('.')
        if len(base_parts) > 1:
            submods = base_parts[1:]
            for submod in submods:
                module = getattr(module, submod)

        builtins.__import__ = _import_decorator(builtins.__import__)

        return module

    def __getattr__(self, item):
        builtins.__import__ = self.import_func
        if item == '__path__':
            return sys.path

        try:
            if importlib.util.find_spec(self.base_name + '.' + item):
                self.base_name+= '.' + item
                return self
        except Exception:
            pass

        builtins.__import__ = _import_decorator(builtins.__import__)

        module = self._load()
        return getattr(module, item)

    def __dir__(self):
        module = self._load()
        return dir(module)

def _import_decorator(original_import):
    @wraps(original_import)
    def decorated(name, globals=None, locals=None, fromlist=(), level=0):
        return _LazyLoader(original_import, name,globals,locals,fromlist,level)

    return decorated

builtins.__import__ = _import_decorator(builtins.__import__)