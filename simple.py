from random import shuffle

from base import Base, grouper


class Simple(Base):
    @staticmethod
    def generate_key(size: int):
        elements = list(range(size))
        shuffle(elements)
        return "_".join(map(str, elements))
    
    def __init__(self, data: str, key: str, **kwargs) -> None:
        super().__init__(data, key, kwargs.get('with_null'), kwargs.get('dtype'))
        self._key = self._key.split('_')
    
    def encryption(self) -> str:
        self.check_last_block()
        grouped_data = grouper(self._data, len(self._key))
        result = ''
        for s in grouped_data:
            # print(repr(s))
            result += ''.join(y for _, y in sorted((x, y) for x, y in zip(self._key, s)))
        # print(repr(result))
        if not self._with_null:
            return result.replace('\0', '')
        return result
    
    def decryption(self) -> str:
        self.check_last_block()
        grouped_data = list(grouper(self._data, len(self._key)))
        result = ''
        for s in grouped_data:
            print(repr(s))
            if s == grouped_data[-1] and self._with_null is False and any('\0' in x for x in s):
                helper = list('\0' * len(s))
                for i, key in enumerate(sorted(self._key[:-self._null_amount])):
                    helper[int(key)] = s[i]
                s = helper
                # helper = list(s[:-self._null_amount])
                # # print(repr(helper))
                # for i in sorted(self._key[-self._null_amount:]):
                #     helper.insert(int(i), s[-1])
                # s = helper
                print(repr(s))
            result += ''.join([s[int(x)] for x in self._key])
        if not self._with_null:
            return result.replace('\0', '')
        return result
        
    def check_last_block(self) -> None:
        if len(self._data) % len(self._key):
            if self._with_null is None:
                exit('wrong settings for last block')
            self._null_amount = len(self._key) - len(self._data) % len(self._key)
            if self._dtype and 'group' in self._dtype:
                self._data += ['\0' * self._dtype[1] for _ in range(self._null_amount)]
            else:
                self._data += '\0' * (self._null_amount)


key = Simple.generate_key(20)
encryption = Simple('IlyaVazinovV', key, with_null=True)
# print(encryption._data)
print(encryption._key)
encrypted_data = encryption.encryption()
print(repr(encrypted_data))
decryption = Simple(encrypted_data, key, with_null=True)
# print(repr(decryption._data))
print(repr(decryption.decryption()))
