from parsec import *

class Var:
    def __init__(self, x):
        self.x = x

    def beta(self, x, e):
        return e if self.x == x else self

    def eval(self, env):
        return env[self.x]

    def __str__(self):
        return str(self.x)

    def __repr__(self):
        return 'Var(%r)' % (self.x)

class Lambda:
    def __init__(self, x, e):
        self.x = x
        self.e = e

    def beta(self, x, e):
        return self if self.x == x else Lambda(self.x, self.e.reduce(x, e))

    def eval(self, env):
        return self

    def __str__(self):
        return '\\%s . %s' % (self.x, self.e)

    def __repr__(self):
        return 'Lambda(%r, %r)' % (self.x, self.e)

class Apply:
    def __init__(self, e1, e2):
        self.e1 = e1
        self.e2 = e2

    def beta(self, x, e):
        return Apply(self.e1.beta(x, e), self.e2.beta(x, e))

    def eval(self, env):
        f = self.e1.eval(env)
        x = self.e2.eval(env)
        return f.e.beta(f.x, x).eval(env)

    def __str__(self):
        return '(%s %s)' % (self.e1, self.e2)

    def __repr__(self):
        return 'Apply(%r, %r)' % (self.e1, self.e2)

symbol = oneof("`~!@#$%^&*-_+|;:',/?[]<>")

identifier = +(letter | digit | symbol)

def curry(xs, e):
    if not xs:
        return e
    (x, *xs) = xs
    return Lambda(x, curry(xs, e))

@Parser
def parse_term(s):
    return (parse_var | parse_lambda | parse_apply)(s)
parse_var = Var >= identifier
parse_apply = Apply * ((char('(') >> parse_term << spaces) ^ (parse_term << char(')')))
parse_lambda = curry * ((char('\\') >> +(identifier << spaces) << char('.') << spaces) ^ parse_term)

def repl(prompt='> '):
    while True:
        try:
            term = input(prompt)
        except EOFError:
            break
        if not term:
            break

        (p, s) = parse_term(term)
        if p is None:
            print('Failed to parse')
            continue

        try:
            print(p.eval({}))
        except Exception as e:
            print(repr(e))

if __name__ == '__main__':
    repl()