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
            if self._dtype and 'group' in self._dtype:
                while '\0' * self.m in self._data:
                    self._data.remove('\0' * self.m)
                data_list = self._data
                print(data_list)
            else:
                data_list = list(self._data.replace('\0', ''))
            for ind in indexes:
                data_list.insert(ind * self.m + self.m - 1, '\0')
            print(data_list)
            self._data = data_list
        grouped_data = list(grouper(self._data, self.m))
        res = ''
        print(grouped_data)
        new_block = [grouped_data[key] for key in self._key]
        res += ''.join(''.join(line) for line in zip(*new_block))
        if self._with_null is False:
            return res.replace('\0', '')
        return res
            
key = '2x4 '
gkey = Vertical.generate_key(4)
# gkey = '1_3_0_2'
print(gkey)
v = Vertical('IlyaVazinoVa22', key + gkey, with_null=False, dtype=('group', 2))
print(repr(v._data))
encrypted = v.encryption()
print(repr(encrypted))
v2 = Vertical(encrypted, key + gkey, with_null=False, dtype=('group', 2))
print(repr(v2.decryption()))
