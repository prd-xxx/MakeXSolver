from fractions import Fraction
class Formula:
    def __init__(self, used_bit, x, left_formula=None, right_formula=None, operand=None):
        self.used_bit = used_bit
        self.x = x
        self.left_formula = left_formula
        self.right_formula = right_formula
        self.operand = operand
    def add(self, right_formula):
        assert (self.used_bit & right_formula.used_bit) == 0
        return Formula(self.used_bit|right_formula.used_bit, self.x + right_formula.x, self, right_formula, '+')
    def sub(self, right_formula):
        assert (self.used_bit & right_formula.used_bit) == 0
        return Formula(self.used_bit|right_formula.used_bit, self.x - right_formula.x, self, right_formula, '-')
    def prod(self, right_formula):
        assert (self.used_bit & right_formula.used_bit) == 0
        return Formula(self.used_bit|right_formula.used_bit, self.x * right_formula.x, self, right_formula, '*')
    def div(self, right_formula):
        assert (self.used_bit & right_formula.used_bit) == 0
        assert right_formula.x != 0
        return Formula(self.used_bit|right_formula.used_bit, self.x / right_formula.x, self, right_formula, '/')
    def __str__(self):
        if self.left_formula is None:
            return str(self.x)
        else:
            return str('({}{}{})'.format(str(self.left_formula), self.operand, str(self.right_formula)))

class MakeXSolver:
    def __init__(self, A, X):
        assert len(A) <= 10, 'too many elements to solve: {}'.format(len(A))
        self.A = A
        self.X = X
        self.N = len(A)
    @staticmethod
    def popcnt(n):
        c = (n & 0x5555555555555555) + ((n >> 1) & 0x5555555555555555)
        c = (c & 0x3333333333333333) + ((c >> 2) & 0x3333333333333333)
        c = (c & 0x0f0f0f0f0f0f0f0f) + ((c >> 4) & 0x0f0f0f0f0f0f0f0f)
        c = (c & 0x00ff00ff00ff00ff) + ((c >> 8) & 0x00ff00ff00ff00ff)
        c = (c & 0x0000ffff0000ffff) + ((c >> 16) & 0x0000ffff0000ffff)
        c = (c & 0x00000000ffffffff) + ((c >> 32) & 0x00000000ffffffff)
        return c
    def solve(self):
        # results[s][x] には、集合sに含まれる要素i番目のA[i]をすべて使ってxを作る作り方を高々1つ格納していく
        results = [{} for _ in range(1<<self.N)]
        for i,a in enumerate(self.A):
            a = Fraction(a)
            results[1<<i][a] = Formula(1<<i, a)
        for s in range(1,1<<self.N):
            if self.popcnt(s) <= 1: continue
            #sの部分集合tを列挙し、u=s\t との組み合わせで作れる結果をすべて results[s]に入れる
            t = s
            while t:
                t = (t-1)&s
                u = s^t
                assert (t&u)==0
                for x,l in results[t].items():
                    for y,r in results[u].items():
                        if x+y not in results[s] and t < u:
                            results[s][x+y] = l.add(r)
                        if x-y not in results[s]:
                            results[s][x-y] = l.sub(r)
                        if x*y not in results[s] and t < u:
                            results[s][x*y] = l.prod(r)
                        if y != 0 and x/y not in results[s]:
                            results[s][x/y] = l.div(r)
        if self.X in results[-1]:
            print('{}={}'.format(results[-1][X], X))
        else:
            print('not found')
    
*A,X = list(map(int,input().split()))
solver = MakeXSolver(A,X)
solver.solve()