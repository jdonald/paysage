
from cytoolz import compose
from math import sqrt
from collections import namedtuple

from .. import backends as be

Gradient = namedtuple("Gradient", [
    "layers",
    "weights"
])

"""
Utility functions for manipulating Gradient objects
"""

def grad_fold(func, grad):
    """
    Apply a function entrywise over a Gradient objet,
    combining the result.

    Args:
        func (callable): function with two arguments
        grad (Gradient)

    returns:
        float

    """
    result = 0
    for ly in grad.layers:
        result = be.fold(func, ly)
    for w in grad.weights:
        result = be.fold(func, w)
    return result

def grad_accumulate(func, grad):
    """
    Apply a funciton entrywise over a Gradient object,
    accumulating the result.

    Args:
        func (callable): function with one argument
        grad (Gradient)

    returns:
        float

    """
    result = 0
    for ly in grad.layers:
        result = be.accumulate(func, ly)
    for w in grad.weights:
        result = be.accumulate(func, w)
    return result

def grad_apply(func, grad):
    """
    Apply a function entrywise over a Gradient object.

    Args:
        func (callable)
        grad (Gradient)

    Returns:
        Gradient

    """
    return Gradient(
        [be.apply(func, ly) for ly in grad.layers],
        [be.apply(func, w) for w in grad.weights]
    )

def grad_apply_(func_, grad):
    """
    Apply a function entrywise over a Gradient object.

    Notes:
        Modifies elements of grad in place.

    Args:
        func_ (callable, in place operation)
        grad (Gradient)

    Returns:
        None

    """
    for ly in grad.layers:
        be.apply_(func_, ly)
    for w in grad.weights:
        be.apply_(func_, w)

def grad_mapzip(func, grad1, grad2):
    """
    Apply a function entrywise over the zip of two Gradient objects.

    Args:
        func_ (callable, in place operation)
        grad (Gradient)

    Returns:
        Gradient

    """
    n = len(grad1.layers)
    m = len(grad1.weights)
    return Gradient(
    [be.mapzip(func, grad1.layers[i], grad2.layers[i]) for i in range(n)],
    [be.mapzip(func, grad1.weights[i], grad2.weights[i]) for i in range(m)]
    )

def grad_mapzip_(func_, grad1, grad2):
    """
    Apply an in place function entrywise over the zip of two Gradient objects.

    Notes:
        Modifies elements of grad1 in place.

    Args:
        func_ (callable, in place operation)
        grad1 (Gradient)
        grad2 (Gradient)

    Returns:
        None

    """
    n = len(grad1.layers)
    m = len(grad1.weights)
    for i in range(n):
        be.mapzip_(func_, grad1.layers[i], grad2.layers[i])
    for j in range(m):
        be.mapzip_(func_, grad1.weights[j], grad2.weights[j])

def grad_magnitude(grad):
    """
    Compute the root-mean-square of the gradient.

    Args:
        grad (Gradient)

    Returns:
        magnitude (float)

    """
    n = len(grad.layers) + len(grad.weights)
    tensor_mean_square = compose(be.mean, be.square)
    return sqrt(grad_accumulate(tensor_mean_square, grad) / n)
