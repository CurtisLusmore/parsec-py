"""
# ----- fail -----
>>> fail([])
(None, [])

>>> fail(['a', 'b', 'c'])
(None, ['a', 'b', 'c'])

# ----- char -----
>>> char('a')([])
(None, [])

>>> char('a')(['a', 'b', 'c'])
('a', ['b', 'c'])

>>> char('A')(['a', 'b', 'c'])
(None, ['a', 'b', 'c'])

>>> char('b')(['a', 'b', 'c'])
(None, ['a', 'b', 'c'])

# ----- oneof -----
>>> oneof([])([])
(None, [])

>>> oneof(['a'])([])
(None, [])

>>> oneof([])(['a', 'b', 'c'])
(None, ['a', 'b', 'c'])

>>> oneof(['a'])(['a', 'b', 'c'])
('a', ['b', 'c'])

>>> oneof(['A'])(['a', 'b', 'c'])
(None, ['a', 'b', 'c'])

>>> oneof(['A', 'a'])(['a', 'b','c'])
('a', ['b', 'c'])

>>> oneof(['b'])(['a', 'b', 'c'])
(None, ['a', 'b', 'c'])

# ----- a | b -----
>>> (fail | fail)(['a', 'b', 'c'])
(None, ['a', 'b', 'c'])

>>> (fail | char('a'))(['a', 'b', 'c'])
('a', ['b', 'c'])

>>> (char('a') | fail)(['a', 'b', 'c'])
('a', ['b', 'c'])

# ----- a >> b -----
>>> (fail >> fail)(['a', 'b', 'c'])
(None, ['a', 'b', 'c'])

>>> (fail >> char('a'))(['a', 'b', 'c'])
(None, ['a', 'b', 'c'])

>>> (char('a') >> fail)(['a', 'b', 'c'])
(None, ['a', 'b', 'c'])

>>> (char('a') >> char('b'))(['a', 'b', 'c'])
('b', ['c'])

# ----- a << b -----
>>> (fail << fail)(['a', 'b', 'c'])
(None, ['a', 'b', 'c'])

>>> (fail << char('a'))(['a', 'b', 'c'])
(None, ['a', 'b', 'c'])

>>> (char('a') << fail)(['a', 'b', 'c'])
(None, ['a', 'b', 'c'])

>>> (char('a') << char('b'))(['a', 'b', 'c'])
('a', ['c'])

# ----- f >= a -----
>>> ((lambda p: p[0] == 'a') >= fail)(['a', 'b', 'c'])
(None, ['a', 'b', 'c'])

>>> ((lambda p: p[0] == 'a') >= char('a'))(['a', 'b', 'c'])
(True, ['b', 'c'])

# ----- a[int] -----
>>> fail[0](['a', 'b', 'c'])
([], ['a', 'b', 'c'])

>>> char('a')[0](['a', 'b', 'c'])
([], ['a', 'b', 'c'])

>>> char('a')[1](['a', 'b', 'c'])
(['a'], ['b', 'c'])

>>> char('a')[2](['a', 'b', 'c'])
(None, ['a', 'b', 'c'])

>>> char('a')[2](['a', 'a', 'a'])
(['a', 'a'], ['a'])

>>> char('a')[5](['a'])
(None, ['a'])

>>> char('a')[3](['a', 'a', 'a'])
(['a', 'a', 'a'], [])

# ----- a[l:h] -----
>>> char('a')[0:1](['b', 'b', 'c'])
([], ['b', 'b', 'c'])

>>> char('a')[0:1](['a', 'b', 'c'])
(['a'], ['b', 'c'])

>>> char('a')[0:1](['a', 'a', 'b'])
(['a'], ['a', 'b'])

>>> char('a')[2:3](['a', 'b', 'c'])
(None, ['a', 'b', 'c'])

>>> char('a')[2:3](['a', 'a', 'b'])
(['a', 'a'], ['b'])

>>> char('a')[2:5](['a', 'a'])
(['a', 'a'], [])

# ----- a[:h] -----
>>> char('a')[:1](['b', 'b', 'c'])
([], ['b', 'b', 'c'])

>>> char('a')[:1](['a', 'b', 'c'])
(['a'], ['b', 'c'])

>>> char('a')[:1](['a', 'a', 'b'])
(['a'], ['a', 'b'])

# ----- [l:] -----
>>> char('a')[1:](['b', 'b', 'c'])
(None, ['b', 'b', 'c'])

>>> char('a')[1:](['a', 'b', 'c'])
(['a'], ['b', 'c'])

>>> char('a')[1:](['a', 'a', 'a', 'a', 'a', 'a', 'b'])
(['a', 'a', 'a', 'a', 'a', 'a'], ['b'])

>>> char('a')[1:](['a', 'a', 'a'])
(['a', 'a', 'a'], [])

# ----- a[l:h:i] -----
>>> char('a')[1:10:2](['a', 'a', 'b'])
(['a'], ['a', 'b'])

>>> char('a')[1:10:2](['a', 'a', 'a'])
(['a', 'a', 'a'], [])

>>> char('a')[1:10:2](['a', 'a', 'a', 'a'])
(['a', 'a', 'a'], ['a'])

>>> char('a')[1:2:3](['a', 'a', 'a', 'a'])
(['a'], ['a', 'a', 'a'])

# ----- a+ -----
>>> (+char('a'))(['b', 'b', 'c'])
(None, ['b', 'b', 'c'])

>>> (+char('a'))(['a', 'b', 'c'])
(['a'], ['b', 'c'])

>>> (+char('a'))(['a', 'a', 'b'])
(['a', 'a'], ['b'])

# ----- a + b -----
>>> (char('a') + char('b'))(['b', 'b', 'c'])
(None, ['b', 'b', 'c'])

>>> (char('a') + char('b'))(['a', 'a', 'c'])
(None, ['a', 'a', 'c'])

>>> (char('a') + char('b'))(['a', 'b', 'c'])
('ab', ['c'])

# ----- a ^ b -----
>>> (char('a') ^ char('b'))(['b', 'b', 'c'])
(None, ['b', 'b', 'c'])

>>> (char('a') ^ char('b'))(['a', 'a', 'c'])
(None, ['a', 'a', 'c'])

>>> (char('a') ^ char('b'))(['a', 'b', 'c'])
(('a', 'b'), ['c'])

# ----- f * a -----
>>> ((lambda x: x) * fail)(['a', 'b', 'c'])
(None, ['a', 'b', 'c'])

>>> ((lambda x, y: x) * (char('a') ^ char('b')))(['a', 'b', 'c'])
('a', ['c'])
"""

from doctest import testmod
from parsec import *

testmod(verbose=True)