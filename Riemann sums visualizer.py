import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from math import *  #lets the user enter complicated functions easily, eg: exp(3*sin(x**2))

def good_ylim(values, default):  # log scale can give ugly ticks for y values. This fixes that with a 0 and a power of 10 times a digit, like 9e-2.
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

def graphAccuracy(axes, listn, exact, listdist):
    if exact == 0:
        titles = ("difference for each approximation compared to the exact value of the integral, 0",
                  "difference for each approximation compared to the exact value of the integral, 0, on a logarithmic scale")
    else:
        titles = (f"error percentage for each approximation compared to the exact integral: {exact}",
                  f"error percentage for each approximation compared to the exact integral: {exact}, on a logarithmic scale")

    ax = axes[0]
    ax.plot(listn, listdist)
    for x, y in zip(listn, listdist):
        ax.text(x, y, f"{max(str(y)[:7], str(int(y)), key=len)}")
    ax.grid(True)
    ax.set_title(titles[0])

    ax = axes[1]
    ax.plot(listn, listdist)
    ax.set_xscale("log")
    ax.get_xaxis().set_tick_params(which='minor', size=0)
    ax.get_xaxis().set_tick_params(which='minor', width=0)
    ax.set_yscale("symlog")
    ax.set_ylim(good_ylim(listdist, ax.get_ylim()))
    for x, y in zip(listn, listdist):
        ax.text(x, y, f"{max(str(y)[:7], str(int(y)), key=len)}")
    ax.set_title(titles[1])
    ax.grid(True, which='major')

def simpleRiemann(fig, f, formula, xmin, xmax, boolLogX, boolLogY, listn, lenContinuous, side):
    #each listx contains the coordinates of the appropriate side, listy the corresponding y values
    if side=='left':
        *listListx, continuous_x = (np.linspace(xmin, xmax - (xmax - xmin) / n, n) for n in listn + [lenContinuous])
        listWidth = tuple((listx[-1] - listx[0]) / (len(listx) - 1) for listx in listListx)
    else:
        *listListx, continuous_x = (np.linspace(xmin + (xmax - xmin) / n, xmax, n) for n in listn + [lenContinuous])
        listWidth = tuple(-(listx[-1] - listx[0]) / (len(listx) - 1) for listx in listListx) # the - sign matters for proper display later
    *listListy, continuous_y = (np.fromiter(map(f, listx), dtype=float) for listx in (listListx + [continuous_x]))

    fig.suptitle(f"Study of the function y = {formula} on the interval ({xmin}, {xmax}) "
                 f"and of the error of some {side} Riemann sums compared to the exact value")

    areaAxes = (fig.add_subplot(len(listn), 2, i) for i in range(1, 2 * (len(listn)) + 1, 2))  #the left side of the figure

    for ax, listx, listy, width in zip(areaAxes, listListx, listListy, listWidth):
        ax.plot(continuous_x, continuous_y)
        ax.bar(listx, listy, align='edge', alpha=0.5, width=width,
               color=list("#70db70" if y >= 0 else "#ff6666" for y in listy),)
        if boolLogX: ax.set_xscale('log')
        if boolLogY: ax.set_yscale('log')
        ax.set_title(f"Visualization of the {side} Riemann sum with {len(listx)} rectangles")
        ax.grid(True)

    exact = quad(f, xmin, xmax)[0]
    if exact == 0:
        listdist = [(listy.mean() * (listx[-1] - xmin) - exact) for listx, listy in zip(listListx, listListy)]
    else:
        listdist = [(100 * (listy.mean() * (listx[-1] - xmin) - exact) / exact) for listx, listy in zip(listListx, listListy)]

    accuracyAxes = [fig.add_subplot(2, 2, i) for i in (2, 4)]
    graphAccuracy(accuracyAxes, listn, exact, listdist)

def midpoint(fig, f, formula, xmin, xmax, boolLogX, boolLogY, listn, lenContinuous):
    *listListx, continuous_x = (np.linspace(xmin, xmax - (xmax - xmin) / n, n) + (xmax - xmin) / (2 * n) for n in listn + [lenContinuous]) #This is the list of the middles
    listWidth = tuple((listx[-1] - listx[0]) / (len(listx) - 1) for listx in listListx)
    *listListy, continuous_y = (np.fromiter(map(f, listx), dtype=float) for listx in (listListx + [continuous_x]))

    fig.suptitle(f"Study of the function y = {formula} on the interval ({xmin}, {xmax}) "
                 f"and of the error of some midpoint sums compared to the exact value")

    areaAxes = (fig.add_subplot(len(listn), 2, i) for i in range(1, 2 * (len(listn)) + 1, 2))  # the left side of the figure

    for ax, listx, listy, width in zip(areaAxes, listListx, listListy, listWidth):
        ax.plot(continuous_x, continuous_y)
        ax.bar(listx, listy, alpha=0.5, width=width,
               color=list("#70db70" if y >= 0 else "#ff6666" for y in listy), )
        if boolLogX: ax.set_xscale('log')
        if boolLogY: ax.set_yscale('log')
        ax.set_title(f"Visualization of the midpoint Riemann sum with {len(listx)} rectangles")
        ax.grid(True)

    exact = quad(f, xmin, xmax)[0]
    if exact == 0:
        listdist = [(listy.mean() * (listx[-1] - xmin) - exact) for listx, listy in zip(listListx, listListy)]
    else:
        listdist = [(100 * (listy.mean() * (listx[-1] - xmin) - exact) / exact) for listx, listy in zip(listListx, listListy)]

    accuracyAxes = [fig.add_subplot(2, 2, i) for i in (2, 4)]
    graphAccuracy(accuracyAxes, listn, exact, listdist)

def main():
    fig = plt.gcf()
    formula = input("f(x) = ")
    f = lambda x: eval(formula)
    xmin, xmax = eval(input("Interval of integration, (xmin, xmax) = "))
    boolLogX = input("Logarithmic x scale for graphing f(x) ? [y/n]").lower() == 'y'
    boolLogY = input("Logarithmic y scale for graphing f(x) ? [y/n]").lower() == 'y'
    listn = list(map(int, input("what number of rectangles would you like to study ? use comma separated values, "
                                "like \"10, 100, 1000, 10000\", spaces don't matter: ").split(',')))
    lenContinuous = 100000  # 100000 is very precise, but 10000 can be used fine, it only matters for zooming in a lot.

    args = [fig, f, formula, xmin, xmax, boolLogX, boolLogY, listn, lenContinuous]

    dictMethod = {
        1: simpleRiemann,
        2: midpoint,
    }
    method = dictMethod[int(input("What method would you like to use ? 1 for basic Riemann sums, 2 for midpoint sums: "))]
    if method == simpleRiemann:
        args.append(input("what side would you like ? Left Riemann sums, or right Riemann sums ? [left/right]: "))
    method(*args)

    fig.subplots_adjust(left=0.05, bottom=0.05,right=0.95, top=0.9, wspace=0.1, hspace=0.6)
    plt.show()

if __name__ == '__main__':
    main()
