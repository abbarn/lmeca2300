# *-* coding: utf-8 *-*

"""
Created on  ven 05 mar 2021 14:40:48 CET 

@author : vekemans

p14.py - Solve non linear BVP u_xx = exp(u), u(-1) = u(1) = 0

"""

from numpy import *
from numpy.linalg import inv,norm

import matplotlib
import matplotlib.pyplot as plt
nfig = 1

N = 16

# D : differentiation matrix
# x : Chebyshev grid
def cheb(N):
	if N==0:
		return 0,1
	x = np.cos(pi * np.linspace(0,1, N+1))
	c = np.concatenate(([2],np.ones(N-1),[2])) * np.power(-1, np.arange(N+1))
	X = x.repeat(N+1).reshape((N+1,N+1))
	dX = X - X.T
	D = (c/c.T) / (dX+np.eye(N+1))
	D = D - np.diag(np.sum(D, axis=1))
	return D,x

D,x = cheb(N)

D2 = D@D
D2 = D2[1:N,1:N]
N2 = len(D2)
u = np.zeros(N2)
err,n = 1,0
while (err > 1e-15) and (n < 100):
	# fixed-point iteration
	unew = np.linalg.inv(D2)@np.exp(u)
	err = np.linalg.norm(unew-u, np.inf)
	u = unew
	n += 1

u = np.append([0],np.append(u,[0]))

fig = plt.figure(nfig)
plt.grid(ls='--', lw=.8, c='lightgrey')
plt.scatter(x,u, s=16)
xx = np.linspace(-1,1, 101)
uu = np.polyval(np.polyfit(x,u,N//2),xx)
plt.plot(xx,uu)
plt.title(r'no.steps = %d, $u_0$ = %.5f' %(n,u[N//2]))

plt.show()
