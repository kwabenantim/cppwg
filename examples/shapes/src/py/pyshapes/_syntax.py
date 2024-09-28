from collections.abc import Iterable


class ClassDict:

    def __init__(self, template_dict):
        self._dict = {}
        for arg_tuple, clas in template_dict.items():
            if not isinstance(arg_tuple, Iterable):
                arg_tuple = (arg_tuple,)
            key = tuple(str(arg) for arg in arg_tuple)
            self._dict[key] = clas

    def __getitem__(self, arg_tuple):
        if not isinstance(arg_tuple, Iterable):
            arg_tuple = (arg_tuple,)
        key = tuple(str(arg) for arg in arg_tuple)
        return self._dict[key]
