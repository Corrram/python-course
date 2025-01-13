# -*- coding: utf-8 -*-
"""
Created on Sun Dec 1 15 11:46:21 2019

@author: Marten Hillebrand (marten.hillebrand@vwl.uni-freiburg.de) 
"""

import matplotlib.pyplot as plt
from scipy.optimize import fminbound
import numpy as np

show_plots = 'yes'
save_figs = 'no'
# Length of iteration:
T_horizon = 200
T_ahead = 200
T = T_horizon + T_ahead 
iterate = 'yes'    
##############################################################################
# A. Consumer parameters
##############################################################################
N = 1
K_0 = 0.75
# Discount factor: 
beta = 0.9
# Utility exponent: 
sigma = 2
# Period utility function:
def u(c): 
    if sigma == 1:
        u_value = np.log(c)
    else:
        u_value = (c**(1-sigma)-1)/(1-sigma)
    return u_value
# Marginal utility function: 
def d_u(c): 
    return c**(-sigma)

# Check if parameters make economic sense:
assert beta>0 and beta<1
assert sigma > 0
##############################################################################
# B. Production parameters
##############################################################################
# Production parameters:
alpha = 1/3
epsilon = 1/2
theta = 1.0
kappa = 0.95
# Rate of depreciation:
delta = 0.1
rho = (epsilon-1)/epsilon
# Resource sector;
c_x = 0.025
v_in = c_x*1.000065
S_0 = 80
# Rates of efficiency growth:
g_h = 0.01
h_0=1
g_e = 0.05
e_0 =1
beta_hat = beta*(1+g_h)**(1-sigma)

assert beta_hat <1

##############################################################################
# C. Computational parameters and functions
##############################################################################
# Auxilliary function: 
def G(K,L):
    return K**alpha*L**(1-alpha)
    
def F(K,L, X):
   if rho == 0:
       F_value = theta*G(K,L)**kappa*X**(1-kappa)
   else: 
       F_value = theta*(kappa*G(K,L)**rho + (1-kappa)*X**rho)**(1/rho)
    #
   return F_value 

def eta(K,L, X):    
#    return theta**rho*kappa*G(K,L)**rho/(F(K,L,X)**rho)
    return theta**rho*(1-kappa)*X**rho/(F(K,L,X)**rho)

def F_K(K,L,X):
    return alpha*F(K,L,X)/K*(1-eta(K,L,X))

def F_X(K,L,X):
    return F(K,L,X)/X*eta(K,L,X)


# Check if parameters make economic sense:
assert delta >0 and delta <=1
assert kappa >0 and kappa <1
assert alpha > 0 and alpha <1
assert epsilon >0
assert theta > 0


def update_X(K,v_old,e,h, X_in):    
    Z_crit = 0.1**8
    X_min = 0
#    X_max = X_in*2
    X_max = S_0
    conv = 0    
    counter  = 0
    while conv == 0: 
        counter +=1
        if counter== 2500 or K<=0:
            print('WAAAAAAAHHHHH')
            print('Sorry, no solution for X could be computed')
            if K<0:
                print('Reason: Negative capital!')
            break
        X = (X_min + X_max)/2
        #print('Trying X=', X)
        R = F_K(K, h*N, e*X) + 1 -delta
        Z = e*F_X(K, h*N, e*X) - c_x - (v_old-c_x)*R
        #print('Z=', Z)
        if abs(Z) < Z_crit:
            #print('Computation of X successful! :-)')
            conv = 1
        else:
            if Z>0:
                X_min = X
            if Z<0:    
                X_max = X   
    return X

   
X_e_series = np.empty(T)
e_series = np.empty(T)
h_series = np.empty(T)
K_series = np.empty(T)
X_series = np.empty(T)
v_series = np.empty(T)
C_series = np.empty(T)
Y_series = np.empty(T)
S_series = np.empty(T)
R_series = np.empty(T)
g_Y_series = np.empty(T)
g_C_series = np.empty(T)
g_K_series = np.empty(T)
g_X_e_series = np.empty(T)
g_X_series = np.empty(T)
eta_series = np.empty(T)


##############################################################################
# D. Computing equilibrium functions C* and G
##############################################################################


