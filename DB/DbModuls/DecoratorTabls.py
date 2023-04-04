def value_insert(fn):
    def wrapper(self, *args, **kwargs):
        if args.__len__() <= 0:
            return []

        _key = str(type([x for x in list(args[0].keys())][0]))

        if "int" in _key:
            _value = []
            for key, val in args[0].items():
                _value.extend(fn(self, val))
            return _value

        elif "str" in _key:
            return fn(self, *args, **kwargs)

    return wrapper


def get_table_dan(fn):
    def wrapper(self, *args, **kwargs):
        p0, p1 = fn(self, *args, **kwargs)
        __z = self._all_rec_table(p0, p1)
        if __z == None:
            return None
        else:
            _count_z = len(__z[0])
            if _count_z == 2:
                return {str(x[0]).strip(): x[1] for x in __z}

            return {str(x[0]).strip(): [x[i] for i in range(1, _count_z)] for x in __z}

    return wrapper


def get_index_int(fn):
    def wrapper(self, *args, **kwargs):
        __z = fn(self, *args, **kwargs)
        if __z is None:
            return -1
        else:
            return __z[0][0]
    return wrapper
