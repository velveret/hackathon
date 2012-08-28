# -*- coding: utf-8 -*-
import numpy  as np
import sympy  as sp
#import pygame as pg
from scipy import integrate
t=sp.Symbol('t')
def calcEL(L, coordinates):
    """
    L is a sympy expression for the Lagrangian.
    coordinates is a list of tuples, like so:
    [(x,xdot),(y,ydot)]
    constraints are expressions that must be 0.
    Output:
    a tuple containing:
        eulerLagrange: the expression the euler lagrange equation yields
        that will be equal to 0.
        coordinates_t: a list of coordinates as functions of t, with the
        same order as the input coordinates list
        t: time variable.
    """
    #First, we need functions of time that correspond to each position
    #    variable. This is clunky, but should work...
    EL=[]
    toTimeDependent={}
    fromTimeDependent={}
    for (i,(q,qdot)) in enumerate(coordinates):
        q_t=sp.Function('q_%i'%i)
        toTimeDependent[sp.symbols(str(qdot)+"dot")]=sp.diff(q_t(t),t,t)
        toTimeDependent[qdot]=sp.diff(q_t(t),t)
        toTimeDependent[q]=q_t(t)
        fromTimeDependent[sp.diff(q_t(t),t,t)]=sp.symbols(str(qdot)+"dot")
        fromTimeDependent[sp.diff(q_t(t),t)]=qdot
        fromTimeDependent[q_t(t)]=q
    #print fromTimeDependent
    for (i,(q,qdot)) in enumerate(coordinates):
        dL_dq=sp.diff(L,q)
        dL_dqdot=sp.diff(L,qdot).subs(toTimeDependent)
        ddL_dqdot_dt=sp.diff(dL_dqdot,t).subs(fromTimeDependent)
        EL.append(ddL_dqdot_dt-dL_dq)
    qdotdot=[sp.symbols(str(qdot)+"dot") for (q,qdot) in coordinates]
    for i in range(len(EL)):
        while not any([qdotdot_i in EL[i].atoms() for qdotdot_i in qdotdot]):
            ELNew=EL[i].subs(toTimeDependent)
            ELNew=sp.diff(ELNew,t).subs(fromTimeDependent)
            #print ELNew
            EL[i]=ELNew
    return EL
def makeOdeFunc(EL,coords):
    """
    coords should be of the same form as input to calcEL
    """
    qdotdot=[sp.symbols(str(qdot)+"dot") for (q,qdot) in coords]
    hasSecondDeriv=[any((qdotdot_i in EL_i for EL_i in EL))
            for qdotdot_i in qdotdot]
    hasFirstDeriv=[any((qdot in EL_i for EL_i in EL))
            for (q,qdot) in coords]
    solveForVars=[]
    for ((q_i,qdot_i),qdotdot_i,fd,sd) in \
            zip(coords,qdotdot,hasFirstDeriv,hasSecondDeriv):
        if sd:
            solveForVars.append(qdotdot_i)
        elif fd:
            solveForVars.append(qdot_i)
        else:
            solveForVars.append(q_i)
    print solveForVars
    ELMatrix=sp.Matrix(EL)
    leadingCoeffs=ELMatrix.jacobian(solveForVars)
    nonLeadingTerms=leadingCoeffs*sp.Matrix(solveForVars)-ELMatrix
    nonLeadingTerms=sp.Matrix([sp.simplify(term) for term in nonLeadingTerms])
    solvedVars=leadingCoeffs.inv()*nonLeadingTerms
    funcList=[]
    inputs=[]
    for (i,((q_i,qdot_i),qdotdot_i)) in enumerate(zip(coords,qdotdot)):
        if qdotdot_i in solveForVars:
            inputs.append(q_i)
            inputs.append(qdot_i)
        elif qdot_i in solveForVars:
            inputs.append(q_i)
    print inputs
    #Dfun=[]
    for (i,((q_i,qdot_i),qdotdot_i)) in enumerate(zip(coords,qdotdot)):
        if qdotdot_i in solveForVars:
            funcList.append((lambda qdot_i: lambda x:x[inputs.index(qdot_i)])(qdot_i))
            #Dfun.append([lambda x:0]*len(inputs))
            #Dfun[-1][inputs.index(qdot_i)]=lambda x:1
            funcList.append((lambda f: lambda x: f(*x))(sp.lambdify(inputs,
                    solvedVars[i])))
            #Dfun.append([(lambda f: lambda x: f(*x))(sp.lambdify(inputs,
            #        sp.diff(solvedVars[i],inp))) for inp in inputs])
        elif qdot_i in solveForVars:
            funcList.append((lambda f: lambda x: f(*x))(sp.lambdify(inputs,
                    solvedVars[i])))
            #Dfun.append([(lambda f: lambda x: f(*x))(sp.lambdify(inputs,
            #        sp.diff(solvedVars[i],inp))) for inp in inputs])
    def odeFunc(coords,t=None):
         """
         Takes a list of coordinates of the form [x,xdot,y,ydot]
         Returns a list of time derivatives for those coordinates
         Note that if a variable only has first derivative terms, it won't
         have the qdot term, and if it's directly determined in terms of other
         variables it won't show up at all.
         """		
         return [f(coords) for f in funcList]
    return odeFunc
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
def numTimeEvolve(L,coordinates,initialConditions,t):
    EL=calcEL(L, coordinates)
    F=makeOdeFunc(EL,coordinates)
    print "Starting time Evolution"
    return integrate.odeint(F,flatten(initialConditions),t)
def flatten(x):
    result = []
    for el in x:
        if hasattr(el, "__iter__") and not isinstance(el, basestring):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result