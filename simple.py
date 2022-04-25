from random import shuffle

from base import Base, grouper


class Simple(Base):
    @staticmethod
    def generate_key(size: int):
        elements = list(range(size))
        shuffle(elements)
        return "_".join(map(str, elements))
    
    def __init__(self, data: str, key: str, **kwargs) -> None:
        super().__init__(data, key, kwargs.get('with_null'))
        self._key = self._key.split('_')
    
    def encryption(self) -> str:
        self.check_last_block()
        grouped_data = grouper(self._data, len(self._key))
        result = ''
        for s in grouped_data:
            result += ''.join(y for _, y in sorted((x, y) for x, y in zip(self._key, s)))
        if not self._with_null:
            return result.replace('\0', '')
        return result
    
    def decryption():
        # ! Написать
        pass
        
    def check_last_block(self) -> None:
        if len(self._data) % len(self._key):
            if self._with_null is None:
                exit('wrong settings for last block')
            self._data += '\0' * (len(self._key) - len(self._data) % len(self._key))


key = Simple.generate_key(4)
s = Simple('IlyaVazin', key, with_null=False)
print(s._data)
print(s._key)
print(repr(s.encryption()))
