from re import S
from simple import Simple
from vertical import Vertical
from rail_fence import RailFence


if __name__ == '__main__':
    # Множественный алгоритм
    simple_key = Simple.generate_key(7)
    vertical_key = '3x7 ' + Vertical.generate_key(7)
    rf_key = '3x7'
    s = Simple('ilya vazinov the bestilya vazinov the best', simple_key, with_null=False, dtype=('group', 2))
    crypt = s.encryption()
    v = Vertical(crypt, vertical_key, with_null=False, dtype=('group', 2))
    crypt = v.encryption()
    rf = RailFence(crypt, rf_key, with_null=False, dtype=('group', 2))
    crypt = rf.encryption()
    print(repr(crypt))
    rf = RailFence(crypt, rf_key, with_null=False, dtype=('group', 2))
    crypt = rf.decryption()
    v = Vertical(crypt, vertical_key, with_null=False, dtype=('group', 2))
    crypt = v.decryption()
    s = Simple(crypt, simple_key, with_null=False, dtype=('group', 2))
    crypt = s.decryption()
    print(repr(crypt))
