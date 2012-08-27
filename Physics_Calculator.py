# -*- coding: utf-8 -*-
import numpy  as np
import sympy  as sp
import pygame as pg
def solveSymbolic(L, coordinates):
	"""
	L is a sympy expression for the Lagrangian.
	conjugateVariables is a list of tuples, like so:
	[(x,xdot),(y,ydot)]
	"""
	#First, we need functions of time that correspond to each position
	#	variable. This is clunky, but should work...
	t=sp.Symbol('t')
	eulerLagrange=[]
	coordinates_t=[]
	for (i,(q,qdot)) in enumerate(coordinates):
		q_t=sp.Function('q%i'%i)
		dL_dq=sp.diff(L,q).subs({q:q_t(t),qdot:sp.diff(q_t(t),t)})
		dL_dqdot=sp.diff(L,qdot).subs({q:q_t(t),qdot:sp.diff(q_t(t),t)})
		ddL_dqdot_dt=sp.diff(dL_dqdot,t)
		eulerLagrange.append((ddL_dqdot_dt-dL_dq))
		coordinates_t.append(q_t)
	return (eulerLagrange,coordinates_t,t)
	