class Formula:
    def __init__(self, used_bit, x, left_formula=None, right_formula=None, operator=None):
        self.used_bit = used_bit
        self.x = x
        self.left_formula = left_formula
        self.right_formula = right_formula
        self.operator = operator
        self.has_multi_terms = operator is not None and operator in '+-'
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
        # 余計な括弧はつけないぞという謎のこだわりポイント
        _left = str(self.left_formula)
        left = '({})'.format(_left) if self.left_formula.has_multi_terms and self.operator in '*/' else _left
        _right = str(self.right_formula)
        if self.right_formula.has_multi_terms:
            right = '({})'.format(_right) if self.right_formula.has_multi_terms and self.operator != '+' else _right
        else:
            right = '({})'.format(_right) if self.right_formula.has_multi_terms and self.operator == '/' \
                and self.right_formula.left_formula is not None \
                or self.right_formula.operator == '/' else _right
        return '{}{}{}'.format(left, self.operator, right)

from fractions import Fraction
class MakeXSolver:
    def __init__(self, A, X):
        assert len(A) <= 10, 'too many elements to solve: {}'.format(len(A))
        self.A = A
        self.X = X
        self.N = len(A)
    def solve(self):
        # results[s][x] には、集合sに含まれる要素i番目のA[i]をすべて使ってxを作る作り方を高々1つ格納していく
        results = [{} for _ in range(1<<self.N)]
        for i,a in enumerate(self.A):
            x = Fraction(a)
            results[1<<i][x] = Formula(1<<i, x)
        for s in range(1,1<<self.N):
            if bin(s).count('1') <= 1: continue
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