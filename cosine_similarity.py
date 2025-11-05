import numpy as np
from numpy.linalg import norm

input_data = np.array([[0, 0, 0], [1, 1, 1], [2, 2, 2]])
epsilon = 1e-10

def cosine_sim(input_data, epsilon=1e-10):
    cos_sim = np.zeros((input_data.shape[0], input_data.shape[0]))
    for row in input_data:
        for row2 in input_data:
            cos_data = np.dot(row, row2) / (norm(row) * norm(row2) + epsilon)
            cos_sim[input_data.tolist().index(row)][input_data.tolist().index(row2)] = cos_data
    return cos_sim