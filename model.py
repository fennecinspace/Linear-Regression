from matrix import Vector, Matrix
import random
import matplotlib.pyplot as plt

class Data():
    def __init__(self, path, delimiter = ',', header = True):
        with open(path) as f:
            data_str = f.read()
        lines = data_str.strip().splitlines()
        data = [line.split(delimiter) for line in lines]
        if header:
            self.header = data[0]
            self.values = [ [ float(c) for c in l] for l in data[1:] ]
        else:
            self.values = [ [ float(c) for c in l] for l in data ]

    def __getitem__(self, index):
        return self.values[index]

    def __call__(self, start, end = None, cols = False):
        if end:
            if cols: 
                return [[ line[i] for line in self.values ] for i in range(start, end) ]
            else:
                return [ line[start:end] for line in self.values ]
        else: 
            return [ line[start] for line in self.values ]

    @property
    def size(self):
        return (len(self.values), len(self.values[0]) - 1)
            
class Model:
    def __init__(self, x, y,  cost = 1, learning_rate = 0.2):
        self.x = Matrix([[1, *sample] for sample in x.raw])
        self.y = y
        self.m = self.x.size[0]
        self.n = self.x.size[1]
        self.weights = Vector.gen(self.n, fill = 0)
        self.learning_rate = learning_rate
        self.stop_cost = cost

    @classmethod
    def calc_gravity(self, vect):
        return sum(vect.raw) / vect.size[0]

    @classmethod
    def normalize(self, data):
        if type(data).__name__ == 'Matrix':
            data_norm = []
            for c in range(data.size[1]):
                column = data(c)
                min_ = min(column.raw)
                max_ = max(column.raw)
                data_norm += [ [ (data[l][c] - min_) / (max_ - min_) for l in range(data.size[0]) ] ]
            return Matrix(data_norm).transpose()
        
        elif type(data).__name__ == 'Vector':
            min_ = min(data.raw)
            max_ = max(data.raw)
            return Vector([ (data[l] - min_) / (max_ - min_) for l in range(data.size[0]) ])

    def gradient(self):
        t = []
        for i in range(self.weights.size[0]):
            t += [self.weights[i] - (self.learning_rate * 1 / self.m * self.gradient_error(i))]
        self.weights = Vector(t)
        
    def gradient_error(self, theta_i):
        error = 0
        for i in range(self.m):
            error += ( self.predictions[i] - self.y[i] ) * self.x[i][theta_i]
        return error

    def calc_cost(self):
        self.cost = 1  / 2 * self.m * self.error()
        return self.cost

    def error(self, pwr = 2):
        error = 0
        for i in range(self.m):
            error += ( self.predictions[i] - self.y[i] ) ** pwr  
        return error

    def predict(self, sample, poly = False):
        if sample.size[1] == self.weights.size[0]:
            if poly == True:
                prediction = (Vector([ f ** i for i, f in enumerate(sample.raw) ], transpose = True) * self.weights)[0][0]
            else:
                prediction = (sample * self.weights)[0][0]
            return prediction
        else:
            print('Wrong Sample', sample)


    def learn(self, iters = 10000, s_cost = 0.1, d_cost = 0.01, polynomial = False):
        cost = []
        for i in range(iters + 1):
            # calculating iteration predictions
            self.predictions = Vector([self.predict(self.x[i], polynomial) for i in range(self.m)])
            # applying gradient descent
            self.gradient()
            # calculating new cost
            cost += [self.error()]
            print("\rIteration : {}, Cost: {}".format(i, cost[len(cost) - 1]), end = "")
            if cost[len(cost) - 1] < s_cost:
                break
            if len(cost) > 50 and (cost[len(cost) - 50] - cost[len(cost) - 1]) < d_cost:
                break
        print('\n')
        self.predictions = Vector([self.predict(self.x[i], polynomial) for i in range(self.m)])
        self.cost = Vector(cost)

    def r2_score(self):
        cost = self.error()
        var = sum([ (self.y[i] - self.y.gravity) ** 2 for i in range(self.m)])
        return 1 - (cost / var)
        

    def plot_cost(self, fig = 1):
        plt.figure(fig)
        plt.plot([i for i in range(self.cost.size[0])], self.cost.raw)
        plt.ylabel("Cost")
        plt.xlabel('Iteration')

    def plot_2d_dataset(self, fig = 1):
        plt.figure(fig)
        plt.plot(self.x(1).raw, self.y.raw, 'r+')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.plot(self.x(1).raw, self.predictions.raw, 'b--')


