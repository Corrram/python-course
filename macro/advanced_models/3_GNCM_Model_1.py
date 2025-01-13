#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 09:13:21 2021

@author: marten.hillebrand@vwl.uni-freiburg.de
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numba import jit


diagnostic_check = 'yes'
# Do you want to see the figures?
show_plots = 'yes'
# Do you want to save the figures?
save_figs = 'no'
# error_tolerance:
err_tol = 0.1**15


##############################################################################
#  0. Calibration targets 
##############################################################################
# Output target 2006-2015
Y_target = 0.99297
# Global emissions 2006-2015 in Gt C:
X_target =  92.673
# Atmospheric stock of carbon at the begining of 2006/end of 2005  in Gt C:
S_target_2005 = 807
# Atmospheric stock of carbon at the begining of 2016/end of 2015 in Gt C:
S_target_2015 = 851

##############################################################################
#  1. Simulaton parameters
##############################################################################
##############################################################################
#  1.A. Numerical parameters
##############################################################################
# Length of iteration:
T_horizon = 30
# Periods ahead (shooting):
T_ahead = 30
# Total iteration:
T = T_horizon + T_ahead 
    
##############################################################################
#  1.B. Model parameters
##############################################################################
# Final sector production
kappa = 0.95
alpha = 0.3/0.95
epsilon  = 0.75
rho = (epsilon-1)/epsilon
# Efficiency growth of labor and energy 
g_h = 0.1
g_e = 0.1
# Resource sector
# Extraction costs trillion dollar/ GtC:
c_x = 0.000043/0.5441
# Climate Parameters
phi = 0.0228
phi_L = 0.2
phi_0 = 0.393
phi_X = phi_L + (1-phi_L)*phi_0
S_bar = 581
gamma = 0.000053
# Consumer parameters
beta = 0.985**10
sigma = 1.0
# Check validity
msg = 'Invalid economic parameter!'
assert 0<beta < 1, msg
assert 0<alpha<1, msg
assert 0<kappa<1, msg
assert epsilon >0, msg

##############################################################################
#  1.C. Climate policies
##############################################################################
# Climate policy parameters
g = g_h
beta_hat = beta*(1+g)**(1-sigma)
tau_bar_eff = gamma*((phi_L/(1-beta_hat) + (1-phi_L)*phi_0/(1-beta_hat*(1-phi))))
Policies = [0,tau_bar_eff]
P = len(Policies)

##############################################################################
#  1.D. Initial conditions
##############################################################################
# World capital stock (balanced level, about 20% of ouput):
K_0 = 0.2
# Initial resource stock of fossil fuels in GtC (approximately infinite):
R_0 = 10*10 
v_in = c_x
assert v_in >= c_x, msg

##############################################################################
#  1.E Population and labor 
##############################################################################
# Empirical population sizes for 2005-2105: 
N_s_series = np.empty(T)
df_pop = pd.read_csv('World_population_2006_2105_decades.csv')
d = 1/10**9
# Population constant after 2100:
for t in range (T):
    if t < len(df_pop):
        N_s_series[t] = df_pop.iloc[t,1]*d        
    else:
        N_s_series[t] = df_pop.iloc[ len(df_pop)-1,1]*d

##############################################################################
#  1.F. Computational parameters 
##############################################################################
# Series to store equilibrium values in: 
Y_series = np.empty((T,P))
K_series = np.empty((T,P))
X_series = np.empty((T,P))
h_series = np.empty((T,P))
e_series = np.empty((T,P))
tau_series = np.empty((T,P))
S_all_series = np.empty((T,P))
S_1_series = np.empty((T,P))
S_2_series = np.empty((T,P))
R_series = np.empty((T,P))
r_series = np.empty((T,P))
w_series = np.empty((T,P))
C_series = np.empty((T,P))
v_series = np.empty((T,P))
X_series = np.empty((T,P))
Temp_series = np.empty((T,P))
Temp_rel_series = np.empty((T,P))
tau_in_dollar_per_ton_of_CO2_series= np.empty((T,P))

##############################################################################
#   1.G. Functions
##############################################################################
# Capital-labor aggregate: 
@jit
def G(K,L):
    return K**alpha*L**(1-alpha)
# Final production: 
@jit
def F(K,L,X_e):
    if epsilon ==1:
        return G(K,L)**kappa*(X_e)**(1-kappa)
    else:
        return (kappa*G(K,L)**rho + (1-kappa)*(X_e)**rho)**(1/rho) 
