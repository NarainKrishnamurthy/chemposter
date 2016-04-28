import numpy as np
import random
from numpy.linalg import det

def inverse(N, C):
    n = N
    j = 0
    while (j < N):
        #IF... add a non-zero row to row j
        if (C[j][j] == 0):
            print "adding a zero row"
            k = 0
            #Find the non-zero k
            ##pragma omp parallel for
            for i in xrange(0,N):
                if (C[i][j]!=0):
                    k = i
                    break

            #Add the row k to row j
            for i in xrange(0, 2*N):
                C[j][i] +=  C[k][i]
        ajj = C[j][j]
        
        #Divide out ajj
        ##pragma omp parallel for
        for i in xrange(0, 2*N):
            C[j][i] /= ajj

        #Subtract row j multiplied by appropriate constant from other rows
        for i in xrange(0,N):
            if (i!=j):
                aij = C[i][j]
                for r in xrange(0, 2*N):
                    C[i][r] = C[i][r] - aij*C[j][r]
        j += 1

    A_inv = [[] for i in xrange(0,N)]
    for i in xrange(0,N):
        for j in xrange(0,N):
            A_inv[i].append(C[i][j+N])

    return A_inv

def generate_matrix(N,a,b):
    return [[float(random.randint(a,b)) for i in range(N)] for j in range(N)]

def my_inv_test(A, N, my_inv, err):
    a = np.array(A)
    I = a.dot(np.array(my_inv))

    error = False
    for i in xrange(0,N):
        for j in xrange(0,N):
            if j == i:
                if abs(I[i][j] - 1) > err:
                    print "ERROR for 1 - (i,j):", i, j
                    print I[i][j]
                    error = True
                    
            else:
                if abs(I[i][j] - 0) > err:
                    print "ERROR for 0 - (i,j):", i, j
                    print I[i][j]
                    error = True

    if not error:
        print "INV TEST SUCCEEDED"
    return I

def augment(A,N):
    C = [[] for i in xrange(0, len(A))]
    for i in xrange(0, len(A)):
        for j in xrange(0, len(A)*2):
            if j<len(A):
                C[i].append(A[i][j])
            elif j == len(A) + i:
                C[i].append(1.)
            else:
                C[i].append(0.)
    return C

def test(num_tests, N, a, b):
    for i in xrange(0, num_tests):
        A = generate_matrix(N,a,b)
        if det(np.array(A)) == 0:
            print "0 DETERMINANT"
            continue

        C = augment(A,N)

        my_inv = inverse(len(A), C)
        my_inv_test(A,N,my_inv, 10**-3)


