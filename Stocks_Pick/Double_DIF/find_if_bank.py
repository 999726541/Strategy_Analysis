import numpy as np

a = np.array([3,4])
b = np.array([9,5])
print(np.corrcoef(a,b)[0][1])