# Function determining the capital cost share in final production: 
@jit
def eta_x(K,L,X_e):
    return ((1-kappa)*X_e**rho)/(kappa*G(K,L)**rho + (1-kappa)*X_e**rho)  
#Function which updates the previous climate depending on emissions X:
@jit
def update_climate_state(S_1_old, S_2_old, X):
     S_1_new = S_1_old + phi_L*X
     S_2_new = (1-phi)*S_2_old + (1-phi_L)*phi_0*X
     return [S_1_new, S_2_new]
# Damage function: 
@jit
def D(S):
    return 1-np.exp(-gamma*(S-S_bar))

#Function to compute equilibrium emissions (using a bisection method)
def compute_X(K, N, v_old, S_1_old, S_2_old, h, e):
    Phi = lambda X: eta_x(K,N*h, e*X)*F(K,N*h, e*X)/X - \
        alpha*(1-eta_x(K,N*h, e*X))*F(K,N*h, e*X)*(v_old-c_x) \
            - c_x/(1-D(S_1_old + S_2_old*(1-phi) + phi_X*X))     \
            -tau_bar*F(K,N*h, e*X)               
    # Find a number X_max at which Phi(X_max)<0:
    X_max = .1
    phi_max = 1          
    while phi_max >0:
        X_max = X_max*2
        phi_max = Phi(X_max)
    # Minimum values at which Phi(X_max)>0:    
    X_min = X_max/2    
    phi_val = 1
    counter = 0     
    # Determine X by bisecting the interval [X_min, X_max]:
    while abs(phi_val) > err_tol and counter < 10**5:
        X = (X_max+X_min)/2  
        phi_val = Phi(X)
        if phi_val >0:
            X_min = X
        if phi_val <0:
            X_max = X
        counter +=1
    return X

#Function to compute equilibrium variables (Y, X, r, v) given exogenous 
# and pre-determined variables:: 
def compute_equilibrium(K_s, N_s, v_old, S_1_old, S_2_old, h, e):
    X = compute_X(K_s, N_s, v_old, S_1_old, S_2_old, h, e)   
    S = sum(update_climate_state(S_1_old, S_2_old, X))
    Y = (1-D(S))*F(K_s, h*N_s, e*X)
    eta = eta_x(K_s, h*N_s, e*X)
    r = alpha*(1-eta)*Y/K_s
    v = c_x+r*(v_old-c_x)
    return [Y, X, r, v]


##############################################################################
#  2. Initialization  
##############################################################################
# Initial climate state:
S_2_in = (S_target_2005 - S_target_2015 + X_target*(phi_L + phi_0*(1-phi_L)))/phi 
S_1_in = S_target_2005-S_2_in
S_0 = sum(update_climate_state(S_1_in, S_2_in, X_target))
# Initial labor and energy efficiency:
tau_bar = Policies[0]
N_0 = N_s_series[0]
D_0_bar = D(S_1_in + (1-phi)*S_2_in + phi_X*X_target)
eta_bar = v_in*X_target/Y_target
e_0 = Y_target/(1-D_0_bar)/X_target*(eta_bar/(1-kappa))**(1/rho)
val = ((Y_target/(1-D_0_bar))**rho - (1-kappa)*(e_0*X_target)**rho)/kappa
h_0 = (val**(1/rho)/(K_0**alpha*N_0**(1-alpha)))**(1/(1-alpha))  

##############################################################################
#  3. Iteration 
##############################################################################
for p in range(P):
    print('Iterating model for policy', p)
    print('Please stand by...')
    for m in range(T_horizon+1):
        if(m==0):
            C_max = Y_target 
            C_min = 0
#            K_series[m,p] = K_0
        else:
            C = C_series[m-1,p]
            C_max = C*1.05    
            C_min = C*0.95                    
        finished = 0
        counter = 0    
        max_iter = 50000
