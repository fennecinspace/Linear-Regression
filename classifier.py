from matrix import Vector, Matrix

class Classifier:
    def __init__(self, x, y):
        self.x = Matrix([[1, *sample] for sample in x])
        self.y = Vector(y)
        self.m = self.x.size()[0]
        self.weights = Vector.gen(c = self.m + 1, fill = 1)
        self.cost = 0
        self.rate = 1

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
    c.learn()