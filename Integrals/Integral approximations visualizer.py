import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches
from matplotlib.legend_handler import HandlerTuple
from scipy.integrate import quad
from math import *  #lets the user enter complicated functions easily, eg: exp(3*sin(x**2))
import pyinputplus as pyip # makes taking inputs more convenient for the user

# prevents a warning for calling ax.set_yscale("symlog", linthresh=ACERTAINVALUE) with linthresh where it is.
from warnings import filterwarnings
filterwarnings("ignore", category=__import__('matplotlib').cbook.mplDeprecation)


#This function is unique because it's the only one to graph many things on each axis, thus it is separate in order to not make special cases in the rest of the code
def Riemann(fig, formula, f, xmin, xmax, boolLogX, boolLogY, listGraph_n, listComp_n, lenContinuous):
    continuous_x = np.linspace(xmin, xmax, lenContinuous)
    continuous_y = f(continuous_x)
    interval = xmax - xmin
    listListGraph_xLeft = [np.linspace(xmin, xmax - (interval) / n, n) for n in listGraph_n]
    listListGraph_yLeft = [f(list_x) for list_x in listListGraph_xLeft]
    listListComp_xLeft = [np.linspace(xmin, xmax - (interval) / n, n) for n in listComp_n]
    listListComp_yLeft = [f(list_x) for list_x in listListComp_xLeft]
    listListGraph_xRight = [np.linspace(xmin + (interval) / n, xmax, n) for n in listGraph_n]
    listListGraph_yRight = [f(list_x) for list_x in listListGraph_xRight]
    listListComp_xRight = [np.linspace(xmin + (interval) / n, xmax, n) for n in listComp_n]
    listListComp_yRight = [f(list_x) for list_x in listListComp_xRight]
    listListGraph_x = [np.linspace(xmin, xmax - interval / n, n) + interval / (2 * n) for n in listGraph_n]
    listListGraph_y = [(list_yLeft + list_yRight) / 2 for list_yLeft, list_yRight in zip(listListGraph_yLeft, listListGraph_yRight)]
    listListComp_y = [(list_yLeft + list_yRight) / 2 for list_yLeft, list_yRight in zip(listListComp_yLeft, listListComp_yRight)]
    listWidth = [interval / n for n in listGraph_n]

    fig.suptitle(f"Study of the approximation of the integral of the function y = {formula} on the interval ({xmin}, {xmax}) "
                 f"by left and right Riemann sums and their average and of the quality of the approximations compared to the exact value")

    #This fills the left side of the figure, filling it row by row.
    nbCol = ceil(len(listGraph_n) / 5)
    areaAxes = [fig.add_subplot(ceil(len(listGraph_n) / nbCol), 2 * nbCol, i) for i in range(1, 2 * len(listGraph_n)) if 0 <= i % (2 * nbCol) - 1 < nbCol]

    for i, ax in enumerate(areaAxes):
        ax.bar(listListGraph_xLeft[i], listListGraph_yLeft[i], align='edge', alpha=0.5, width=listWidth[i], label="Left sum",
               color=list("#70db70" if y >= 0 else "#ff6666" for y in listListGraph_yLeft[i])) #green and red
        ax.bar(listListGraph_x[i], listListGraph_y[i], align='center', alpha=0.5, width=listWidth[i], label="Average of left and right sums",
               color=list("#071ba3" if y >= 0 else "#d8e30e" for y in listListGraph_y[i])) # blue and orange
        ax.bar(listListGraph_xRight[i], listListGraph_yRight[i], align='edge', alpha=0.5, width=-listWidth[i], label="Right sum",
               color=list("#6815a3" if y >= 0 else "#e08f0b" for y in listListGraph_yRight[i])) # purple and yellow
        ax.plot(continuous_x, continuous_y)
        if boolLogX:
            ax.set_xscale('symlog', linthreshy=0.9 * min(abs(xmin), abs(xmax)))
        if boolLogY:
            ax.set_yscale('symlog', linthreshy=absGetNonZeroMin(listListGraph_yLeft + listListComp_yLeft + listListGraph_yRight + listListComp_yRight))
        ax.set_title(f"{listGraph_n[i]} rectangles")
        ax.grid(True)

    #stuff for the legend to display both colors for each barplot. See last answer at
    #https://stackoverflow.com/questions/31478077/how-to-make-two-markers-share-the-same-label-in-the-legend-using-matplotlib
    #for explanation, by user rouckas
    legendpatches = ((patches.Patch(color=color1, alpha=0.5), patches.Patch(color=color2, alpha=0.5))
                     for color1, color2 in zip(("#70db70", "#071ba3", "#6815a3"), ("#ff6666", "#d8e30e", "#e08f0b")))
    areaAxes[0].legend((legendpatches), ("Left sum", "Average of left and right sums", "Right sum"), handler_map={tuple: HandlerTuple(ndivide=None)}, fontsize=10)

    exact, errorBound = quad(f, xmin, xmax)
    errorBounder = np.vectorize(lambda x: x if abs(x) > errorBound else 0)
    #the sorting here is to keep the implicit mapping between the lists of y values and the n values, which gets sorted later.
    listDistLeft = errorBounder(np.fromiter(((list_y.mean() * (interval) - exact) for list_y in sorted(listListGraph_yLeft + listListComp_yLeft, key=len)), dtype=float))
    listDistMid = errorBounder(np.fromiter(((list_y.mean() * (interval) - exact) for list_y in sorted(listListGraph_y + listListComp_y, key=len)), dtype=float))
    listDistRight = errorBounder(np.fromiter(((list_y.mean() * (interval) - exact) for list_y in sorted(listListGraph_yRight + listListComp_yRight, key=len)), dtype=float))

    accuracyAxes = [fig.add_subplot(2, 2, i) for i in (2, 4)]

    if 0 in listDistLeft + listDistRight + listDistMid:
        print(f"Some 0s are displayed in the accuracy check, however this does not mean necessarily mean the accuracy is perfect:\n"
              f"the exact value is computed with a certain margin of error, here it is {niceStr(errorBound)}\n"
              f"and any 0 displayed here means the inacurracy is less than this, and thus too small to be evaluated properly")
    if exact == 0:
        titles = ("difference for each approximation compared to the exact value of the integral, 0",
                  "difference for each approximation compared to the exact value of the integral, 0, on a logarithmic scale")
    else:
        listDistLeft, listDistMid, listDistRight = map(lambda x: x * (100 / exact), (listDistLeft, listDistMid, listDistRight))
        titles = (f"error percentage for each approximation compared to the exact integral: {niceStr(exact)}",
                  f"error percentage for each approximation compared to the exact integral: {niceStr(exact)}, on a logarithmic scale")

    #sorted to avoid lines going back and forth because it wouldn't be monotonically increasing.
    listTot_n = list(sorted(listGraph_n + listComp_n))
    ax = accuracyAxes[0]
    for listDist, color, label in zip((listDistLeft, listDistMid, listDistRight), ("#70db70", "#071ba3", "#6815a3"),
                                      ("Left sums", "Average of left and right sums", "Right sums")):
        ax.plot(listTot_n, listDist, color=color, label=label)
    for x, y in zip(listTot_n * 3, np.concatenate((listDistLeft, listDistMid, listDistRight))):
        ax.text(x, y, niceStr(y))
    ax.grid(True)
    ax.set_title(titles[0])
    ax.legend()

    ax = accuracyAxes[1]
    for listDist, color, label in zip((listDistLeft, listDistMid, listDistRight), ("#70db70", "#071ba3", "#6815a3"),
                                      ("Left sums", "Average of left and right sums", "Right sums")):
        ax.plot(listTot_n, listDist, color=color, label=label)
    ax.set_xscale("log")
    ax.get_xaxis().set_tick_params(which='minor', size=0)
    ax.get_xaxis().set_tick_params(which='minor', width=0)
    ax.set_yscale("symlog", linthreshy=absGetNonZeroMin(listDistLeft + listDistMid + listDistRight) * 0.9)
    good_ylim(ax, np.concatenate((listDistLeft, listDistMid, listDistRight)))  # sets the y limits to something a bit cleaner
    for x, y in zip(listTot_n * 3, np.concatenate((listDistLeft, listDistMid, listDistRight))):
        ax.text(x, y, niceStr(y))
    ax.set_title(titles[1])
    ax.grid(True, which='major')
    ax.legend()


