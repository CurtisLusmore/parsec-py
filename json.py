from collections import OrderedDict

from parsec import *

def const(x):
    def f(*args):
        return x
    return f

join = ''.join

comma = whitespace[:] ^ char(',') ^ whitespace[:]
colon = whitespace[:] ^ char(':') ^ whitespace[:]

@Parser
def value(s):
    return (quoted_string | number | object | array | true | false | null)(s)

true = const(True) >= string('true')
false = const(False) >= string('false')
null = const(None) >= string('null')

character = anybut(['"', '\\', '\r', '\n'])
control_char = join >= (char('\\')[1] + oneof(['"', '\\', '/', 'b', 'f', 'n', 'r', 't'])[1])
quoted_string = join >= (char('"') >> (character | control_char)[:] << char('"'))

unsigned = join >= +digit
integer = join >= (char('-')[:1] + unsigned[1])
fractional = char('.') + unsigned
number = float >= (join >= integer[1] + fractional[:1])

array = char('[') >> value.sepby(comma) << char(']')
pair = quoted_string ^ (colon >> value)
object = OrderedDict >= (char('{') >> whitespace[:] >> pair.sepby(comma) << whitespace[:] << char('}'))