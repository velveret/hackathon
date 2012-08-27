# -*- coding: utf-8 -*-
import numpy  as np
import sympy  as sp
import pygame as pg
def calcEL(L, coordinates):
	"""
	L is a sympy expression for the Lagrangian.
	coordinates is a list of tuples, like so:
	[(x,xdot),(y,ydot)]
	Output:
	a tuple containing:
		eulerLagrange: the expression the euler lagrange equation yields
		that will be equal to 0.
		coordinates_t: a list of coordinates as functions of t, with the
		same order as the input coordinates list
		t: time variable.
	"""
	#First, we need functions of time that correspond to each position
	#	variable. This is clunky, but should work...
	t=sp.Symbol('t')
	EL=[]
	toTimeDependent={}
	fromTimeDependent={}
	for (i,(q,qdot)) in enumerate(coordinates):
		q_t=sp.Function('q_%i'%i)
		toTimeDependent[qdot]=sp.diff(q_t(t),t)
		toTimeDependent[q]=q_t(t)
		fromTimeDependent[sp.diff(q_t(t),t,t)]=sp.symbols(str(qdot)+"dot")
		fromTimeDependent[sp.diff(q_t(t),t)]=qdot
		fromTimeDependent[q_t(t)]=q
	for (i,(q,qdot)) in enumerate(coordinates):
		dL_dq=sp.diff(L,q)
		dL_dqdot=sp.diff(L,qdot).subs(toTimeDependent)
		ddL_dqdot_dt=sp.diff(dL_dqdot,t).subs(fromTimeDependent)
		EL.append(ddL_dqdot_dt-dL_dq)
	return EL
def makeOdeFunc(EL):
	"""
	Doesn't really work; feel free to disregard...
	"""
	def odeFunc(coords):
		#Takes a list of coordinates of the form [x,xdot,y,ydot]
		#Returns a list of time derivatives for those coordinates
		output=[None]*size(coords)
		output[::2]=coords[1::2]
		
def solveSystem(L,coordinates,initialConditions):
	"""
	This is currently not in use; I'm not sure it ever will be used.	
	
	L is a sympy expression for the Lagrangian.
	coordinates is a list of tuples, like so:
	[(x,xdot),(y,ydot)]
	initialConditions are a list of the above form.
	"""	
	(eulerLagrange,coordinates_t,t)=calcEL(L, coordinates)
	for (i,(EL_i,coordinates_t_i)) in\
			enumerate(zip(eulerLagrange,coordinates_t)):
		eqn=sp.dsolve(EL_i,coordinates_t_i(t))
		freeVars=filter(lambda x:x!=t,eqn.atoms())
		newFreeVars=[sp.Symbol(str(freeVar)+"_%i"%i)
			for freeVar in freeVars]
def numTimeEvolve(L,coordinates,initialConditions):
	return None 