import matplotlib.pyplot as plt

def myplot(f, x):
    """
    :param f: function to plot
    :type f: callable
    :param x: values for x
    :type x: list or ndarray

    Plots the function f(x).
    """
    # yes, you can pass functions around as if
    # they were ordinary variables (they are)
    plt.plot(x, f(x))
    plt.xlabel("Eje $x$",fontsize=16)
    plt.ylabel("$f(x)$",fontsize=16)
    plt.title("Funcion $f(x)$")