#v_in = c_x*1.0291
C_in_max  = F(K_0, h_0*N,S_0/T) + (1-delta)*K_0
C_in_min = 0#.05*(F(K_0, h_0*N,S_0/9T) + (1-delta)*K_0)
count_crit = 100
# Set initial values

overall_counter = 0
if iterate == 'yes':
    print('Iterating the model- please stand by...')
    for m in range(T_horizon+1):
        if(m==0):
            C_max = C_in_max  
            C_min = C_in_min
        else:
            C = C_series[m-1]
            C_max = C*1.15    
            C_min = C*0.85                    
        finished = 0
        counter = 0    
        max_iter = 5000
        print("Optimizing period m=", m)
        while finished == 0 and counter <=max_iter:      
            #print("Optimizing period m=", m)
            overall_counter +=1
            if overall_counter== 10000:
                print('Sorry, maximium count reached. Exiting')
                break
            counter += 1
            if m==0:
                e = e_0
                h=h_0
                S= S_0
                K = K_0
                # values from t=-1;
                v = v_in
                X = S_0
            else:
                e = (1+g_e)*e_series[m-1]
                h = (1+g_h)*h_series[m-1]
                v = v_series[m-1]
                S = S_series[m]
                K = K_series[m]
                X = X_series[m-1]                      
            C_0 = (C_max + C_min)/2                   
            C = C_0       
            #print('Trying C =', C)
            #print('C_min = ', C_min)
            #print('C_max = ', C_max)        
           # print('Current state:')
           # print('e=', e)
           # print('h=', h)
           # print('v=', v)
           # print('K=', K)
           # print('C=', C)
           # print('S=', S)
            for t in range(m, m+T_ahead):                                
                #print('Period t =', t)
                # Compoute current endogenous variables
                X_old = X
                X = update_X(K, v, e, h, X_old)  
                Y = F(K, h*N, e*X)
                Y_gross = Y + (1-delta)*K - c_x*X
                R = F_K(K, h*N, e*X) + (1 - delta)
                v = c_x + R*(v-c_x)
                C = C*(R*beta)**(1/sigma)    
                # Store variables    
                e_series[t] = e
                X_e_series[t] = e*X
                h_series[t] = h
                K_series[t] = K
                X_series[t] = X
                v_series[t] = v
                C_series[t] = C
                S_series[t] = S                 
                R_series[t] = R
                Y_series[t] = Y
                eta_series[t] = eta(K, h*N, e*X) 
                
                # Update state variables for nex period 
                if C < 0.01*Y_gross:
                    #print('C=', C)
                    C_min = C_0 
                    #print('consumption too low. Seeting C_min= ', C_min)  
                    break
                K = Y + (1-delta)*K-c_x*X-C
                if K<0.01*Y_gross:
                    #print('K=', K)
                    C_max = C_0 
                    #print('consumption too high. Seeting C_max= ', C_max)  
                    break
                if abs(C_max-C_min) < 0.1**10:
                   finished = 1
                S += -X    
                e = (1+g_e)*e
                h = h*(1+g_h)

                if(t==m+T_ahead-1):    
                    finished = 1   
                
check_acc = np.empty(T_horizon)
cons_adj = np.empty(T_horizon)
cons_adj[0] =0
for t in range(1,T_horizon):
    C = C_series[t]
    C_old = C_series[t-1]
    R = R_series[t]
    g_Y_series[t] = (Y_series[t]/Y_series[t-1]-1)*100
    g_K_series[t] = (K_series[t]/K_series[t-1]-1)*100
    g_C_series[t] = (C_series[t]/C_series[t-1]-1)*100
    g_X_e_series[t] = (X_e_series[t]/X_e_series[t-1]-1)*100
    g_X_series[t] = (X_series[t]/X_series[t-1]-1)*100
    cons_adj[t] = abs(C - C_old*(beta*R)**(1/sigma))     
    K = K_series[t]
    X = X_series[t]
    h = h_series[t]
    e = e_series[t]
    R = R_series[t]
    v = v_series[t]
    L = h*N
    w = (1-alpha)/alpha*K/L*F_K(K,L,e*X)
    Y = Y_series[t]
    check_acc[t] = abs(Y+(1-delta)*K - R*K- w*L - v*X) 

