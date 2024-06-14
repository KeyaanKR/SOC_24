from typing import Callable
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

def func(t, v, k):
    """ computes the function S(t) with constants v and k """
    
    # TODO: return the given function S(t)
    return v*(t-((1-np.exp(-k*t))/k))
    # END TODO


def find_constants(df: pd.DataFrame, func: Callable):
    """ returns the constants v and k """

    v = 0
    k = 0

    # TODO: fit a curve using SciPy to estimate v and k
    t = df['t'].values
    S = df['S'].values
    popt, pcov = curve_fit(func,t,S)
    v,k = popt
    # END TODO

    return v, k


if __name__ == "__main__":
    df = pd.read_csv("data.csv")
    v, k = find_constants(df, func)
    v = v.round(4)
    k = k.round(4)
    print(v, k)

    # TODO: plot a histogram and save to fit_curve.png

    # Extract t and S from the DataFrame
    t = df['t'].values
    S = df['S'].values

    # Generate the fitted curve
    fitted_S = func(t, v, k)

    # Create a plot
    plt.figure()

    # Plot the original data points
    plt.scatter(t, S, label='data', color='blue',marker='*')

    # Plot the fitted curve
    plt.plot(t, fitted_S, label=f'fit: v={v}, k={k}', color='red')

    # Add labels and legend
    plt.xlabel('t')
    plt.ylabel('S')
    plt.legend()
    
    # Save the plot
    plt.savefig('fit_curve.png')
    plt.close()

    # END TODO
