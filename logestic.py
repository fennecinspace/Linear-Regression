from matrix import Vector, Matrix


class Model:
    def __init__(self, x, y, normalize = False):
        self.x = Matrix([[1, *sample] for sample in x])
        self.y = Vector(y)
        self.m = self.x.size()[0]
        self.n = self.x.size()[1]
        self.weights = Vector.gen(c = self.m + 1, fill = 1)
        self.cost = 0
        self.rate = 1

        if normalize:
            self._x = self.x
            self._y = self.y
            self.x = self.normalize(self.x)
            self.y = self.normalize(self.y)


    @classmethod
    def calc_gravity(self, vect):
        return sum(vect.vector) / vect.size()[0]

    @classmethod
    def normalize(self, data):
        if type(data).__name__ == 'Matrix':
            data_norm = []
            for c in range(data.size()[1]):
                data_gravity = self.calc_gravity(data(None,c))
                data_norm += [ [ data(l,c) - data_gravity for l in range(data.size()[0]) ] ]
            return Matrix(data_norm).transpose()
        
        elif type(data).__name__ == 'Vector':
            data_gravity = self.calc_gravity(data)
            return Vector([ data(l) - data_gravity for l in range(data.size()[0]) ])
        

    def gradient(self):
        for i in range(self.weights.size()):
            self.weights.vector[i] = self.weights(i) - (self.rate * 1 / self.m * self.gradient_error()) 

    def gradient_error(self):
        error = 0
        for i in range(self.m):
            error += ( self.predict(self.x(i)) - self.y(i) ) * self.x(i)  
        return error

    def calc_cost(self):
        self.cost = 1  / 2 * self.m * self.error()
        return self.cost

    def error(self, pwr = 2):
        error = 0
        for i in range(self.m):
            error += ( self.predict(self.x(i)) - self.y(i) ) ** pwr  
        return error

    def predict(self, sample):
        if sample.size()[0] == sample.size()[0] - 1:
            sample.vector = [1 , *sample.vector]
        if sample.size()[0] == sample.size()[0]:
            return sample.transpose().mul(self.weights)
        else:
            print('Invalid Sample')


    def learn(self, x, y):
        x.show()
        y.show()



if __name__ == '__main__':
    model = Model([[1,2],[3,4],[5,6],[7,9],[3,1],[2,5],[6,1]],[1,4,6,7,1,5,6])
    x_norm = Model.normalize(model.x)
    y_norm = Model.normalize(model.y)
    model.learn(x_norm, y_norm)