# Paysage

Paysage is library for machine learning with Boltzmann machines written in Python.
The library is still in the early stages, so new features will be added frequently.
Currently, paysage can be used to train:

* Bernoulli Restricted Boltzmann Machines (just a plain ol' RBM)
* Gaussian Restricted Boltzmann Machines
* Hopfield Models (an RBM with Gaussian hidden units)

Soon, we will be adding support for:

* Ising and Potts models (i.e., Markov Random Fields)
* Layer-by-layer training of Deep Boltzmann Machines
* Utilizing a GPU backend to speed up training

## Make Boltzmann machines great again!

* **Better performance through better algorithms**.
We are focused on making better Monte Carlo samplers, initialization methods,
and optimizers that allow you to train Boltzmann machines without emptying
your wallet for a new computer.
* **Stay close to Python**. Everybody loves Python, but sometimes it is too
slow to get the job done. We want to minimize the amount of computation that
gets shifted to the backend by targeting efforts for acceleration to the main
bottlenecks in training.


## Installation:
1. Clone the [git repo](https://github.com/drckf/paysage)
2. Move into the directory with setup.py
3. Run “pip install -e .”

Running the examples requires a file mnist.h5 containing the MNIST dataset
of handwritten images. The script `download_mnist.py` in the `mnist/` folder will
fetch the file from the web.

## System Dependencies

- hdf5, 1.8 required required by tables
- llvm, llvm-config required by scikit-learn

## About the name:
Boltzmann machines encode information in an
["energy landscape"](https://en.wikipedia.org/wiki/Energy_landscape) where
highly probable states have low energy and lowly probable states have high
energy. The name "landscape" was already taken, but the French
translation "paysage" was not.