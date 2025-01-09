# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 09:38:34 2021

@author: Marten Hillebrand (marten.hillebrand@vwl.uni-freiburg.de)
"""

import numpy as np
import matplotlib.pyplot as plt
from math import log
import scipy.optimize


# Length of iteration:
T = 300
# Do you want to see the plots?
show_plots = "yes"
# show_plots = 'no'
# Do you want to save the figures?
# save_figs = 'yes'
save_figs = "no"

##############################################################################
# A. Model parameters
##############################################################################
# Savings rate:
s = 0.4
# Population growth rate:
g_N = 0.02
# Labor efficiency growth rate:
g_h = 0.01
# Rate of depreciation:
delta = 0.5
# Production parameters (CES function):
alpha = 1 / 3
# Elasticity of substitution (1=Cobb-Douglas)
sigma = 1
# sigma =1 is the Cobb-Douglas case
theta = 2

##############################################################################
# B. Initial conditions:
##############################################################################
N_0 = 1000
h_0 = 1
K_0 = 500
# Determine initial labor force and its constant growth rate:
L_0 = h_0 * N_0
g_L = (1 + g_N) * (1 + g_h) - 1
# Initial capital intensity:
k_0 = K_0 / L_0
# Initial capital per capita:
k_p_0 = K_0 / N_0

# Check if parameters make economic sense
assert s > 0 and s <= 1
assert delta > 0 and delta <= 1
assert g_N > -1 and g_h >= 0
assert alpha > 0 and alpha < 1
assert sigma > 0
assert theta > 0
assert h_0 > 0
assert N_0 > 0
assert K_0 > 0


##############################################################################
# C. Functions
##############################################################################
# Production function (CES):
def f(k):
    rho = (sigma - 1) / sigma
    if rho == 0:
        f_value = theta * k**alpha
    else:
        f_value = theta * (alpha * k**rho + 1 - alpha) ** (1 / rho)
    return f_value


# Time-one map:
def G(k):
    G_value = 1 / (1 + g_L) * (s * f(k) + (1 - delta) * k)
    return G_value


# Fixed point map (zeroes are fixed points)
def H(k):
    H_value = G(k) - k
    return H_value


# Function to compute the fixed point:
def compute_fixed_point(k_guess):
    solution = scipy.optimize.root(H, k_guess)
    return solution.x


# Function to demonstrate existence of fixed point graphically:
def g(k):
    g_value = f(k) / k
    return g_value


##############################################################################
# D. Simulation parameters
##############################################################################
# Data-arrays to store values in:
k_series = np.empty(T + 1)
k_p_series = np.empty(T + 1)
K_series = np.empty(T + 1)
L_series = np.empty(T + 1)
Y_series = np.empty(T + 1)
y_series = np.empty(T + 1)
y_p_series = np.empty(T + 1)
C_series = np.empty(T + 1)
c_series = np.empty(T + 1)
log_y_series = np.empty(T + 1)
N_series = np.empty(T + 1)
h_series = np.empty(T + 1)
g_k_series = np.empty(T + 1)
g_k_p_series = np.empty(T + 1)
g_K_series = np.empty(T + 1)
g_y_series = np.empty(T + 1)
g_y_p_series = np.empty(T + 1)
g_Y_series = np.empty(T + 1)
g_C_series = np.empty(T + 1)
g_c_series = np.empty(T + 1)
g_N_series = np.empty(T + 1)
g_L_series = np.empty(T + 1)
log_y_p_series = np.empty(T + 1)
log_k_p_series = np.empty(T + 1)
log_y_p_trend_series = np.empty(T + 1)
log_k_p_trend_series = np.empty(T + 1)
log_y_p_trend_series2 = np.empty(T + 1)
log_k_p_trend_series2 = np.empty(T + 1)

##############################################################################
# E. Initialization
##############################################################################
# Set initial values:
K = K_0
L = L_0
N = N_0
h = h_0
k = k_0
k_p = k_p_0
Y = L * f(K / L)
C = (1 - s) * Y
y = Y / L
y_p = Y / N
c = C / N
# Endogenous gowth rates in t=0 are set to zero:
g_k_series[0] = 0
g_k_p_series[0] = 0
g_K_series[0] = 0
g_Y_series[0] = 0
g_y_series[0] = 0
g_y_p_series[0] = 0
g_C_series[0] = 0
g_c_series[0] = 0
g_N_series[0] = 0

##############################################################################
# F. Compute fixed point values
##############################################################################
k_bar_value = compute_fixed_point(2)
k_bar = k_bar_value[0]
y_bar = f(k_bar)
c_bar = (1 - s) * f(k_bar)

##############################################################################
# G. Iteration
##############################################################################
# Iterate system forward for T periods:
for t in range(T + 1):
    L_series[t] = L
    N_series[t] = N
    h_series[t] = h
    K_series[t] = K
    k_series[t] = k
    k_p_series[t] = k_p
    Y_series[t] = Y
    y_series[t] = y
    y_p_series[t] = y_p
    C_series[t] = C
    c_series[t] = c
    log_y_series[t] = log(y)
    log_y_p_series[t] = log(y_p)
    log_k_p_series[t] = log(k_p)
    log_y_p_trend_series[t] = log(y_bar) + t * log(1 + g_h)
    log_k_p_trend_series[t] = log(k_bar) + t * log(1 + g_h)
    if t > 0:
        g_N = N / N_series[t - 1] - 1
        g_k = k / k_series[t - 1] - 1
        g_k_p = k_p / k_p_series[t - 1] - 1
        g_K = K / K_series[t - 1] - 1
        g_Y = Y / Y_series[t - 1] - 1
        g_y = y / y_series[t - 1] - 1
        g_y_p = y_p / y_p_series[t - 1] - 1
        g_C = C / C_series[t - 1] - 1
        g_c = c / c_series[t - 1] - 1
        g_N_series[t] = g_N * 100
        g_k_series[t] = g_k * 100
        g_k_p_series[t] = g_k_p * 100
        g_K_series[t] = g_K * 100
        g_Y_series[t] = g_Y * 100
        g_y_series[t] = g_y * 100
        g_y_p_series[t] = g_y_p * 100
        g_C_series[t] = g_C * 100
        g_c_series[t] = g_c * 100
    #   Update values for t+1:
    k = G(k)
    L = (1 + g_L) * L
    K = k * L
    Y = L * f(k)
    C = (1 - s) * Y
    N = (1 + g_N) * N
    h = (1 + g_h) * h
    y = Y / L
    c = C / L
    k_p = K / N
    y_p = Y / N
    c_p = C / N

##############################################################################
# H. Post-processing
##############################################################################
if show_plots == "yes":
    T_1 = 25
    g_L_line = [g_L * 100] * T
    g_N_line = [g_N * 100] * T
    g_h_line = [g_h * 100] * T
    zero_line = [0] * T

    print("Production factors:")
    plt.plot(L_series[0:T_1], "bo", linewidth=1, linestyle="-", label="$L_t$")
    plt.plot(K_series[0:T_1], "ro", linewidth=1, linestyle="-", label="$K_t$")
    plt.xlabel("Period $t$")
    plt.ylabel("Production factors")
    plt.legend(loc="best")
    if save_figs == "yes":
        plt.savefig("../MySlides/figures/Solow_factors.eps", format="eps", dpi=1000)
    plt.show()

    print("Factor growth:")
    plt.plot(g_L_line[1:T_1], "bo", linewidth=1, linestyle="-", label="$g_{L}$")
    plt.plot(g_K_series[1:T_1], "ro", linewidth=1, linestyle="-", label="$g_{K,t}$")
    plt.xlabel("Period $t$")
    plt.ylabel("Growth rates of production factors in %")
    plt.legend(loc="best")
    if save_figs == "yes":
        plt.savefig(
            "../MySlides/figures/Solow_factor_growth.eps", format="eps", dpi=1000
        )
    plt.show()

    print("Level of GDP:")
    plt.plot(Y_series[0:T_1], "mo", linewidth=1, linestyle="-", label="$Y_t$")
    plt.xlabel("Period $t$")
    plt.ylabel("Real GDP")
    plt.legend(loc="best")
    if save_figs == "yes":
        plt.savefig("../MySlides/figures/Solow_output.eps", format="eps", dpi=1000)
    plt.show()

    print("Real GDP growth:")
    plt.plot(g_L_line[1:T_1], "bo", linewidth=1, linestyle="--", label="$g_L$")
    plt.plot(g_Y_series[1:T_1], "mo", linewidth=1, linestyle="-", label="$g_{Y,t}$")
    plt.xlabel("Period $t$")
    plt.ylabel("Real GDP growth in %")
    plt.legend(loc="best")
    if save_figs == "yes":
        plt.savefig(
            "../MySlides/figures/Solow_output_growth.eps", format="eps", dpi=1000
        )
    plt.show()

    print("Capital-labor ratio:")
    plt.plot(k_series[0:T_1], "ro", linewidth=1, linestyle="-", label="$k_t$")
    plt.xlabel("Period $t$")
    plt.ylabel("Capital intensity")
    plt.legend(loc="best")
    if save_figs == "yes":
        plt.savefig("../MySlides/figures/Solow_k.eps", format="eps", dpi=1000)
    plt.show()

    print("Growth rate of capital intensity:")
    plt.plot(zero_line[1:T_1], color="black", linewidth=1, linestyle="--", label="$0$")
    plt.plot(g_k_series[1:T_1], "ro", linewidth=1, linestyle="-", label="$g_{k,t}$")
    plt.xlabel("Period $t$")
    plt.ylabel("Growth rate of capital intensity in %")
    plt.legend(loc="best")
    if save_figs == "yes":
        plt.savefig("../MySlides/figures/Solow_g_k.eps", format="eps", dpi=1000)
    plt.show()

    print("Capital per capita:")
    plt.plot(k_p_series[0:T_1], "bo", linewidth=1, linestyle="-", label="$k_t^p$")
    plt.xlabel("Period $t$")
    plt.ylabel("Capital per capita")
    plt.legend(loc="best")
    if save_figs == "yes":
        plt.savefig("../MySlides/figures/Solow_k_p.eps", format="eps", dpi=1000)
    plt.show()

    print("Growth rate of capital per capita:")
    plt.plot(g_h_line[1:T_1], color="black", linewidth=1, linestyle="--", label="$g_h$")
    plt.plot(g_k_p_series[1:T_1], "bo", linewidth=1, linestyle="-", label="$g_{k^p,t}$")
    plt.xlabel("Period $t$")
    plt.ylabel("Growth rate of capital per capita in %")
    plt.legend(loc="best")
    if save_figs == "yes":
        plt.savefig("../MySlides/figures/Solow_g_k_p.eps", format="eps", dpi=1000)
    plt.show()

    print("Level of labor productivity:")
    plt.plot(y_series[0:T_1], "mo", linewidth=1, linestyle="-", label="$y_t$")
    plt.xlabel("Period $t$")
    plt.ylabel("Labor productivity")
    plt.legend(loc="best")
    if save_figs == "yes":
        plt.savefig("../MySlides/figures/Solow_y.eps", format="eps", dpi=1000)
    plt.show()

    print("Growth rate of labor productivity:")
    plt.plot(zero_line[1:T_1], color="black", linewidth=1, linestyle="--", label="$0$")
    plt.plot(g_y_series[1:T_1], "mo", linewidth=1, linestyle="-", label="$g_{y,t}$")
    plt.xlabel("Period $t$")
    plt.ylabel("Growth rate of labor productivity in %")
    plt.legend(loc="best")
    if save_figs == "yes":
        plt.savefig("../MySlides/figures/Solow_g_y.eps", format="eps", dpi=1000)
    plt.show()

    print("Level of real GDP per capita:")
    plt.plot(y_p_series[0:T_1], "go", linewidth=1, linestyle="-", label="$y^p_t$")
    plt.xlabel("Period $t$")
    plt.ylabel("Real GDP per capita")
    plt.legend(loc="best")
    if save_figs == "yes":
        plt.savefig("../MySlides/figures/Solow_y_p.eps", format="eps", dpi=1000)
    plt.show()

    print("Growth rate of real GDP per capita:")
    plt.plot(g_h_line[1:T_1], color="black", linewidth=1, linestyle="--", label="$g_h$")
    plt.plot(g_y_p_series[1:T_1], "go", linewidth=1, linestyle="-", label="$g_{y^p,t}$")
    plt.xlabel("Period $t$")
    plt.ylabel("Growth rate of real GDP per capita in %")
    plt.legend(loc="best")
    if save_figs == "yes":
        plt.savefig("../MySlides/figures/Solow_g_y_p.eps", format="eps", dpi=1000)
    plt.show()

    print("Real GDP per capita (log scale):")
    # plt.plot(log_y_p_trend_series2[0:T_1], color="red", linewidth=1, linestyle="--", label="Trend ($s_1=0.25$)")
    plt.plot(
        log_y_p_series[0:T_1], "go", linewidth=1, linestyle="-", label=r"$\log(y_t^p)$"
    )
    plt.plot(
        log_y_p_trend_series[0:T_1],
        color="red",
        linewidth=2,
        linestyle="-",
        label=r"$\log(\bar{y}_t^p)$",
    )
    plt.xlabel("Period $t$")
    plt.ylabel("Real GDP per capita (log scale )")
    plt.legend(loc="best")
    if save_figs == "yes":
        plt.savefig("../MySlides/figures/Solow_y_p_log.eps", format="eps", dpi=1000)
    plt.show()

    print("Time-one map:")
    Range = np.linspace(0.00001, 2 * k_bar, 100000)
    id_map = [x for x in Range]
    G_values = G(Range)
    plt.plot(Range, G_values, linewidth=1, linestyle="-", color="red", label="$G(k)$")
    plt.plot(Range, id_map, linewidth=1, linestyle="-", color="black", label="$id(k)$")
    plt.xlabel("$k_t$")
    plt.ylabel("$k_{t+1} = G(k_t)$")
    plt.legend(loc="best")
    if save_figs == "yes":
        plt.savefig(
            "../MySlides/figures/Solow_time_one_map.eps", format="eps", dpi=1000
        )
    plt.show()
