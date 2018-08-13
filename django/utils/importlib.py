# Taken from Python 2.7 with permission from/by the original author.
import sys

from django.utils import six

def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in range(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                              "package")
    return "%s.%s" % (package[:dot], name)


if six.PY3:
    from importlib import import_module
else:
    def import_module(name, package=None):
        """Import a module.

        The 'package' argument is required when performing a relative import. It
        specifies the package to use as the anchor point from which to resolve the
        relative import to an absolute import.

        """
        if name.startswith('.'):
            if not package:
                raise TypeError("relative imports require the 'package' argument")
            level = 0
            for character in name:
                if character != '.':
                    break
                level += 1
            name = _resolve_name(name[level:], package, level)
        __import__(name)
        return sys.modules[name]

def import_class_method(module_name, class_name=None, method_name=None, *args, **kwargs):
    """
    Replaces the need to use an 'exec' statement with import statements.
    :param module_name is a string of the module to be imported.
    :param class_name should be a string with the class name defined inside the imported module. If not defined, its value takes from module_name.
    :param method_name should be a string with the static or class method name defined in the loaded class.
    :returns a class or a callable method in that class. None if a method name was defined and not found or if not callable
    """
    module = __import__(module_name, globals(), locals(), fromlist=[module_name])
    res = getattr(module, class_name or module_name)
    if method_name:
        res = res(*args, **kwargs)
        res = getattr(res, method_name, None)
        res = (None, res)[callable(res)]
    return res