class Midpoint:

    def __init__(self, f, xmin, xmax, listGraph_n, listComp_n):
        self.interval = xmax - xmin
        self.listListGraph_x = [np.linspace(xmin, xmax - self.interval / n, n) + self.interval / (2*n) for n in listGraph_n]
        self.listListGraph_y = [np.fromiter((f(x) for x in list_x), dtype=float) for list_x in self.listListGraph_x]
        self.listListComp_x = [np.linspace(xmin, xmax - self.interval / n, n) + self.interval / (2*n) for n in listComp_n]
        self.listListComp_y = [np.fromiter((f(x) for x in list_x), dtype=float) for list_x in self.listListComp_x]
        self.listWidth = [self.interval / n for n in listGraph_n]

    def titleSpecs(self): return "some midpoint sums"
    def listDist(self, exact):
        return np.fromiter(((list_y.mean() * (self.interval) - exact) for list_y in sorted(self.listListGraph_y + self.listListComp_y, key=len)), dtype=float)

    def graph(self, ax, i):
        ax.bar(self.listListGraph_x[i], self.listListGraph_y[i], alpha=0.5, width=self.listWidth[i],
               color=["#70db70" if y >= 0 else "#ff6666" for y in self.listListGraph_y[i]])


class Trapezoidal:

    def __init__(self, f, xmin, xmax, listGraph_n, listComp_n):
        self.interval = xmax - xmin
        self.listListGraph_x = [np.linspace(xmin, xmax, n + 1) for n in listGraph_n]
        self.listListGraph_y = [np.fromiter((f(x) for x in list_x), dtype=float) for list_x in self.listListGraph_x]
        self.listListComp_x = [np.linspace(xmin, xmax, n + 1) for n in listComp_n]
        self.listListComp_y = [np.fromiter((f(x) for x in list_x), dtype=float) for list_x in self.listListComp_x]
        self.listWidth = [self.interval / n for n in listGraph_n]

    def titleSpecs(self): return "some trapezoidal sums"
    def listDist(self, exact):
        return np.fromiter((((list_y.sum() - (list_y[0] + list_y[-1]) / 2) / (len(list_y) - 1) * (self.interval) - exact)
                            for list_y in sorted(self.listListGraph_y + self.listListComp_y, key=len)), dtype=float)

    def graph(self, ax, i):
        ax.plot(self.listListGraph_x[i], self.listListGraph_y[i], color='#8b008b', linestyle='--')
        ax.fill_between(self.listListGraph_x[i], self.listListGraph_y[i], alpha=0.5, interpolate=True,
                        color=["#70db70" if y >= 0 else "#ff6666" for y in self.listListGraph_y[i]])

