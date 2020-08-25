import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from math import *  #lets the user enter complicated functions easily, eg: exp(3*sin(x**2))
import pyinputplus as pyip # makes taking inputs more convenient for the user

# prevents a warning for calling ax.set_yscale("symlog", linthresh=1e-30) with linthresh where it is.
import warnings
warnings.filterwarnings("ignore", category=__import__('matplotlib').cbook.mplDeprecation)


def good_ylim(ax, values):  # symlog scale can give ugly limits for y values. This fixes that with a 0 and a power of 10 times a digit, like 9e-2.
    mini, maxi = min(values), max(values)
    newBottom, newTop = ax.get_ylim()
    if mini < 0 < maxi:
        newBottom = -(int(str(-mini / 10 ** floor(log10(-mini)))[0]) + 1) * 10 ** floor(log10(-mini))
        newTop = (int(str(maxi / 10 ** floor(log10(maxi)))[0]) + 1) * 10 ** floor(log10(maxi))
        ax.yticks(list(ax.yticks()[0]) + [0])  # adds 0 to the major ticks, as it is not always there by default, doesn't seem to work though
    elif mini < maxi <= 0 :
        newBottom = -(int(str(-mini / 10 ** floor(log10(-mini)))[0]) + 1) * 10 ** floor(log10(-mini))
        newTop = 0
    elif 0 <= mini < maxi:
        newBottom = 0
        newTop = (int(str(maxi / 10 ** floor(log10(maxi)))[0]) + 1) * 10 ** floor(log10(maxi))
    ax.set_ylim(newBottom, newTop)


def niceStr(val):   #gives a nice value, avoids having far too many digits display.
    if 100 < abs(val) < 1000000:   #just take away a few decimal digits
        return str(round(val, max(0, 6 - floor(log10(abs(val))))))
    #if it is in scientific notation, keep the scientific notation, just reduce the number of digits
    string = str(val)
    end = string.find('e')
    if end != -1:
        return string[:6] + string[end:]
    else:
        return string[:6]


def graphAccuracy(axes, list_n, exact, errorBound, listDist):
    errorBounder = np.vectorize(lambda x: x if abs(x) > errorBound else 0)
    listDist = errorBounder(listDist)
    if 0 in listDist:
        print(f"Some 0s are displayed in the accuracy check, however this does not mean necessarily mean the accuracy is perfect:\n"
              f"the exact value is computed with a certain margin of error, here it is {niceStr(errorBound)}\n"
              f"and any 0 displayed here means the inacurracy is less than this, and thus too small to be evaluated properly")
    if exact == 0:
        titles = ("difference for each approximation compared to the exact value of the integral, 0",
                  "difference for each approximation compared to the exact value of the integral, 0, on a logarithmic scale")
    else:
        listDist =  listDist * (100 / exact)
        titles = (f"error percentage for each approximation compared to the exact integral: {niceStr(exact)}",
                  f"error percentage for each approximation compared to the exact integral: {niceStr(exact)}, on a logarithmic scale")


    ax = axes[0]
    ax.plot(list_n, listDist)
    for x, y in zip(list_n, listDist):
        ax.text(x, y, niceStr(y))
    ax.grid(True)
    ax.set_title(titles[0])

    ax = axes[1]
    ax.plot(list_n, listDist)
    ax.set_xscale("log")
    ax.get_xaxis().set_tick_params(which='minor', size=0)
    ax.get_xaxis().set_tick_params(which='minor', width=0)
    ax.set_yscale("symlog", linthresh=1e-30)
    good_ylim(ax, listDist)  #sets the y limits to something a bit cleaner
    for x, y in zip(list_n, listDist):
        ax.text(x, y, niceStr(y))
    ax.set_title(titles[1])
    ax.grid(True, which='major')


def simpleRiemann(fig, f, formula, xmin, xmax, boolLogX, boolLogY, list_n, lenContinuous):
    side = input("what side would you like ? Left Riemann sums, or right Riemann sums ? [left/right]: ")
    #each listx contains the coordinates of the appropriate side, listy the corresponding y values
    if side=='left':
        *listList_x, continuous_x = (np.linspace(xmin, xmax - (xmax - xmin) / n, n) for n in list_n + [lenContinuous])
        listWidth = tuple((xmax - xmin) / (len(list_x)) for list_x in listList_x)
    else:
        *listList_x, continuous_x = (np.linspace(xmin + (xmax - xmin) / n, xmax, n) for n in list_n + [lenContinuous])
        listWidth = tuple(-(list_x[-1] - list_x[0]) / (len(list_x) - 1) for list_x in listList_x) # the - sign matters for proper display later
    *listList_y, continuous_y = (np.fromiter(map(f, list_x), dtype=float) for list_x in (listList_x + [continuous_x]))

    fig.suptitle(f"Study of the function y = {formula} on the interval ({xmin}, {xmax}) "
                 f"and of the error of some {side} Riemann sums compared to the exact value")

    areaAxes = (fig.add_subplot(len(list_n), 2, i) for i in range(1, 2 * (len(list_n)) + 1, 2))  #the left side of the figure

    for ax, list_x, list_y, width in zip(areaAxes, listList_x, listList_y, listWidth):
        ax.bar(list_x, list_y, align='edge', alpha=0.5, width=width,
               color=list("#70db70" if y >= 0 else "#ff6666" for y in list_y))
        ax.plot(continuous_x, continuous_y)
        if boolLogX: ax.set_xscale('symlog', linthresh=1e-30)
        if boolLogY: ax.set_yscale('symlog', linthresh=1e-30)
        ax.set_title(f"Visualization of the {side} Riemann sum with {len(list_x)} rectangles")
        ax.grid(True)

    exact, errorBound = quad(f, xmin, xmax)
    listDist = np.fromiter(((list_y.mean() * (xmax - xmin) - exact) for list_y in listList_y), dtype=float)

    accuracyAxes = [fig.add_subplot(2, 2, i) for i in (2, 4)]
    graphAccuracy(accuracyAxes, list_n, exact, errorBound, listDist)


