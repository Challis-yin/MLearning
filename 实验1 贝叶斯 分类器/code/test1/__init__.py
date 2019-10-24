import numpy as np
from numpy.linalg import cholesky


import matplotlib.pyplot as plt
sampleNo = 1000;
mu = np.array([[1, 5]])
Sigma = np.array([[1, 0.5], [1.5, 3]])
R = cholesky(Sigma)
s = np.dot(np.random.randn(sampleNo, 2), R) + mu
print(s)
print(np.var(s, axis=0))