def firstDigit(num):
    digits = '123456789'
    for char in str(num):
        if char in digits:
            return int(char)

def good_ylim(ax, values):  # symlog scale can give ugly limits for y values. This fixes that with a 0 and a power of 10 times a digit, like 9e-2.
    mini, maxi = min(values), max(values)
    newBottom, newTop = ax.get_ylim()
    if mini < 0 < maxi:
        newBottom = -(firstDigit(mini) + 1) * 10 ** floor(log10(-mini))
        newTop = (firstDigit(maxi) + 1) * 10 ** floor(log10(maxi))
    elif mini < maxi <= 0 :
        newBottom = -(firstDigit(mini) + 1) * 10 ** floor(log10(-mini))
        newTop = 0
    elif 0 <= mini < maxi:
        newBottom = 0
        newTop = (firstDigit(maxi) + 1) * 10 ** floor(log10(maxi))
    ax.set_ylim(newBottom, newTop)

def niceStr(val):   #gives a nice value, avoids having far too many digits display.
    if 100 < abs(val) < 1000000:   #just take away a few decimal digits
        return str(round(val, max(0, 6 - floor(log10(abs(val))))))
    #if it is in scientific notation, keep the scientific notation, just reduce the number of digits
    string = str(val)
    end = string.find('e')
    if end != -1:
        return string[:min(7, end)] + string[end:]
    else:
        return string[:min(7, len(string))]

