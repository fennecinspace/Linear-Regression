from matrix import Vector, Matrix
import random
import matplotlib.pyplot as plt


class Model:
    def __init__(self, x, y,  cost = 1):
        self.x = Matrix([[1, *sample] for sample in x.matrix])
        self.y = y
        self.m = self.x.size()[0]
        self.n = self.x.size()[1]
        self.weights = Vector.gen(self.n, fill = 0)
        self.learning_rate = 0.2
        self.stop_cost = cost

    @classmethod
    def calc_gravity(self, vect):
        return sum(vect.vector) / vect.size()[0]

    @classmethod
    def normalize(self, data):
        if type(data).__name__ == 'Matrix':
            data_norm = []
            for c in range(data.size()[1]):
                # data_gravity = self.calc_gravity(data(None,c))
                min_ = min(data(None,c).vector)
                max_ = max(data(None,c).vector)
                data_norm += [ [ (data(l,c) - min_) / (max_ - min_) for l in range(data.size()[0]) ] ]
            return Matrix(data_norm).transpose()
        
        elif type(data).__name__ == 'Vector':
            # data_gravity = self.calc_gravity(data)
            min_ = min(data.vector)
            max_ = max(data.vector)
            return Vector([ (data(l) - min_) / (max_ - min_) for l in range(data.size()[0]) ])

    def accuracy(self):
        predicted_values = [self.predict(self.x(i)) for i in range(self.m)]
        predictions = [ 1 if predicted_values[i] == self.y(i) else 0 for i in range(self.m)]
        return len([p for p in predictions if p == 1]) / len(predictions)

    def gradient(self):
        t = []
        for i in range(self.weights.size()[0]):
            t += [self.weights(i) - (self.learning_rate * 1 / self.m * self.gradient_error(i))]
        self.weights = Vector(t)
        
    def gradient_error(self, theta_i):
        error = 0
        for i in range(self.m):
            error += ( self.predict(self.x(i)) - self.y(i) ) * self.x(i, theta_i)
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
        if sample.size()[0] == sample.size()[0]:
            prediction = sample.mul(self.weights)(0,0)
            return prediction
        else:
            print('Invalid Sample')

    def learn(self, iters = 10000, s_cost = 0.1, d_cost = 0.01):
        cost = []
        for i in range(iters + 1):
            self.gradient()
            cost += [self.error()]
            print("\rIteration : {}, Cost: {}".format(i, cost[len(cost) - 1]), end = "")
            if cost[len(cost) - 1] < s_cost:
                break
            if len(cost) > 50 and (cost[len(cost) - 50] - cost[len(cost) - 1]) < d_cost:
                break
        print('\n')
        self.predictions = Vector([self.predict(self.x(i)) for i in range(self.m)])
        self.cost = Vector(cost)

    def plot_cost(self, fig = 1):
        plt.figure(fig)
        plt.plot([i for i in range(self.cost.size()[0])], self.cost.vector)
        plt.ylabel("Cost")
        plt.xlabel('Iteration')

    def plot_2d_dataset(self, fig = 1):
        plt.figure(fig)
        plt.plot(self.x(None,1).vector, self.y.vector, 'r+')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.plot(self.x(None,1).vector, self.predictions.vector, 'b--')


