# visualizing-mathematics
This is a personnal repository under the MIT license containing all my programs that are related to data visualization, in particular with matplotlib and visualizing mathematical formulas or concepts. 

Every program (only one for now) in this repository that I plan on expanding, is to be used freely by people, mainly as a learning tool, either to learn a little more about python programming, or as a tool to visualize certain mathematical concepts.

The 60 lines below explain the point of the first program, Integral approximations visualizer.py, and how to use it, in case this wasn't clear enough when running it.

I have tried to make it comprehensive and detailed, so feel free to skim through it or not read it at all.

You can freely download the code to run it on your computer (just check the dependencies at the beginning of the code).
This program allows you to give a function on a certain interval, as well as other details if you want, you then choose different methods of approximations: Riemann sums, midpoint rule, trapezoidal rule, and more when I add them. It will then display a visualization/graph of how it approximates the area and a plot of the accuracy as the number of intervals increases.

### HOW TO USE THE PROGRAM

The code below is an example, feel free to skip the rest and come back to it only if you don't understand something.

```
How much customization do you want ? 0: stop, 1: minimum, 2: average, 3: advanced : 3
f(x) = x**4 - 3*x**3 - 12*x**2 + 20*x + 50*abs(sin(x/2))
Interval of integration: xmin, xmax = -3.5, 4.5
Logarithmic x scale for graphing f(x) ? [y/n]n
Logarithmic y scale for graphing f(x) ? [y/n]n
what number of intervals would you like to study ? use comma separated values, eg: 10, 100, 1000, 10000, spaces don't matter: 10, 100, 1000
Enter anything that evaluates to a regular python list of integers, such as [10, 100, 1000] or [3**i for i in range(2, 10)],
these will be added to the computations to display more points in the accuracy graphs:
[5**i for i in range(1, 7)]
How many values should be used to plot f(x) ? For graphing purposes only: 25000
What methods would you like to use ? all methods called will be executed one after the other, the results will be displayed at the end.
1 for Riemann sums, 2 for midpoint rule, 3 for trapezoidal rule: 1, 2, 3
How much customization do you want ? 0: stop, 1: minimum, 2: average, 3: advanced : 0

Process finished with exit code 0
```

Shows, after some computing:

