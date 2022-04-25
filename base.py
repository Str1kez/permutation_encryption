from itertools import zip_longest


class Base:
    def __init__(self, data, key, with_null, dtype=None) -> None:
        self._dtype = dtype
        self._data = data
        self._key = key
        self._with_null = with_null
        self._check_dtype()
        
    def _check_dtype(self) -> None:
        if self._dtype:
            if isinstance(self._dtype, tuple):
                if self._dtype[0] == 'group':
                    self._data = list(''.join(x) for x in grouper(self._data, self._dtype[1], incomplete='strict'))
                else:
                    raise ValueError('Your data type is not group')
            elif (self._dtype == 'byte' or self._dtype == 'bit') and not isinstance(self._dtype, bytearray):
                raise TypeError(f'It is not {self._dtype}')


def grouper(iterable, n, *, incomplete='fill', fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, fillvalue='x') --> ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') --> ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') --> ABC DEF
    args = [iter(iterable)] * n
    if incomplete == 'fill':
        return zip_longest(*args, fillvalue=fillvalue)
    if incomplete == 'strict':
        return zip(*args, strict=True)
    if incomplete == 'ignore':
        return zip(*args)
    else:
        raise ValueError('Expected fill, strict, or ignore')