if show_plots == 'yes':               
    plt.plot(C_series[0:T_horizon], color = 'green', linewidth=1, linestyle="-", label="$C_t$")
    plt.plot(K_series[0:T_horizon], color = 'blue', linewidth=1, linestyle="-", label="$K_t$")
    plt.plot(Y_series[0:T_horizon], color = 'red', linewidth=1, linestyle="-", label="$Y_t$")
    plt.legend(loc='best')
    plt.xlabel("$t$")
    #plt.ylabel("$C^*(k)$")   
    plt.legend(loc='best')
    if save_figs == 'yes':
        plt.savefig('../MySlides/figures/NCG_energy_Y_C_K_scenario_1.eps', format='eps', dpi=1000)
    plt.show()
    
    T_1 = T_horizon
    g_h_line = [g_h*100]*T_horizon
    plt.plot(g_C_series[1:T_1], color = 'green', linewidth=1, linestyle="-", label="$g_{C,t}$")
    plt.plot(g_K_series[1:T_1], color = 'blue', linewidth=1, linestyle="-", label="$g_{K,t}$")
    plt.plot(g_Y_series[1:T_1], color = 'red', linewidth=1, linestyle="-", label="$g_{Y,t}$")
    plt.plot(g_h_line[1:T_1], color = 'black', linewidth=1, linestyle="--", label="$g_{h}$")
    plt.legend(loc='best')
    plt.xlabel("$t$")
    plt.ylabel("Growth rates in percent")
    #plt.ylabel("$C^*(k)$")   
    plt.legend(loc='best')
    if save_figs == 'yes':
        plt.savefig('../MySlides/figures/NCG_energy_g_Y_g_C_g_K_scenario_1.eps', format='eps', dpi=1000)
    plt.show()
    
    zero_line = [0]*T_horizon
    plt.plot(X_series[0:T_horizon], color = 'magenta', linewidth=1, linestyle="-", label="$X_t$")
    plt.plot(zero_line[0:T_horizon], color = 'black', linewidth=1, linestyle="--", label="$0$")
    plt.legend(loc='best')
    plt.xlabel("$t$")
    #plt.ylabel("$C^*(k)$")   
    plt.legend(loc='best')
    if save_figs == 'yes':
        plt.savefig('../MySlides/figures/NCG_energy_X_scenario_1.eps', format='eps', dpi=1000)
    plt.show()
    
    plt.plot(S_series[0:T_horizon], color = 'blue', linewidth=1, linestyle="-", label="$S_t$")
    plt.plot(zero_line[0:T_horizon], color = 'black', linewidth=1, linestyle="--", label="$0$")
    plt.legend(loc='best')
    plt.xlabel("$t$")
    if save_figs == 'yes':
        plt.savefig('../MySlides/figures/NCG_energy_S_scenario_1.eps', format='eps', dpi=1000)
    plt.show() 
    
    zero_line = [0]*T_horizon
    plt.plot(X_e_series[0:T_horizon], color = 'firebrick', linewidth=1, linestyle="-", label="$X_t^e$")
    plt.plot(zero_line[0:T_horizon], color = 'black', linewidth=1, linestyle="--", label="$0$")
    plt.legend(loc='best')
    plt.xlabel("$t$")
    #plt.ylabel("$C^*(k)$")   
    plt.legend(loc='best')
    if save_figs == 'yes':
        plt.savefig('../MySlides/figures/NCG_energy_X_e_scenario_1.eps', format='eps', dpi=1000)
    plt.show()
    
    zero_line = [0]*T_horizon
    plt.plot(v_series[0:T_horizon], color = 'cornflowerblue', linewidth=1, linestyle="-", label="$v_t$")
    plt.plot(zero_line[0:T_horizon], color = 'black', linewidth=1, linestyle="--", label="$0$")
    plt.legend(loc='best')
    plt.xlabel("$t$")
    #plt.ylabel("$C^*(k)$")   
    plt.legend(loc='best')
    if save_figs == 'yes':
        plt.savefig('../MySlides/figures/NCG_energy_v_scenario_1.eps', format='eps', dpi=1000)
    plt.show()


print('Simulation accuracy')
print('Terminal resource stock: S = ', S_series[T_horizon+1])     
print('Maximum adjustment of Euler equations due to shooting-adjustment:', max(cons_adj))  
print('Maximum deviation of final profits from zero (consistency check):', max(check_acc))  

                   