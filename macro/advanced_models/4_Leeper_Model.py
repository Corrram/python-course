# -*- coding: utf-8 -*-
"""
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize

##############################################################################
# 0. Simulation paramaeters
##############################################################################

# Length of iteration: 
length = 2000
show_plots = 'yes'
save_figs = 'no'
##############################################################################
# 1. Model parameters
##############################################################################
# Nominal emprical targets in trillion (10**12) U.S. dollar: 
c_target = 18
b_target = 32
y_target = 25
m_target = 20
# Initial values:
# Initial nominal money stock outstanding in trillion U.S. dollars: 
m_n_old = m_target
# Initial nominal bonds outstanding in trillion U.S. dollars: 
b_n_old = b_target
# Price level from previous period t = -1:
p_old = 1
# Previous nominal interest rate on bonds:
i_old = 0.03
# Initial price of money
p_m_old = i_old/(1+i_old)
# Total initial oustanding nominal liabilities
a_n_old = m_n_old + b_n_old*(1+i_old)

 # Consumer parameters:
# Use this to back out constant seignorage and utility parameter gamma: 
s_m = m_target*p_m_old#/1000
#s_m = 1
gamma = s_m/c_target 
# Discount factor and real inteers rate and return: 
beta = 0.99 
r= 1/beta -1 
R = 1+ r

# Policy parameters:
# Monetary policy parameters (Taylor rule)
pi_target = 0.02
alpha_pi = .9

# Fiscal policy parameters (Tax rule)
tau_target= 6.9
alpha_b = 0.001
g_star =  y_target- c_target

s_f_bar = tau_target - g_star 
# Minimal inflation rate to produce positive interest rates:
pi_min = (beta-1+pi_target*(alpha_pi*beta**2))/(alpha_pi*beta**2)


# Parameter check
assert 0<beta < 1
assert m_n_old >0
assert p_old >0
assert i_old >0

##############################################################################
# 2. Functions
##############################################################################
# Taylor rule
def I(pi):
    return (1+pi_target)/beta-1 + alpha_pi*(pi-pi_target)
# Money demand function
def M_d(i):
    return s_m*(1+i)/i
# Fiscal rule
def S_f(b):
    return s_f_bar + alpha_b*b
# Dynamic law of motion for inflation
def G(pi):
    return  pi_target + alpha_pi*beta*(pi-pi_target)

S_all_series = []    
def J(pi):
    S_all = 0
    m_old = m_n_old/p_old 
    for t in range(10**4):
        m = M_d(I(pi))                
        Dm = m - m_old/(1+pi)
        s = s_f_bar + Dm
        S_all += s/(R-alpha_b)**t
        m_old = m
        pi = G(pi)  
        S_all_series.append(S_all) 
    return S_all   

def compute_initial_state(pi_guess):
    H = lambda pi: J(pi) - ((1+i_old)/(1+pi) -alpha_b)*b_n_old/p_old
    solution = scipy.optimize.root(H, pi_guess)
    sol_value = solution.x
    return sol_value[0]


##############################################################################
# 3. Steady state 
##############################################################################
# Steady state values: 
pi_bar = pi_target
i_bar = I(pi_bar)
m_bar = M_d(i_bar)
DM_bar = m_bar*pi_bar/(1+pi_bar)        
b_bar = (s_f_bar + DM_bar)/(r-alpha_b)
    # i_bar = (pi_target+1)/beta-1 - alpha_pi*beta*pi_target

##############################################################################
# 4. Iteration 
##############################################################################
# M passive, F passive:
if alpha_pi < R and alpha_b >r:    
    print('Case 1: Monetary policy passive, fiscal policy passive')
    pi_vals = [0.01, pi_bar, 0.1]
# M passive, F active:
if alpha_pi < R and alpha_b <r:    
    print('Case 2: Monetary policy passive, fiscal policy active')
    #pi_max = 10
    pi_0 = compute_initial_state(pi_bar)          
    assert pi_0 > pi_min, 'Fatal error: No equilibrium exists!' 
    pi_vals = [pi_0]
# M active, F passive:
if alpha_pi > R and alpha_b >r:
    print('Case 3: Monetary policy active, fiscal policy passive')
    pi_0 = pi_bar
    pi_vals = [pi_bar]
if alpha_pi > R and alpha_b <r:
    print('Case 4: Monetary policy active, fiscal policy active')
    print('Sorry, no equilibrium exists')
    pi_vals = []
    

# Arrays to store values in
pi_series = np.empty((length, len(pi_vals)))
b_series = np.empty((length, len(pi_vals)))
i_series = np.empty((length, len(pi_vals)))
m_series = np.empty((length, len(pi_vals)))
Dm_series = np.empty((length, len(pi_vals)))
s_f_series = np.empty((length, len(pi_vals)))

p=0
for pi in pi_vals:
    i = I(pi)
    m = M_d(i)
    b = a_n_old/p_old/(1+pi) - S_f(b_n_old/p_old) - M_d(I(pi))    
    Dm = m - m_n_old/p_old/(1+pi)
    s_f = S_f(b_n_old/p_old)
    for t in range(length):
        # Save values 
        pi_series[t,p] = pi
        i_series[t,p] = i
        m_series[t,p] = m
        Dm_series[t,p] = Dm
        s_f_series[t,p] = s_f
        b_series[t,p] = b
        # Update values
        pi = G(pi)
        i = I(pi)        
        m_old = m
        m = M_d(i)
        Dm = m - m_old/(1+pi)
        s_f = S_f(b)
        b = R*b - s_f - Dm        
    p+=1     
        
        
        
##############################################################################
# 5. Post-processing
##############################################################################   

colors = ['red', 'purple', 'blue']
colors2 = ['darkturquoise', 'mediumblue', 'hotpink']
colors3 = ['orangered', 'firebrick', 'maroon']
colors4 = ['slategrey', 'royalblue', 'blueviolet']
colors5 = ['peru', 'darkgrey', 'gold']
colors6 = ['goldenrod', 'navy', 'saddlebrown']

if show_plots == 'yes' and len(pi_vals)>0:  
    T_1 = 50 
    print('Time series of inflation:')
    for p in range(len(pi_vals)):
        plt.plot(pi_series[0:T_1,p], color = colors[p], linewidth=1, linestyle="-", label = "Inflation rate")
    plt.xlabel(r"$t$") 
    plt.ylabel(r"$\pi_t$") 
    plt.legend(loc='best')
    if save_figs == 'yes':
       plt.savefig('../MySlides/figures/Leeper_model_Case_3_inflation.eps', format='eps', dpi=1000)
    plt.show()    

    print('Time series of nominal interest rate:')
    for p in range(len(pi_vals)):
        plt.plot(i_series[0:T_1,p], color = colors2[p], linewidth=1, linestyle="-", label = "Nominal interest rate")
    plt.xlabel("Period $t$") 
    #plt.ylabel("Nominal interest rate") 
    plt.ylabel(r"$i_t$") 
    plt.xlabel(r"$t$") 
    plt.legend(loc='best')
    if save_figs == 'yes':
        plt.savefig('../MySlides/figures/Leeper_model_Case_3_interest.eps', format='eps', dpi=1000)
    plt.show()    

    print('Time series of real money balances:')
    for p in range(len(pi_vals)):
        plt.plot(m_series[0:T_1,p], color = colors3[p], linewidth=1, linestyle="-", label = "Real money balances")
    plt.xlabel(r"$t$") 
    plt.ylabel(r"$m_t$") 
    plt.legend(loc='best')
    if save_figs == 'yes':
        plt.savefig('../MySlides/figures/Leeper_model_Case_3_money.eps', format='eps', dpi=1000)
    plt.show()    

    T_1 = 1000

    print('Time series of fiscal surpluses:')
    for p in range(len(pi_vals)):
        plt.plot(s_f_series[0:T_1,p], color = colors4[p], linewidth=1, linestyle="-", label = "Real fiscal surpluses")
    plt.xlabel(r"$t$") 
    plt.ylabel(r"$s_t^f$") 
    plt.legend(loc='best')
    if save_figs == 'yes':
        plt.savefig('../MySlides/figures/Leeper_model_Case_3_surpluses.eps', format='eps', dpi=1000)
    plt.show()    

    print('Time series of real debt dynamics:')
    for p in range(len(pi_vals)):
        plt.plot(b_series[0:T_1,p], color = colors5[p], linewidth=1, linestyle="-", label = 'Real fiscal debt')
    plt.xlabel(r"$t$") 
    plt.ylabel(r"$b_t$") 
    plt.legend(loc='best')
    if save_figs == 'yes':
        plt.savefig('../MySlides/figures/Leeper_model_Case_3_debt.eps', format='eps', dpi=1000)
    plt.show()    
    
    T_1=50
    print('Time series of changes in real money balances (seignorage):')
    for p in range(len(pi_vals)):
        plt.plot(Dm_series[0:T_1,p], color = colors6[p], linewidth=1, linestyle="-", label = 'Real seignorage')
    plt.xlabel(r"$t$") 
    plt.ylabel(r"$\Delta m_t$") 
    plt.legend(loc='best')
    if save_figs == 'yes':
        plt.savefig('../MySlides/figures/Leeper_model_Case_3_seignorage.eps', format='eps', dpi=1000)
    plt.show()    
    

        
        
        
        
    
    
