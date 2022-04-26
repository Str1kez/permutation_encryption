from base import Base, grouper


class Vertical(Base):
    def __init__(self, data: str, key: str, **kwargs) -> None:
        super().__init__(data, key, kwargs.get('with_null'), kwargs.get('dtype'))
        self._key = self._key.split()
        self.m, self.k = map(int, self._key[0].split('x'))
        self._key = list(map(int, self._key[1].split('_')))
        if self.k != len(self._key) or self.k * self.m < len(self._data) \
                                    or self.k * self.m - len(self._data) >= self.k:
            raise ValueError('Wrong size of matrix')
        self._check_last_block(self.k)
    
    def encryption(self) -> str:
        grouped_data = grouper(self._data, self.k)
        # print(*grouped_data)
        res = ''
        columns = list(zip(*grouped_data))
        # print(columns)
        res += ''.join([''.join(y) for _, y in sorted(zip(self._key, columns))])
        # print(repr(res))
        if self._with_null is False:
            return res.replace('\0', '')
        return res
    
    def decryption(self) -> str:
        if self._with_null is False and any('\0' in x for x in self._data):
            indexes = self._key[::-1][:self._null_amount]
            indexes.sort()
            self._data = [x for x in self._data if '\0' not in x]
            for ind in indexes:
                self._data.insert(ind * self.m + self.m - 1, '\0')
            # print(self._data)
        grouped_data = list(grouper(self._data, self.m))
        res = ''
        # print(grouped_data)
        new_block = [grouped_data[key] for key in self._key]
        res += ''.join(''.join(line) for line in zip(*new_block))
        return res.rstrip('\0')
            
            
if __name__ == '__main__':    
    key = '2x7 '
    gkey = Vertical.generate_key(7)
    # gkey = '1_3_0_2'
    print(gkey)
    v = Vertical('IlyaVazinoVa2200', key + gkey, with_null=False, dtype=('group', 2))
    print(repr(v._data))
    encrypted = v.encryption()
    print(repr(encrypted))
    v2 = Vertical(encrypted, key + gkey, with_null=False, dtype=('group', 2))
    print(repr(v2.decryption()))
