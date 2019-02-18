from matrix import Vector, Matrix

class Classifier:
    def __init__(self, x, y):
        self.x = Matrix([[1, *sample] for sample in x])
        self.y = Vector(y)
        self.m = self.x.size()[0]
        self.n = self.x.size()[1]
        self.weights = Vector.gen(c = self.m + 1, fill = 1)
        self.cost = 0
        self.rate = 1
        self._gravity = None


    @property
    def gravity(self):
        if not self._gravity:
            g = []
            for i in range(self.n):
                g += [sum(self.x(None,i).vector) / self.x(None,i).size()[0]]
            g += [sum(self.y.vector) / self.y.size()[0]]
            self._gravity = Vector(g, transpose =  True)
        
        return self._gravity


    @property
    def x_gravity(self):
        return Vector(self.gravity.vector[0: self.n], transpose = True)


    @property  
    def y_gravity(self):
        return self.gravity(self.n)
    

    def normalize(self, x = True, y = True):
        x_norm = []
        for c in range(self.n):
            x_norm += [ [ self.x(l,c) - self.x_gravity(c) for l in range(self.m) ] ]
        self.x_norm = Matrix(x_norm).transpose()
        self.y_norm = Vector([ self.y(l) - self.y_gravity for l in range(self.m) ])


    def gradient(self):
        for i in range(self.weights.size()):
            self.weights.vector[i] = self.weights(i) - (self.rate * 1 / self.m * self.gradient_error()) 


    def gradient_error(self):
        error = 0
        for i in range(self.m):
            error += ( self.predict(self.x(i)) - self.y(i) ) * self.x(i)  
        return error


    def error(self, pwr = 2):
        error = 0
        for i in range(self.m):
            error += ( self.predict(self.x(i)) - self.y(i) ) ** pwr  
        return error


    def calc_cost(self):
        self.cost = 1  / 2 * self.m * self.error()
        return self.cost


    def predict(self, sample):
        return sample.transpose().mul(self.weights)


    def learn(self):
        self.x.show()
        self.y.show()





if __name__ == '__main__':
    c = Classifier([[1,2],[3,4],[5,6],[7,9],[3,1],[2,5],[6,1]],[1,4,6,7,1,5,6])
    c.normalize()
    c.learn()