class ClassDict:

    def __init__(self, name, arg_tuples):
        self._dict = {}
        for arg_tuple in arg_tuples:
            self._dict[arg_tuple] = name + "_" + "_".join(arg_tuple)

    def __getitem__(self, key):
        return self._dict[key]
