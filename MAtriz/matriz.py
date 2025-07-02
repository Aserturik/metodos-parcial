import numpy as np
A=np.array([[1,-1,3,51],[2,5,7,9],[-3,0,7,5]],dtype=float)
dimA=np.shape(A)
print('La matriz A=\n',A)
print('la dimensión es \n',dimA)
print('la columna 3 de la matriz A=\n', A[:,2])
print('la fila 2 de la matriz A=\n', A[1,:])
B=A
print('La matriz B=\n',B)
B[0][1]=10
print('La matriz B modificada=\n',B)
print('La matriz A sin cambios=\n',A)