#        print("Optimizing period m=", m)
 #       print('tau = ', tau_bar)
        
        while finished == 0 and counter <=max_iter:      
            counter += 1
            if m==0:
                S_1 = S_1_in
                S_2 = S_2_in
                v_old = v_in
                K = K_0        
                #h = h_0
                #e = e_0
                R = R_0
            else:
                S_1 = S_1_series[m-1,p]
                S_2 = S_2_series[m-1,p]
                v_old = v_series[m-1,p]
                K = K_series[m,p]          
                R = R_series[m-1,p]
            C_0 = (C_max + C_min)/2                   
            C = C_0       
            #print("Trying C_0=", C)
            #print("C_max = ", C_max)
            #print("C_min = ", C_min)                                
            for t in range(m, m+T_ahead):        
               if t==0:
                   tau_bar = 0
               else:
                   tau_bar =Policies[p]
               h = h_0*(1+g_h)**t
               e = e_0*(1+g_e)**t               
               N = N_s_series[t]
               E = compute_equilibrium(K, N, v_old, S_1, S_2, h, e)
               #print('E=', E)
               Y = E[0]
               X = E[1]
               r = E[2]
               v = E[3]
               C = C*(beta*r)**(1/sigma)
               X_series[t,p] = X
               Y_series[t,p] = Y
               r_series[t,p] = r
               v_series[t,p] = v
               K_series[t,p] = K
               C_series[t,p] = C
               tau_series[t,p] = tau_bar*Y
               eta = eta_x(K, h*N, e*X)
               w_series[t,p] = (1-alpha)*(1-eta)*Y/N
               S = update_climate_state(S_1, S_2, X)
               S_1_series[t,p] = S[0] 
               S_2_series[t,p] = S[1] 
               S_all_series[t,p] = S[0] + S[1]                
               Temp_series[t,p] = 3*np.log((S[0] + S[1])/S_bar)/np.log(2) 
               Temp_rel_series[t,p] = Temp_series[t,p] - Temp_series[0,p]
               h_series[t,p] = h
               e_series[t,p] = e
               R_series[t,p] = R-X  
               tau_series[t,p] = tau_bar*Y
               K = Y - c_x*X - C     
               #h = (1+g_h)*h
               #e = (1+g_e)*e           
               tau_in_dollar_per_ton_of_CO2_series[t,p] = tau_bar*Y*10**6*12/44               
                            
               if t==m+T_ahead-1 or abs(C_max-C_min) < err_tol:    
                 #print("no notable difference between consumption values- moving on")
                 finished = 1               
               if K<0.01*(Y-c_x*X):
                   #print("Consumption too high")
                   C_max = C_0
                   break
               if C<0.01*(Y- c_x*X):
                   #print("Consumption too low")
                   C_min = C_0
                   break       
               
                


##############################################################################
#  4. Diagnostic checking  
##############################################################################
if diagnostic_check == 'yes' :   
    # Evaluate shooting accuracy by evaluating the adjustments in consumption: 
    cons_adj = np.empty((T_horizon, P))
    cons_adj_val = 0 
    for p in range(P):
        cons_adj[0,p] =0
        for t in range(1,T_horizon):
            C = C_series[t,p]
            C_old = C_series[t-1,p]
            r = r_series[t,p]
            cons_adj[t,p] = abs(C - C_old*(beta*r)**(1/sigma))     
            cons_adj_val = max(cons_adj_val, cons_adj[t,p]/C_series[t,p]*100)         
    zero_profit_error = np.empty((T_horizon, P))
    r_error = np.empty((T_horizon, P))
    v_error = np.empty((T_horizon, P))
    max_zero_profit_error = 0  
    max_r_error =0
    max_v_error =0  
   
    
    for p in range(P):
        for t in range(0,T_horizon):
            Y = Y_series[t,p]
            h = h_series[t,p]
            e = e_series[t,p]
            N = N_s_series[t]
            K = K_series[t,p]
            X = X_series[t,p]
            eta = eta_x(K, h*N, e*X)
            w = w_series[t,p]
            r = r_series[t,p]
            v = v_series[t,p]
            tau = tau_series[t,p]       
            err = abs(Y - r*K - w*N - (v + tau)*X) 
            zero_profit_error[t,p] = err          
            max_zero_profit_error = max(max_zero_profit_error, err)
            err = abs(r - alpha*(1-eta)*Y/K)    
            r_error[t,p] = err   
            max_r_error = max(max_r_error, err)   
            err = abs(v + tau - Y*eta/X)                          
            v_error[t,p] = err     
            max_v_error = max(max_v_error, err)   
            D_val = D(S_all_series[t,p])
            F_val = F(K,N*h, e*X)              
            err = eta*Y/X  - c_x -tau 
            
    print('Accuracy of equilibrium:')
    print('Maximum percentage re-adjustment in consumption:', cons_adj_val)
    print('Maximum error in zero-profit constraint:', max_zero_profit_error)
    print('Maximum error in determination of interest rates:', max_r_error)
    print('Maximum error in  determination of resource prices:', max_v_error)


                    
##############################################################################
#  5. Post-processing 
##############################################################################

