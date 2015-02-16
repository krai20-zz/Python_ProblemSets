def evaluate_poly(poly, x):

    total = 0.0

    for i in range(len(poly)):
        total += poly[i] * (x ** i)

    return total




def compute_deriv(poly):
    """
    Computes and returns the derivative of a polynomial function. If the
    derivative is 0, returns (0.0,).

    Example:
    #>>> poly = (-13.39, 0.0, 17.5, 3.0, 1.0)    # x^4 + 3x^3 + 17.5x^2 - 13.39
    #>>> print compute_deriv(poly)        # 4x^3 + 9x^2 + 35^x
    (0.0, 35.0, 9.0, 4.0)

    poly: tuple of numbers, length > 0
    returns: tuple of numbers
    """
    derivative = ()

    for i in range(len(poly)):
        derivative += (i * poly[i],)

    return derivative




def compute_root(poly, x_0, epsilon):
    """
    Uses Newton's method to find and return a root of a polynomial function.
    Returns a tuple containing the root and the number of iterations required
    to get to the root.

    Example:
    >>> poly = (-13.39, 0.0, 17.5, 3.0, 1.0)    #x^4 + 3x^3 + 17.5x^2 - 13.39
    >>> x_0 = 0.1
    >>> epsilon = .0001
    >>> print compute_root(poly, x_0, epsilon)
    (0.80679075379635201, 8.0)

    poly: tuple of numbers, length > 1.
         Represents a polynomial function containing at least one real root.
         The derivative of this polynomial function at x_0 is not 0.
    x_0: float
    epsilon: float > 0
    returns: tuple (float, int)
    """
    # TO DO ...

    x = x_0
    count = 1

    while abs(evaluate_poly(poly, x)) >= epsilon:

        x -= evaluate_poly(poly, x)/evaluate_poly(compute_deriv(poly), x)

        count += 1

    return (x,) + (count,)


print compute_root((-13.39, 0.0, 17.5, 3.0, 1.0),0.1,0.0001)



