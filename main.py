from simple import Simple
from vertical import Vertical
from rail_fence import RailFence


if __name__ == '__main__':
    # Множественный алгоритм
    data = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent sit amet vehicula diam. Cras scelerisque ipsum at facilisis tincidunt. Proin non felis mattis lacus porttitor fermentum vitae vitae ligula.'
    simple_key = Simple.generate_key(7)
    vertical_key = '6x7 ' + Vertical.generate_key(7)
    rf_key = '3x7'
    s = Simple(data, simple_key, with_null=False, dtype=('group', 5))
    crypt = s.encryption()
    v = Vertical(crypt, vertical_key, with_null=False, dtype=('group', 5))
    crypt = v.encryption()
    rf = RailFence(crypt, rf_key, with_null=False, dtype=('group', 5))
    crypt = rf.encryption()
    print(repr(crypt))
    rf = RailFence(crypt, rf_key, with_null=False, dtype=('group', 5))
    crypt = rf.decryption()
    v = Vertical(crypt, vertical_key, with_null=False, dtype=('group', 5))
    crypt = v.decryption()
    s = Simple(crypt, simple_key, with_null=False, dtype=('group', 5))
    crypt = s.decryption()
    print(repr(crypt))
    print(crypt == data)