# Time windiw for the plots: 
Time_window = np.empty(T_horizon)
for t in range(T_horizon):
    Time_window[t] = 2010 + 10*t

if show_plots == 'yes':
    print('Simulation output:')
    T_plot = 11
    plt.plot(Time_window[0:T_plot], X_series[0:T_plot,0], color="red", linewidth=1, linestyle="-", label="Laissez-faire")
    plt.plot(Time_window[0:T_plot], X_series[0:T_plot,1], color="green", linewidth=1, linestyle="-", label="Optimal")
    plt.xlabel("t (decades)") 
    plt.ylabel("Emissions in GtC") 
    plt.legend(loc='best')
    if save_figs == 'yes':
        plt.savefig('Model_1_emissions.eps', format='eps', dpi=1000)
    plt.show()
    
    T_plot = 5
    plt.plot(Time_window[0:T_plot], 1000*Y_series[0:T_plot,0], color="red", linewidth=1, linestyle="-", label="Laissez-faire")
    plt.plot(Time_window[0:T_plot], 1000*Y_series[0:T_plot,1], color="green", linewidth=1, linestyle="-", label="Optimal")
    plt.xlabel("t (decades)") 
    plt.ylabel("Output in trillion U.S. dollar") 
    plt.legend(loc='best')
    if save_figs == 'yes':
        plt.savefig('Model_1_output.eps', format='eps', dpi=1000)
    plt.show()

    T_plot = 15
    plt.plot(Time_window[0:T_plot], 1000*Y_series[0:T_plot,0], color="red", linewidth=1, linestyle="-", label="Laissez-faire")
    plt.plot(Time_window[0:T_plot], 1000*Y_series[0:T_plot,1], color="green", linewidth=1, linestyle="-", label="Optimal")
    plt.xlabel("t (decades)") 
    plt.ylabel("Output in trillion U.S. dollar") 
    plt.legend(loc='best')
    if save_figs == 'yes':
        plt.savefig('Model_1_output_long.eps', format='eps', dpi=1000)
    plt.show()
    
    T_plot = 25    
    Double_pre_industrial = [2*581]*T 
    plt.plot(Time_window[0:T_plot], S_all_series[0:T_plot,0], color="red", linewidth=1, linestyle="-", label="Laissez-faire")
    plt.plot(Time_window[0:T_plot], S_all_series[0:T_plot,1], color="green", linewidth=1, linestyle="-", label="Optimal")
    plt.plot(Time_window[0:T_plot], Double_pre_industrial[0:T_plot], color="red", linewidth=1, linestyle="--", label="Double pre-industrial")
    plt.xlabel("t (decades)") 
    plt.ylabel("Atmospheric carbon in Gt C") 
    plt.legend(loc='best')
    if save_figs == 'yes':
        plt.savefig('Model_1_carbon.eps', format='eps', dpi=1000)
    plt.show()     
    
    Two_degrees = [1.1]*T
    plt.plot(Time_window[0:T_plot], Temp_rel_series[0:T_plot,0], color="red", linewidth=1, linestyle="-", label="Laissez-faire")
    plt.plot(Time_window[0:T_plot], Temp_rel_series[0:T_plot,1], color="green", linewidth=1, linestyle="-", label="Optimal")
    plt.plot(Time_window[0:T_plot], Two_degrees[0:T_plot], color="red", linewidth=1, linestyle="--", label="Two-degrees")
    plt.xlabel("t (decades)") 
    plt.ylabel("Temperature in degree C") 
    plt.legend(loc='best')
    if save_figs == 'yes':
        plt.savefig('Model_1_temperature.eps', format='eps', dpi=1000)
    plt.show()
       
    Fifty = [50]*T
    plt.plot(Time_window[0:T_plot], tau_in_dollar_per_ton_of_CO2_series[0:T_plot,0], color="red", linewidth=1, linestyle="-", label="Laissez-faire")
    plt.plot(Time_window[0:T_plot], tau_in_dollar_per_ton_of_CO2_series[0:T_plot,1], color="green", linewidth=1, linestyle="-", label="Optimal")
    plt.plot(Time_window[0:T_plot], Fifty[0:T_plot], color="red", linewidth=1, linestyle="--", label="50 dollars")
    plt.xlabel("t (decades)") 
    plt.ylabel("Tax in U.S.dollars per ton of CO2") 
    plt.legend(loc='best')
    if save_figs == 'yes':
        plt.savefig('Model_1_tax.eps', format='eps', dpi=1000)
    plt.show()
    