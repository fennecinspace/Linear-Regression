from model import Model, plt, Data
from matrix import Matrix, Vector

import os 
BASE = os.path.abspath(os.path.dirname(__file__))

## learning rate of 0.4
## normalization
ADDMISSIONS_DATASET = os.path.join(BASE, 'example_datasets', 'Admission_Predict.csv') ## learning rate of 0.4 is good

## learning rate of 0.03 
## no normalization
CRIME_RATE_DATASET = os.path.join(BASE, 'example_datasets', 'Crime_normalized.csv') 

if __name__ == '__main__':
    d = Data(ADDMISSIONS_DATASET)
    x = d(1, 2)
    y = d(d.size[1])

    x = Matrix(x)
    y = Vector(y)
    
    x_norm = Model.normalize(x)
    y_norm = Model.normalize(y)

    model = Model(x_norm, y, learning_rate = 0.4)

    print('INITIAL WEIGHTS : ')
    print(model.weights)

    # learning
    model.learn(iters = 100, d_cost = 0.01)

    print('FITTED WEIGHTS : ')
    print(model.weights)

    print("R2 SCORE :", model.r2_score())

    model.plot_cost(1)
    model.plot_2d_dataset(2)
    plt.show()