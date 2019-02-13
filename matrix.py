class Matrix:
    def __init__(self, mat):
        sizeY = mat[0].__len__()
        for i in range(mat.__len__()):
            if sizeY != mat[i].__len__():
                raise ValueError("Invalid Line {}".format(i))
        self.matrix = mat

    @classmethod
    def gen(self, l, c, fill = 0):
        mat = []
        for i in range(l):
            mat += [[]]
            for j in range(c):
                mat[i] += [fill]
        return Matrix(mat)


    def trace(self):
        trace = 0
        if len(self.matrix) == len(self.matrix[0]):
            for i in range(len(self.matrix)):
                trace += self.matrix[i][i]
            return trace
        else:
            return None

    @classmethod
    def check_size(self, a,b):
        if len(a) != len(b):
            return False

        for i in range(len(a)):
            if len(a[i]) != len(b[i]):
                return False

        return True

    @classmethod
    def check_size_2(self, a, b):
        for i in range(len(a)):
            if len(a[i]) != len(b):
                return False

        return True

    def add(self, b):
        if self.check_size(self.matrix, b.matrix):
            c = []
            for i in range(len(self.matrix)):
                c += [[]]
                for j in range(len(self.matrix[i])):
                    c[i] += [self.matrix[i][j] + b.matrix[i][j]]
            
            return Matrix(c)
        else:
            return None

    def sub(self, b):
        if self.check_size(self.matrix, b.matrix):

            c = []
            for i in range(len(self.matrix)):
                c += [[]]
                for j in range(len(self.matrix[i])):
                    c[i] += [self.matrix[i][j] - b.matrix[i][j]]
            
            return Matrix(c)
        else:
            return None

    @classmethod
    def get_col(self, matrix, index):
        col = []
        for line in matrix.matrix:
            col += [line[index]]
        return col

    @classmethod
    def get_line(self, matrix, index):
        return matrix.matrix[index]

    def mul(self, b):
        if self.check_size_2(self.matrix, b.matrix):
            c = []
            for i in range(len(self.matrix)):
                c += [[]]
                for j in range(len(b.matrix[0])):
                    c[i] += [0]

            for i in range(len(c)):
                for j in range(len(c[i])):
                    c[i][j] = sum([m*n for m,n in zip(self.get_line(self, i), self.get_col(b, j))])

            return Matrix(c)
        else:
            return None

    def show(self):
        print()
        for l in self.matrix:
            print('| ', end = '')
            for c in l:
                print('{:6.2f} '.format( round(float(c), 3)), end = "")
            print('|')
        print()

    def transpose(self):
        c = []
        for i in range(len(self.matrix[0])): 
            c +=  [self.get_col(self, i)]

        return Matrix(c)

    def __call__(self, row = None, col = None):
        if row == None and col == None:
            return self

        elif row == None:
            return Vector(self.get_col(self, col))

        elif col == None:
            return Vector(self.get_line(self, row), transpose = True)
        else:
            return self.matrix[row][col]

    def size(self):
        return self.matrix.__len__(), self.matrix[0].__len__()


class Vector(Matrix):
    def __init__(self, vect, transpose = False):
        self.transposed = transpose
        super().__init__(self.create_mat(vect, transpose))

    @classmethod
    def create_mat(self, vect, transpose):
        if transpose:
            mat = [vect]
        else:
            mat = []
            for elem in vect:
                mat += [[elem]]
        return mat

    @classmethod
    def gen(self, c, fill = 0, transpose = False):
        vect = []
        for i in range(c):
            vect += [fill]
        return Vector(vect)

    @property
    def vector(self):
        if self.transposed:
            return self.matrix[0]
        else:
            return self.get_col(self, 0)

    @vector.setter
    def vector(self, value):
        self.matrix = self.create_mat(value, self.transposed)

    def add(self, b):
        res = super().add(b)
        if res:
            if len(res.matrix) == 1:
                return res(0)
            else:
                return res(None, 0)
        else:
            return None

    def sub(self, b):
        res = super().sub(b)
        if res:
            if len(res.matrix) == 1:
                return res(0)
            else:
                return res(None, 0)
        else:
            return None

    def __call__(self, elem = None):
        if elem == None:
            return self
        else:
            return self.vector[elem]

    def transpose(self):
        if self.transposed:
            return Vector(self.vector, transpose = False)
        else:
            return Vector(self.vector, transpose = True)
