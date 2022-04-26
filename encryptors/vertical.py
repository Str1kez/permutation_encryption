from .base import Base, grouper


class Vertical(Base):
    def __init__(self, data: str, key: str, **kwargs) -> None:
        super().__init__(data, key, kwargs.get('with_null'), kwargs.get('dtype'))
        self._key = self._key.split()
        self.m, self.k = map(int, self._key[0].split('x'))
        self._key = list(map(int, self._key[1].split('_')))
        if self.k != len(self._key) or self.k * self.m < len(self._data) \
                                    or self.k * self.m - len(self._data) >= self.k:
            raise ValueError('Wrong size of matrix')
        
    def __encryption_bit(self) -> list:
        pass
    
    def __encryption_byte(self) -> list:
        grouped_data = grouper(self._data, self.k, fillvalue='\0')
        # print(*grouped_data)
        columns = list(zip(*grouped_data))
        # print(columns)
        res = [x for _, y in sorted(zip(self._key, columns)) for x in y]
        # print(repr(res))
        if self._with_null is False:
            return [x for x in res if '\0' not in str(x)]
        return res
    
    def __decryption_bit(self) -> list:
        pass
    
    def __decryption_byte(self) -> list:
        self._check_last_block(self.k)
        if self._with_null is False and any('\0' in str(x) for x in self._data):
            indexes = self._key[::-1][:self._data.count('\0')]
            indexes.sort()
            self._data = [x for x in self._data if '\0' not in str(x)]
            for ind in indexes:
                self._data.insert(ind * self.m + self.m - 1, '\0')
        grouped_data = list(grouper(self._data, self.m))
        new_block = [grouped_data[key] for key in self._key]
        return [x for line in zip(*new_block) for x in line if '\0' not in str(x)]
    
    def encryption(self) -> str:
        if self._dtype:
            if self._dtype == 'byte':
                return self.__encryption_byte()
            if self._dtype == 'bit':
                return self.__encryption_bit()
        
        self._check_last_block(self.k)
        grouped_data = grouper(self._data, self.k)
        # print(*grouped_data)
        columns = list(zip(*grouped_data))
        # print(columns)
        res = ''.join([''.join(y) for _, y in sorted(zip(self._key, columns))])
        # print(repr(res))
        if self._with_null is False:
            return res.replace('\0', '')
        return res
    
    def decryption(self) -> str:
        if self._dtype:
            if self._dtype == 'byte':
                return self.__decryption_byte()
            if self._dtype == 'bit':
                return self.__decryption_bit()
        
        print(self._dtype)
        self._check_last_block(self.k)
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
    
    def __str__(self) -> str:
        return 'Vertical'
            
            
if __name__ == '__main__':
    with open('gd007.png', 'rb') as f:
        data = f.read()
    key = f'{len(data) // 10 + 1}x10 '
    gkey = Vertical.generate_key(10)
    # gkey = '1_3_0_2'
    # print(gkey)
    # v = Vertical('IlyaVazinoVa2200', key + gkey, with_null=False, dtype=('group', 2))
    v = Vertical(data, key + gkey, with_null=True, dtype='byte')
    # print(repr(v._data))
    encrypted = v.encryption()
    # print(repr(encrypted))
    # v2 = Vertical(encrypted, key + gkey, with_null=False, dtype=('group', 2))
    v2 = Vertical(encrypted, key + gkey, with_null=True, dtype='byte')
    decrypt_data = v2.decryption()
    # print(repr(decrypt_data))
    # print(bytes(decrypt_data))
    # print(data)
    print(data == bytes(decrypt_data))
    # with open('output', 'wb') as f:
    #     f.write(bytes(decrypt_data))
    # with open('output.png', 'wb') as f:
    #     f.write(bytes(decrypt_data))