![image 1](https://github.com/mateo713/visualizing-mathematics/blob/master/images/display_image_1.png)

![image 2](https://github.com/mateo713/visualizing-mathematics/blob/master/images/display_image_2.png)

![image 3](https://github.com/mateo713/visualizing-mathematics/blob/master/images/display_image_3.png)

Disclaimer: What is written here may sound obvious, but I still want to make it clear, just in case.
In order to perform some calculations, the code utilizes the eval function, which executes whatever code it is given. This allows the code to compute whatever function is given (or list comprehension for advanced customization), however it also means that you can execute any code with it, without any restriction: if you enter some code that deletes your file systems, the code will be executed. It is thus your responsability to not play with this in any other way than its intended use. Also note that there are no checks that are done regarding the memory consumption: if you enter values that make it require 60GB of RAM, it will try and access that much. So if you find the program long to perform and you have entered big numbers (usually in the millions, but it may happen in the 100000s), check your task manager (or whatever it is on your OS) and make sure this program isn't starting to use up several GB of RAM (1 or 2 is normal for medium sized numbers though). This can (and did) happen, and it is much better when it is prevented.

Now onto the actual program itself:
This program is an infinite loop so that you don't have to restart it everytime you want to restart.
You will be asked for 3 levels of customization, each adding more inputs and control over what is done.

Control level 1:
f(x) can be any function, but let's make this clearer: it should use pythonic syntax: +, -, \*, /, // (only the integer part), ** for exponentiation, % for modulus operator (the remainder of euclidian division), can access anything from the math module just by its name (like exp, e, sin and pi), and functions from numpy if you wanted (like np.exp and np.sin), as well (arguably) as definite integrals with quad from scipy.integrate (used with quad(function, start, end)), though it isn't always accurate (it isn't imported to be used here). The function shall not use any other variable than x. Here are a few examples: the polynomial f(x) = x\*\*3 + 10\*x\*\*2 – 3\*x + 148 is valid, and so is f(x) = exp(sqrt(tan(x))). You can find the list of functions available in the math module at https://docs.python.org/3/library/math.html .

The interval is as simple as it is. Just make sure not to enter anything that is not in the domain of the function (so -10, 10 is not going to do magic with f(x) = sqrt(x)).

At the end (if you have a higher control level, this will still be at the end), you will be asked for a list of the methods that should be computed. Enter them all at once, separated by commas, then they will all be computed and the graphs will be displayed at the end. Close them all (1 per method) to start all over.

Control level 2: 
This time you can choose to apply logarithmic scales to the x and/or y axes. Note that this uses matplotlib's symlog scale, which allows it to handle negative values in a way similar to -log(-x). The y scale works well with it (as would be expected), however, using the logarithmic x scale is a bit harder to make sense of, as then the intervals appear to have varying sizes, which depicts way less efficiently how well the function is approximated.

You also get to choose the list of number of intervals that should be computed and displayed. This defaults to \[10, 100, 1000] in order to not use a lot of memory, but you can change it as you want.
Note that big numbers take a long time to compute and use a lot of memory, as there are no tricks used to compute the values: it is literally creating a bunch of x values and uses f to compute a bunch of y values, and then displays them and computes the approximations with them. Note that you may enter a lot of values and it shouldn't get too compressed: they will always use only one half of the screen , but will divide themselves into several columns so that there isn't more than 5 rows.

Control level 3:
You get to create a python list (a regular list, not a numpy array or anything else) that contains numbers of intervals (like the previous prompt) except these won't be displayed, they'll just be added to the computations in order to display more points and thus, more accurate graphs.
You may use any syntax that evaluates to a python list, such exemples are:
\[5, 50, 500, 5000], 
 list(range(100, 10100, 100)), 
 \[5\*\*i for i in range(1, 8)], 
 Note that these can greatly lengthen the computations and use up more memory (as is to be expected)

Finally, you will be asked for a number of points. This defaults to 10000 at lower control levels and is the number of points that should be used to plot f(x): matplotlib graphs it by computing a certain amount of points and joining them together with straight lines. This input determines the number of said points. Note that anything above 10000 is only useful for zooming in, as otherwise there are many points per pixel.

### HOW TO UNDERSTAND THE OUTPUT

For each method, a figure (window) is created, that contains 2 sorts of graphs:
The first one is the graphs on the left half of the screen, one per number of intervals. Each of these shows the function, as well as how it (or its area) is approximated by the method used here. This allows for easy visualization of the efficiency of a method, as well as how it works internally.
Note that Riemann sums looks a bit busy because the left, right, and average of left and right sums are superposed, which leads to a rather unusual result. This is to help with the comparison, as having them stand alone is rather trivial, and is something that already exists out there.
The second part, takes up the right half of the screen and is made of 2 plots. These show how well the integral is approximated by the method, and how this changes with the number of intervals.
If you want to interpret these numbers (or make sure you're interpreting them correcty), here is what they mean:
Case 1: the integral is 0. You can't have a percentage of error, so instead it just tells you the value of the approximation, letting you judge whether that is a good approximation or not.
Case 2: the integral is not 0. This time, the numbers displayed are the percentage of error relative to the exact value: 0 means it is exact (up to inacurracies in the computing of the exact value), 100 means 100% too much, which is double the area (approximating at 200 when the exact value is 100), 1000 means approximating the integral as 11 times to big, etc.
negative values behave similarly, with -100 meaning an estimation of 0, -1000 an estimation of -9 times the exact value, ect. 
Another way of putting it is the percentage of over/under estimatition: +50 means 50% overestimate, 100 means double the estimate, -50 means a 50% underestimate. The extension of this concept for values under 100 does get weird, but that only reflects the estimation having the wrong sign.
If you prefer a formula, let E designate the exact integral, and A be the approximation of E. Then the values displayed are computed with result = 100 * (A-E) / E.

### KNOWN ISSUES

There is for now no way to deal with float overflows, which happens if |log10(value)|> 308.25. This should only cause problems with exponential and other fast growing functions. I may fix this at some point, but I haven't had the time to rewrite it all with the decimal module to fix this.

Behind the scenes, scipy.integrate.quad is used to get an exact value for the integral, along with an maximum error bound (a measure of accuracy).
You may get a warning from scipy, such as an Integration Warning. These usually mean (you can read them) that the integral that is computed is not a very "nice" integral, or a badly behaved function. This causes some accuracy issues, which means that estimates can be wildly off (you may also get a bunch of 0 values even for approximations that are visibly off, as errors less than the error bound default to 0).
There is for now no fix for this either, but I plan on doing something about it, probably by asking Wolfram Alpha for a better evaluation.

There may also be other issues from time to time. This can happen, currently this is just a beta version, as I want to add other methods that are both harder to understand/compute and other improvements and quality of life fixes.
