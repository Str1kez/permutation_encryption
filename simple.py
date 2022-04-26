from base import Base, grouper


class Simple(Base):
    # TODO: Надо проверить на fillvalue (без своей проверки на последнем блоке)
    def __init__(self, data: str, key: str, **kwargs) -> None:
        super().__init__(data, key, kwargs.get('with_null'), kwargs.get('dtype'))
        self._key = list(map(int, self._key.split('_')))
        self._check_last_block(len(self._key))
    
    def encryption(self) -> str:
        grouped_data = grouper(self._data, len(self._key))
        result = ''
        for s in grouped_data:
            result += ''.join(y for _, y in sorted((x, y) for x, y in zip(self._key, s)))
        # print(repr(result))
        if self._with_null is False:
            return result.replace('\0', '')
        return result
    
    def decryption(self) -> str:
        grouped_data = list(grouper(self._data, len(self._key)))
        result = ''
        for s in grouped_data:
            # print(repr(s))
            if s == grouped_data[-1] and self._with_null is False and any('\0' in x for x in s):
                helper = list('\0' * len(s))
                for i, key in enumerate(sorted(self._key[:-self._null_amount])):
                    helper[key] = s[i]
                s = helper
                # helper = list(s[:-self._null_amount])
                # # print(repr(helper))
                # for i in sorted(self._key[-self._null_amount:]):
                #     helper.insert(int(i), s[-1])
                # s = helper
                # print(repr(s))
            result += ''.join([s[x] for x in self._key])
        return result.rstrip('\0')

if __name__ == '__main__':
    
    key = Simple.generate_key(11)
    key = '_'.join(map(str, [6, 3, 7, 0, 10, 9, 8, 2, 1, 5, 4]))
    encryption = Simple('IlyaVazinovV', key, with_null=False, dtype=('group', 6))
    # print(encryption._data)
    print(encryption._key)
    encrypted_data = encryption.encryption()
    print(repr(encrypted_data))
    decryption = Simple(encrypted_data, key, with_null=False, dtype=('group', 6))
    # print(repr(decryption._data))
    print(repr(decryption.decryption()))
