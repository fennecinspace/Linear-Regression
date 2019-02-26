class Matrix:
    def __init__(self, mat):
        l_size = len(mat[0])
        for line in mat:
            if l_size != len(line):
                raise ValueError('invalid matrix sizes')
        self._raw = mat

    @property
    def raw(self):
        return self._raw

    @property
    def trace(self):
        if self.size[0] == self.size[1]:
            return sum([ self[i][j] for j in range(self.size[0]) for i in range(self.size[1]) ])
        else: print('nb lines != nb columns')

    @property
    def size(self):
        return self._raw.__len__(), self._raw[0].__len__()

    def __str__(self):
        s = "\n"
        for l in self._raw:
            s +='| '
            for c in l:
                s += '{:6.2f} '.format( round(float(c), 3))
            s +=  '|\n'
        return s
    
    def __call__(self, index):
        return self.col(self, index)

    @classmethod
    def col(self, matrix, index, raw = False):
        col = [ line[index] for line in matrix._raw ]
        if raw: return col
        else: return Vector(col)

    def transpose(self):
        return Matrix([ self.col(self, i, True) for i in range(self.size[1]) ])

    def __setitem__(self, key, item):
        if not type(item).__name__ == 'list' or len(item) != self.size[0]:
            print('invalid assignement')
        else:
            self._raw[key] = item

    def __getitem__(self, key):
        return Vector(self._raw[key], transpose = True)

    def __add__(self, other):
        if type(other).__name__ == 'Matrix' or type(other).__name__ == 'Vector':
            if self.size[0] == other.size[0] and self.size[1] == other.size[1]:
                return Matrix([ [ self[i][j] + other[i][j] for j in range(self.size[1])] for i in range(self.size[0])])
        else:
            try: return Matrix([ [ self[i][j] + other for j in range(self.size[1])] for i in range(self.size[0])])
            except: print('cannot add')
        
    def __sub__(self, other):
        if type(other).__name__ == 'Matrix' or type(other).__name__ == 'Vector':
            if self.size[0] == other.size[0] and self.size[1] == other.size[1]:
                return Matrix([ [ self[i][j] - other[i][j] for j in range(self.size[1])] for i in range(self.size[0])])
        else:
            try: return Matrix([ [ self[i][j] - other for j in range(self.size[1])] for i in range(self.size[0])])
            except: print('cannot substract')

    def __mul__(self, other):
        if type(other).__name__ == 'Matrix' or type(other).__name__ == 'Vector':
            if self.size[1] == other.size[0]: # nb c == nb l
                res = []
                for i in range(self.size[0]):
                    res += [[]]
                    for j in range(other.size[1]):
                        res[i] += [sum([m*n for m,n in zip(self._raw[i], self.col(other, j, True))])]
                return Matrix(res)
        else:
            try: return Matrix([ [ self[i][j] * other for j in range(self.size[1])] for i in range(self.size[0])])
            except: print('cannot substract')

    @classmethod
    def gen(self, l, c, fill = 0):
        mat = [[fill for j in range(c)] for i in range(l)]
        return Matrix(mat)


class Vector(Matrix):
    def __init__(self, vect, transpose = False):
        self.transposed = transpose
        super().__init__([vect] if transpose else [ [elem] for elem in vect ] )

    @property
    def raw(self):
        if self.transposed:
            return self._raw[0]
        else:
            return self.col(self, 0, True)

    @property
    def gravity(self):
        return sum(self.raw) / len(self.raw)

    def __setitem__(self, key, item):
        if self.transposed:
            self._raw[0][key] = item
        else:
            self._raw[key][0] = item

    def __getitem__(self, key):
        if self.transposed:
            if type(self._raw[0][key]).__name__ == 'list':
                return Vector(self._raw[0][key])
            else:
                return self._raw[0][key]
        else:
            if type(self._raw[key][0]).__name__ == 'list':
                return Vector(self._raw[key][0])
            else:
                return self._raw[key][0]
    
    @classmethod
    def gen(self, l, fill = 0):
        mat = super().gen(l, 1, fill)
        return mat(0)