def looper(func, check):  #for taking inputs: if there is an error, then ask for input again. Used on inputs that are quite error prone: listGraph_n and listComp_n.
    while True:
        try:
            list_ = func()
            if check(list_): #raises Exception if wrong
                return list_
        except Exception as e:
            print("An error occured, so you will be asked for that input again, it is probably a typo, but just in case it isn't, here is the error message", e, sep='\n')

def getvalue(variable):  #input taker
    global tier
    tuple = tiers[variable]
    if tier < tuple[0]: return eval(tuple[1])
    else: return eval(tuple[2])

def raiseEx(text): #to raise exceptions in lambda functions
    raise Exception(text)

def absGetNonZeroMin(values):  #returns the smallest non-zero value in the list, positive, used to set linthreshy on symlog scales, as it can't be 0
    if any(isinstance(elem, list) or isinstance(elem, np.ndarray) for elem in values): #if it's nested
        return absGetNonZeroMin(absGetNonZeroMin(arr) for arr in values)
    values = [abs(val) for val in values]
    if 0 not in values:
        return min(values)
    else:
        maxi = max(values)
        if maxi == 0:
            return 1 #default
        else:
            return min(values, key=lambda x: x if x != 0 else maxi)

def main():
    print("If you want to stop the program (which is an infinite loop), enter 0 as a level of customization and the program will terminate")
    while True:  #just a loop allowing to test many functions without quitting/restarting the program.
        global tier, tiers
        tier = pyip.inputInt("How much customization do you want ? 0: stop, 1: minimum, 2: average, 3: advanced : ", min=0, max=3)
        if tier == 0:
            break
        #concept: the first value is the default value, the second value is what is executed (with getvalue) to get the value.
        tiers = {"boologX": (2, 'False', """pyip.inputYesNo("Logarithmic x scale for graphing f(x) ? [y/n]", yesVal='y', noVal='n') == 'y'"""),
                 "boologY": (2, 'False', """pyip.inputYesNo("Logarithmic y scale for graphing f(x) ? [y/n]", yesVal='y', noVal='n') == 'y'"""),
                 "listGraph_n": (2, '[10, 100, 1000]', """list(map(int, input("what number of intervals would you like to study ? use comma separated values, "
                                                            "eg: 10, 100, 1000, 10000, spaces don't matter: ").split(',')))"""),
                 "listComp_n": (3, '[]',  #the + sign on the next line is for proper string formatting: indented code without indented string.
                                """input('''Enter anything that evaluates to a regular python list of integers, such as [10, 100, 1000] or [3**i for i in range(2, 10)],\n''' +
                                '''these will be added to the computations to display more points in the accuracy graphs:\n''')"""),
                 "lenContinuous": (3, '100000', """pyip.inputInt("How many values should be used to plot f(x) ? For graphing purposes only: ")""")}

        formula = input("f(x) = ")
        f = np.vectorize(lambda x: eval(formula))
        xmin, xmax = eval(input("Interval of integration: xmin, xmax = "))
        boolLogX = getvalue("boologX")
        boolLogY = getvalue("boologY")
        listGraph_n = looper(lambda: getvalue('listGraph_n'), lambda list_: True if isinstance(list_, list) and all(isinstance(x, int) for x in list_) else \
                                                                             raiseEx("It should evaluate to a list of integers"))
        listComp_n = [] if tier < 3 else looper(lambda : (eval(eval(tiers['listComp_n'][2]))),
                                                lambda list_: True if isinstance(list_, list) and all(isinstance(x, int) and x >= 1 for x in list_) else \
                                                raiseEx("It should evaluate to a list of integers all >= 1")) #the first eval gets the comprehension, the second eval computes it.
        #these 3 are used to graph the function.
        lenContinuous = getvalue("lenContinuous")
        continuous_x = np.linspace(xmin, xmax, lenContinuous)
        continuous_y = f(continuous_x)

        dictMethod = {
            1: Riemann,
            2: Midpoint,
            3: Trapezoidal
        }
        exact, errorBound = quad(f, xmin, xmax)
        errorBounder = np.vectorize(lambda x: x if abs(x) > errorBound else 0)
        exactMessage = False

        numbers = looper(lambda: list(map(int, input("What methods would you like to use ? all methods called will be executed one after the other, the results will be displayed "
                                                    "at the end." + '\n' + "1 for Riemann sums, 2 for midpoint rule, 3 for trapezoidal rule: ").split(','))),
                         lambda values: True if all(isinstance(val, int) and 1 <= val <= 3 for val in values) else raiseEx("These should all be integers between 1 and 3"))
        for number in numbers:

            fig = plt.figure()
            if number == 1: # this function is a unique case.
                Riemann(fig, formula, f, xmin, xmax, boolLogX, boolLogY, listGraph_n, listComp_n, lenContinuous)
                fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.9, wspace=0.1, hspace=0.6)
                plt.draw()
                continue
            method = dictMethod[number](f, xmin, xmax, listGraph_n, listComp_n)

            fig.suptitle(f"Study of the approximation of the function y = {formula} on the interval ({xmin}, {xmax}) "
                         f"with {method.titleSpecs()} and of the quality of the approximations compared to the exact value")

            nbCol = ceil(len(listGraph_n) / 5)
            areaAxes = (fig.add_subplot(ceil(len(listGraph_n) / nbCol), 2 * nbCol, i) for i in
                        range(1, 2 * len(listGraph_n)) if 0 <= i % (2 * nbCol) - 1 < nbCol)  # the left side of the figure, filled row by row.
            for i, ax in enumerate(areaAxes):
                method.graph(ax, i)
                ax.plot(continuous_x, continuous_y)
                if boolLogX:
                    ax.set_xscale('symlog', linthreshy=0.9 * min(abs(xmin), abs(xmax)))
                if boolLogY:
                    ax.set_yscale('symlog', linthreshy=absGetNonZeroMin(method.listListGraph_y + method.listListComp_y))
                ax.set_title(f"{listGraph_n[i]} intervals")
                ax.grid(True)

            listDist = method.listDist(exact)

            accuracyAxes = [fig.add_subplot(2, 2, i) for i in (2, 4)]
            listDist = errorBounder(listDist)
            if 0 in listDist:
                exactMessage = True
            if exact == 0:
                titles = ("difference for each approximation compared to the exact value of the integral, 0",
                          "difference for each approximation compared to the exact value of the integral, 0, on a logarithmic scale")
            else:
                listDist = listDist * (100 / exact)
                titles = (f"error percentage for each approximation compared to the exact integral: {niceStr(exact)}",
                          f"error percentage for each approximation compared to the exact integral: {niceStr(exact)}, on a logarithmic scale")

            #sorted for nicer graph: prevents line going back and forth by making it monotically increasing. The same sorting order is applied in each method
            listTot_n = list(sorted(listGraph_n + listComp_n))
            ax = accuracyAxes[0]
            ax.plot(listTot_n, listDist)
            for x, y in zip(listTot_n, listDist):
                ax.text(x, y, niceStr(y))
            ax.grid(True)
            ax.set_title(titles[0])

            ax = accuracyAxes[1]
            ax.plot(listTot_n, listDist)
            ax.set_xscale("log")
            ax.get_xaxis().set_tick_params(which='minor', size=0)
            ax.get_xaxis().set_tick_params(which='minor', width=0)
            ax.set_yscale("symlog", linthreshy=absGetNonZeroMin(listDist) * 0.9)
            good_ylim(ax, listDist)  # sets the y limits to something a bit cleaner
            for x, y in zip(listTot_n, listDist):
                ax.text(x, y, niceStr(y))
            ax.set_title(titles[1])
            ax.grid(True, which='major')

            fig.subplots_adjust(left=0.05, bottom=0.05,right=0.95, top=0.9, wspace=0.1, hspace=0.5)
            plt.draw()
        if exactMessage:
            print(f"Some 0s are displayed in the accuracy check, however this does not mean necessarily mean the accuracy is perfect:\n"
                  f"the exact value is computed with a certain margin of error, here it is {niceStr(errorBound)}\n"
                  f"and any 0 displayed here means the inacurracy is less than this, and thus too small to be evaluated properly")
        plt.show()

if __name__ == '__main__':
    main()
