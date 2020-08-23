import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.integrate import quad
from math import *  #lets the user enter complicated functions easily, eg: exp(3*sin(x**2))

def good_ylim(values, default):  # log scale can give ugly ticks for y values. This fixes that with a 0 and a power of 10 times a digit, like 9e-2. Always.
    mini, maxi = min(values), max(values)
    if mini <= maxi <= 0 :
        newBottom = -(int(str(-mini)[0]) + 1) * 10 ** floor(log10(-mini))
        newTop = 0
    elif maxi >= mini >= 0:
        newBottom = 0
        newTop = (int(str(maxi)[0]) + 1) * 10 ** floor(log10(maxi))
    elif mini < 0 < maxi:
        newBottom = -(int(str(-mini)[0]) + 1) * 10 ** floor(log10(-mini))
        newTop = (int(str(maxi)[0]) + 1) * 10 ** floor(log10(maxi))
    else: return default #just in case, prevents crashing
    return newBottom, newTop

def main():
    formula = input("f(x) = ")
    f = lambda x: eval(formula)
    xmin, xmax = eval(input("Interval of integration, [xmin, xmax] = "))
    boolLogX = input("Logarithmic x scale for graphing f(x) ? [y/n]").lower() == 'y'
    boolLogY = input("Logarithmic y scale for graphing f(x) ? [y/n]").lower() == 'y'

    #change the following line to whatever you want and everything shall adapt to that.
    listn = [10, 100, 1000, 10000]  #10000 isn't necessary, it lengthens the computations but offers far greater precision.
    lenContinuous = 100000   #100000 is very precise, but 10000 can be used fine, it shouldn't make a difference on most computers, pixel-wise.
    *listListx, continuous_x = (np.linspace(xmin, xmax - (xmax - xmin) / n, n) for n in listn + [lenContinuous])
    #computation above is to not include the last rectangle in the  sum, which would be wrong. Change this to compute a right Riemann sum.
    *listListy, continuous_y = (np.fromiter(map(f, listx), dtype=float) for listx in (listListx + [continuous_x]))

    fig = plt.gcf()
    fig.suptitle(f"Study of the function y = {formula} on the interval [{xmin}, {xmax}] and of the error compared to the exact value")

    areaAxes = (fig.add_subplot(len(listn), 2, i) for i in range(1, 2 * (len(listn)) + 1, 2))

    for ax, listx, listy in zip(areaAxes, listListx, listListy):
        ax.plot(continuous_x, continuous_y)
        ax.bar(listx, listy, align='edge', width=(listx[-1] - listx[0]) / (len(listx) - 1), alpha=0.5)
        if boolLogX: ax.set_xscale('log')
        if boolLogY: ax.set_yscale('log')
        ax.set_title(f"Visualization of the Riemann sum with {len(listx)} rectangles")
        ax.grid(True)

    exact = quad(f, xmin, xmax)[0]
    if exact == 0:
        listdist = [(listy.mean() * (listx[-1] - xmin) - exact) for listx, listy in zip(listListx, listListy)]
        titles = ("difference for each approximation compared to the exact value of the integral, 0",
                  "difference for each approximation compared to the exact value of the integral, 0, on a logarithmic scale")
    else:
        listdist = [(100 * (listy.mean() * (listx[-1] - xmin) - exact) / exact) for listx, listy in zip(listListx, listListy)]
        titles = (f"error percentage for each sum compared to the exact integral: {exact}",
                  f"error percentage for each sum compared to the exact integral: {exact}, on a logarithmic scale")

    accuracyAxes = [fig.add_subplot(2, 2, i) for i in (2, 4)]

    ax = accuracyAxes[0]
    ax.plot(listn, listdist)
    ax.grid(True)
    ax.set_title(titles[0])

    ax = accuracyAxes[1]
    ax.plot(listn, listdist)
    ax.set_xscale("log")
    ax.get_xaxis().set_tick_params(which='minor', size=0)
    ax.get_xaxis().set_tick_params(which='minor', width=0)
    ax.set_yscale("symlog")
    ax.set_ylim(good_ylim(listdist, ax.get_ylim()))
    #ax.yaxis.set_minor_locator(ticker.LogLocator(subs=(1.0, 2.0, 3.0, 6.0)))
    #ax.yaxis.set_minor_formatter(ticker.LogFormatter(labelOnlyBase=False))
    # TODO: make appear the minor ticks on the y axis
    ax.set_title(titles[1])
    ax.grid(True, which='major')

    fig.subplots_adjust(left=0.05, bottom=0.05,right=0.95, top=0.9, wspace=0.2, hspace=0.6)
    plt.show()

if __name__ == '__main__':
    main()