def midpoint(fig, f, formula, xmin, xmax, boolLogX, boolLogY, list_n, lenContinuous):
    *listList_x, continuous_x = (np.linspace(xmin, xmax - (xmax - xmin) / n, n) + (xmax - xmin) / (2 * n) for n in list_n + [lenContinuous]) #This is the list of the middles
    listWidth = tuple((list_x[-1] - list_x[0]) / (len(list_x) - 1) for list_x in listList_x)
    *listList_y, continuous_y = (np.fromiter(map(f, list_x), dtype=float) for list_x in (listList_x + [continuous_x]))

    fig.suptitle(f"Study of the function y = {formula} on the interval ({xmin}, {xmax}) "
                 f"and of the error of some midpoint sums compared to the exact value")

    areaAxes = (fig.add_subplot(len(list_n), 2, i) for i in range(1, 2 * (len(list_n)) + 1, 2))  # the left side of the figure

    for ax, list_x, list_y, width in zip(areaAxes, listList_x, listList_y, listWidth):
        ax.bar(list_x, list_y, alpha=0.5, width=width,
               color=list("#70db70" if y >= 0 else "#ff6666" for y in list_y))
        ax.plot(continuous_x, continuous_y)
        if boolLogX: ax.set_xscale('symlog', linthresh=1e-30)
        if boolLogY: ax.set_yscale('symlog', linthresh=1e-30)
        ax.set_title(f"Visualization of the midpoint sum with {len(list_x)} rectangles")
        ax.grid(True)

    exact, errorBound = quad(f, xmin, xmax)
    listDist = np.fromiter(((list_y.mean() * (xmax - xmin) - exact) for list_y in listList_y), dtype=float)

    accuracyAxes = [fig.add_subplot(2, 2, i) for i in (2, 4)]
    graphAccuracy(accuracyAxes, list_n, exact, errorBound, listDist)


def trapezoidal(fig, f, formula, xmin, xmax, boolLogX, boolLogY, list_n, lenContinuous):
    *listList_x, continuous_x = (np.linspace(xmin, xmax, n + 1) for n in list_n + [lenContinuous])  # This is the list of the middles
    *listList_y, continuous_y = (np.fromiter(map(f, list_x), dtype=float) for list_x in (listList_x + [continuous_x]))

    fig.suptitle(f"Study of the function y = {formula} on the interval ({xmin}, {xmax}) "
                 f"and of the error of some trapezoidal sums compared to the exact value")

    areaAxes = (fig.add_subplot(len(list_n), 2, i) for i in range(1, 2 * (len(list_n)) + 1, 2))  # the left side of the figure

    for ax, list_x, list_y in zip(areaAxes, listList_x, listList_y):
        ax.plot(list_x, list_y, color='#8b008b', linestyle='--')
        ax.fill_between(list_x, list_y, color="#70db70", where=(list_y >= 0), alpha=0.5, interpolate=True)
        ax.fill_between(list_x, list_y, color="#ff6666", where=(list_y <= 0), alpha=0.5, interpolate=True)
        ax.plot(continuous_x, continuous_y)
        if boolLogX: ax.set_xscale('symlog', linthresh=1e-30)
        if boolLogY: ax.set_yscale('symlog', linthresh=1e-30)
        ax.set_title(f"Visualization of the trapezoidal sum with {len(list_x) - 1} trapezoids")
        ax.grid(True)

    exact, errorBound = quad(f, xmin, xmax)
    listDist = np.fromiter((((list_y.sum() - (list_y[0] + list_y[-1]) / 2) / (len(list_y) - 1) * (xmax - xmin) - exact) for list_y in listList_y), dtype=float)

    accuracyAxes = [fig.add_subplot(2, 2, i) for i in (2, 4)]
    graphAccuracy(accuracyAxes, list_n, exact, errorBound, listDist)


def main():
    formula = input("f(x) = ")
    f = lambda x: eval(formula)
    xmin, xmax = eval(input("Interval of integration, (xmin, xmax) = "))
    boolLogX = pyip.inputYesNo("Logarithmic x scale for graphing f(x) ? [y/n]", yesVal='y', noVal='n') == 'y'
    boolLogY = pyip.inputYesNo("Logarithmic y scale for graphing f(x) ? [y/n]", yesVal='y', noVal='n') == 'y'
    list_n = list(map(int, input("what number of intervals would you like to study ? use comma separated values, "
                                 "like \"10, 100, 1000, 10000\", spaces don't matter: ").split(',')))
    lenContinuous = 1000000  # 1000000 is very precise but can take some time to compute, but 10000 can be used fine,
    # it only matters for zooming in a lot. It's only used for visualization.

    dictMethod = {
        1: simpleRiemann,
        2: midpoint,
        3: trapezoidal
    }
    fig = plt.gcf()
    method = dictMethod[pyip.inputInt("What method would you like to use ? "
                                      "1 for basic Riemann sums, 2 for midpoint rule, 3 for trapezoidal rule: ", min=1, max=3)]
    method(fig, f, formula, xmin, xmax, boolLogX, boolLogY, list_n, lenContinuous)

    fig.subplots_adjust(left=0.05, bottom=0.05,right=0.95, top=0.9, wspace=0.1, hspace=0.6)
    plt.show()

if __name__ == '__main__':
    main()
