from base import Base, grouper
from typing import Union

class RailFence(Base):
    def __init__(self, data: str, key: str, **kwargs) -> None:
        super().__init__(data, key, kwargs.get('with_null'), kwargs.get('dtype'))
        self.m, self.n = map(int, key.split('x'))
        if self.m < 2 or self.n < 2:
            raise ValueError('Wrong size of matrix')
        
    def __create_rail(self, block: Union[list, str, bytearray]) -> list:
        i = 0
        mat = [[None] * self.n for _ in range(self.m)]
        down = False
        for j in range(self.n):
            mat[i][j] = block[j]
            if i == 0 or i == self.m - 1:
                down = not down
            i += 1 if down else -1
        return mat
    
    def __create_decrypted_rail(self, block: Union[list, str, bytearray]) -> list:
        matrix = self.__create_rail(block)
        i = 0
        for line in matrix:
            for j in range(self.n):
                if line[j] is not None:
                    line[j] = block[i]
                    i += 1
        return matrix
    
    def __create_non_zero_rail(self, block: Union[list, str, bytearray]) -> list:
        matrix = self.__create_rail(block)
        i = 0
        non_zero = [x for x in block if '\0' not in x]
        for line in matrix:
            for j in range(self.n):
                if line[j] is not None:
                    if j < len(non_zero):
                        line[j] = block[i]
                        i += 1
        return matrix
    
    def __encryption_byte(self):
        blocks = grouper(self._data, self.n, fillvalue='\0')
        res = []
        for block in blocks:
            matrix = self.__create_rail(block)
            res += [x for s in matrix for x in s if x is not None]

    def __encryption_bit(self):
        pass

    def __decryption_bit(self):
        pass
    
    def __decryption_byte(self):
        pass
    
    def encryption(self):
        if self._dtype:
            if self._dtype == 'byte':
                return self.__encryption_byte()
            if self._dtype == 'bit':
                return self.__encryption_bit()
        blocks = grouper(self._data, self.n, fillvalue='\0')
        res = ''
        for block in blocks:
            # print(repr(block))
            matrix = self.__create_rail(block)
            res += ''.join(''.join(x for x in s if x is not None) for s in matrix)
        if self._with_null is False:
            return res.replace('\0', '')
        return res
    
    def decryption(self):
        if self._dtype:
            if self._dtype == 'byte':
                return self.__encryption_byte()
            if self._dtype == 'bit':
                return self.__encryption_bit()
        blocks = grouper(self._data, self.n, fillvalue='\0')
        res = ''
        for block in blocks:
            if self._with_null is False and any('\0' in x for x in block):
                matrix = self.__create_non_zero_rail(block)
            else:
                matrix = self.__create_decrypted_rail(block)
            i = 0
            down = False
            for j in range(self.n):
                res += matrix[i][j]
                if i == 0 or i == self.m - 1:
                    down = not down
                i += 1 if down else -1
        return res.rstrip('\0')
    
    
if __name__ == '__main__':
    with open('input', 'rb') as f:
        data = f.read()
    key = '3x8'
    encrypted = RailFence('Lorem Ipsum dar omet lalal', key, with_null=False, dtype=('group', 13))
    # encrypted = RailFence(data, key, with_null=True, dtype='byte')
    crypt = encrypted.encryption()
    print(repr(crypt))
    # decrypted = RailFence(crypt, key, with_null=True, dtype='byte')
    decrypted = RailFence(crypt, key, with_null=True, dtype=('group', 13))
    print(repr(decrypted.decryption()))
