class Parser:
    '''
    '''
    def __init__(self, f):
        ''' Parser(f)
        Create a new parser that wraps the function f. The function should take
        one argument, an iterable of tokens, and return a tuple of the parse
        result and the remaining tokens.
        '''

        self.f = f

    def __call__(self, s):
        ''' self(s)
        Apply the parser to an iterable of tokens.
        '''

        return self.f(s)

    def __pos__(self):
        ''' +self
        Create a new parser which applies the given parser at least once, and
        continues to apply it until it fails.
        '''

        return self[1:]

    def __neg__(self):
        ''' -self
        Unused for now.
        '''

    def __invert__(self):
        ''' ~self
        Unused for now.
        '''

    def __add__(self, other):
        ''' self + other
        Create a new parser which applies the given parsers and adds their
        results together. Fails if either parser fails.
        '''

        @Parser
        def parse(s):
            (l, s2) = self(s)
            if l is None:
                return (None, s)
            (r, s3) = other(s2)
            if r is None:
                return (None, s)
            return (l + r, s3)
        return parse

    def __sub__(self, other):
        ''' self - other
        Unused for now.
        '''

    def __rmul__(self, f):
        ''' self * other
        Create a new parser that applies the left function operand to the list
        of results of the right parser operand.
        '''

        @Parser
        def parse(s):
            (p, s) = self(s)
            return (f(*p), s) if p is not None else (None, s)
        return parse

    def __truediv__(self, other):
        ''' self / other
        Unused for now.
        '''

    def __pow__(self, other):
        ''' self ** other
        Unused for now.
        '''

    def __xor__(self, other):
        ''' self ^ other
        Create a new parser which applies the given parsers and returns a tuple
        of the results. Fails if either parser fails.
        '''

        @Parser
        def parse(s):
            (l, s2) = self(s)
            if l is None:
                return (None, s)
            (r, s3) = other(s2)
            if r is None:
                return (None, s)
            return ((l, r), s3)
        return parse

    def __le__(self, f):
        ''' f >= self
        Create a new parser which applies the left function operand to the
        results of the right parser operand.
        '''

        @Parser
        def parse(s):
            (p, s) = self(s)
            return (f(p), s) if p is not None else (None, s)
        return parse

    def __or__(self, other):
        ''' self | other
        Create a new parser which applies the left parser operand, or the right
        if the left fails.
        '''

        @Parser
        def parse(s):
            (p, s) = self(s)
            return (p, s) if p is not None else other(s)
        return parse

    def __rshift__(self, other):
        ''' self >> other
        Create a new parser which applies and ignores the left parser operand
        and then returns the result of the right parser operand.
        '''

        @Parser
        def parse(s):
            (l, s2) = self(s)
            if l is None:
                return (None, s)
            (r, s3) = other(s2)
            if r is None:
                return (None, s)
            return (r, s3)
        return parse

    def __lshift__(self, other):
        ''' self << other
        Create a new parser which applies the left parser operand and then
        applies and ignores the right parser operand.
        '''

        @Parser
        def parse(s):
            (l, s2) = self(s)
            if l is None:
                return (None, s)
            (r, s3) = other(s2)
            if r is None:
                return (None, s)
            return (l, s3)
        return parse

    def __getitem__(self, ind):
        ''' self[ind]
        Create a new parser which repeatedly applies the given parser.
        '''

        if isinstance(ind, int):
            @Parser
            def parse(s):
                ps = []
                s2 = s
                for _ in range(ind):
                    (p, s2) = self(s2)
                    if p is None:
                        return (None, s)
                    else:
                        ps.append(p)
                else:
                    return (ps, s2)
            return parse

        elif isinstance(ind, slice):
            @Parser
            def parse(s):
                l = ind.start or 0
                h = ind.stop
                i = ind.step or 1
                (ps, s2) = self[l](s)
                if ps is None:
                    return (None, s)
                while h is None or len(ps) + i <= h:
                    (ps2, s3) = self[i](s2)
                    if ps2 is None:
                        break
                    ps += ps2
                    s2 = s3
                return (ps, s2)
            return parse

    def sepby(self, sep, n=0):
        ''' self.sepby(sep)
        Create a new parser which repeatedly applies the current parser,
        separated by application of the given parser.
        '''

        @Parser
        def parse(s):
            (p, s2) = self(s)
            if p is None:
                return ([], s) if n == 0 else (None, s)
            (ps, s3) = (sep >> self)[:](s2)
            ps = [p] + ps
            return (ps, s3) if len(ps) >= n else (None, s)
        return parse

@Parser
def fail(s):
    return (None, s)

@Parser
def any(s):
    if not s: return (None, s)
    (h, *t) = s
    return (h, t)

def char(c):
    @Parser
    def parse(s):
        if not s: return (None, s)
        (h, *t) = s
        return (h, t) if h is c else (None, s)
    return parse

def string(cs):
    l = len(cs)
    @Parser
    def parse(s):
        if len(s) < l:
            return (None, s)
        (h, t) = (s[:l], s[l:])
        return (''.join(h), t) if list(h) == list(cs) else (None, s)
    return parse

def oneof(cs):
    @Parser
    def parse(s):
        if not s: return (None, s)
        (h, *t) = s
        return (h, t) if h in cs else (None, s)
    return parse

def anybut(cs):
    @Parser
    def parse(s):
        if not s: return (None, s)
        (h, *t) = s
        return (h, t) if h not in cs else (None, s)
    return parse

def predicate(p):
    @Parser
    def parse(s):
        if not s: return (None, s)
        (h, *t) = s
        return (h, t) if p(h) else (None, s)
    return parse

spaces = +oneof(' \t')
whitespace = +oneof(' \t\r\n')

letter = predicate(str.isalpha)
digit = predicate(str.isnumeric)
