from numpy import dot
from numpy.linalg import norm
X = [0.1,0.2]
Y = [0.2,0.2]
A = 0.3
for i in range(1,3000):
    X.append(A)
    Y.append(A)
cos_sim = dot(X,Y) / (norm(X)*norm(Y))
print(cos_sim)
