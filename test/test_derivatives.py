from paysage import backends as be
from paysage import layers
from paysage.models import model

import pytest

def test_bernoulli_conditional_params():
    num_visible_units = 100
    num_hidden_units = 50
    batch_size = 25

    # set a seed for the random number generator
    be.set_seed()

    # set up some layer and model objects
    vis_layer = layers.BernoulliLayer(num_visible_units)
    hid_layer = layers.BernoulliLayer(num_hidden_units)
    rbm = model.Model([vis_layer, hid_layer])

    # randomly set the intrinsic model parameters
    a = be.randn((num_visible_units,))
    b = be.randn((num_hidden_units,))
    W = be.randn((num_visible_units, num_hidden_units))

    rbm.layers[0].params.loc[:] = a
    rbm.layers[1].params.loc[:] = b
    rbm.weights[0].params.matrix[:] = W

    # generate a random batch of data
    vdata = rbm.layers[0].random((batch_size, num_visible_units))
    hdata = rbm.layers[1].random((batch_size, num_hidden_units))

    # compute conditional parameters
    hidden_field = be.dot(vdata, W) # (batch_size, num_hidden_units)
    hidden_field += be.broadcast(b, hidden_field)

    visible_field = be.dot(hdata, be.transpose(W)) # (batch_size, num_visible_units)
    visible_field += be.broadcast(a, visible_field)

    # compute conditional parameters with layer funcitons
    hidden_field_layer = rbm.layers[1]._conditional_params(
        [vdata], [rbm.weights[0].W()])
    visible_field_layer = rbm.layers[0]._conditional_params(
        [hdata], [rbm.weights[0].W_T()])

    assert be.allclose(hidden_field, hidden_field_layer), \
    "hidden field wrong in bernoulli-bernoulli rbm"

    assert be.allclose(visible_field, visible_field_layer), \
    "visible field wrong in bernoulli-bernoulli rbm"


def test_bernoulli_derivatives():
    num_visible_units = 100
    num_hidden_units = 50
    batch_size = 25

    # set a seed for the random number generator
    be.set_seed()

    # set up some layer and model objects
    vis_layer = layers.BernoulliLayer(num_visible_units)
    hid_layer = layers.BernoulliLayer(num_hidden_units)
    rbm = model.Model([vis_layer, hid_layer])

    # randomly set the intrinsic model parameters
    a = be.randn((num_visible_units,))
    b = be.randn((num_hidden_units,))
    W = be.randn((num_visible_units, num_hidden_units))

    rbm.layers[0].params.loc[:] = a
    rbm.layers[1].params.loc[:] = b
    rbm.weights[0].params.matrix[:] = W

    # generate a random batch of data
    vdata = rbm.layers[0].random((batch_size, num_visible_units))
    vdata_scaled = rbm.layers[0].rescale(vdata)

    # compute the conditional mean of the hidden layer
    hid_mean = rbm.layers[1].conditional_mean([vdata], [rbm.weights[0].W()])
    hid_mean_scaled = rbm.layers[1].rescale(hid_mean)

    # compute the derivatives
    d_visible_loc = -be.mean(vdata, axis=0)
    d_hidden_loc = -be.mean(hid_mean_scaled, axis=0)
    d_W = -be.batch_outer(vdata, hid_mean_scaled) / len(vdata)

    # compute the derivatives using the layer functions
    vis_derivs = rbm.layers[0].derivatives(vdata, [hid_mean_scaled],
                                            [rbm.weights[0].W_T()])

    hid_derivs = rbm.layers[1].derivatives(hid_mean, [vdata_scaled],
                                          [rbm.weights[0].W()])

    weight_derivs = rbm.weights[0].derivatives(vdata, hid_mean_scaled)

    assert be.allclose(d_visible_loc, vis_derivs.loc), \
    "derivative of visible loc wrong in bernoulli-bernoulli rbm"

    assert be.allclose(d_hidden_loc, hid_derivs.loc), \
    "derivative of hidden loc wrong in bernoulli-bernoulli rbm"

    assert be.allclose(d_W, weight_derivs.matrix), \
    "derivative of weights wrong in bernoulli-bernoulli rbm"


def test_ising_conditional_params():
    num_visible_units = 100
    num_hidden_units = 50
    batch_size = 25

    # set a seed for the random number generator
    be.set_seed()

    # set up some layer and model objects
    vis_layer = layers.IsingLayer(num_visible_units)
    hid_layer = layers.IsingLayer(num_hidden_units)
    rbm = model.Model([vis_layer, hid_layer])

    # randomly set the intrinsic model parameters
    a = be.randn((num_visible_units,))
    b = be.randn((num_hidden_units,))
    W = be.randn((num_visible_units, num_hidden_units))

    rbm.layers[0].params.loc[:] = a
    rbm.layers[1].params.loc[:] = b
    rbm.weights[0].params.matrix[:] = W

    # generate a random batch of data
    vdata = rbm.layers[0].random((batch_size, num_visible_units))
    hdata = rbm.layers[1].random((batch_size, num_hidden_units))

    # compute conditional parameters
    hidden_field = be.dot(vdata, W) # (batch_size, num_hidden_units)
    hidden_field += be.broadcast(b, hidden_field)

    visible_field = be.dot(hdata, be.transpose(W)) # (batch_size, num_visible_units)
    visible_field += be.broadcast(a, visible_field)

    # compute the conditional parameters using the layer functions
    hidden_field_func = rbm.layers[1]._conditional_params(
        [vdata], [rbm.weights[0].W()])
    visible_field_func = rbm.layers[0]._conditional_params(
        [hdata], [rbm.weights[0].W_T()])

    assert be.allclose(hidden_field, hidden_field_func), \
    "hidden field wrong in ising-ising rbm"

    assert be.allclose(visible_field, visible_field_func), \
    "visible field wrong in ising-ising rbm"


def test_ising_derivatives():
    num_visible_units = 100
    num_hidden_units = 50
    batch_size = 25

    # set a seed for the random number generator
    be.set_seed()

    # set up some layer and model objects
    vis_layer = layers.IsingLayer(num_visible_units)
    hid_layer = layers.IsingLayer(num_hidden_units)
    rbm = model.Model([vis_layer, hid_layer])

    # randomly set the intrinsic model parameters
    a = be.randn((num_visible_units,))
    b = be.randn((num_hidden_units,))
    W = be.randn((num_visible_units, num_hidden_units))

    rbm.layers[0].params.loc[:] = a
    rbm.layers[1].params.loc[:] = b
    rbm.weights[0].params.matrix[:] = W

    # generate a random batch of data
    vdata = rbm.layers[0].random((batch_size, num_visible_units))
    vdata_scaled = rbm.layers[0].rescale(vdata)

    # compute the mean of the hidden layer
    hid_mean = rbm.layers[1].conditional_mean([vdata], [rbm.weights[0].W()])
    hid_mean_scaled = rbm.layers[1].rescale(hid_mean)

    # compute the derivatives
    d_visible_loc = -be.mean(vdata, axis=0)
    d_hidden_loc = -be.mean(hid_mean_scaled, axis=0)
    d_W = -be.batch_outer(vdata, hid_mean_scaled) / len(vdata)

    # compute the derivatives using the layer functions
    vis_derivs = rbm.layers[0].derivatives(vdata, [hid_mean_scaled],
                                            [rbm.weights[0].W_T()]
                                            )

    hid_derivs = rbm.layers[1].derivatives(hid_mean, [vdata_scaled],
                                           [rbm.weights[0].W()]
                                           )

    weight_derivs = rbm.weights[0].derivatives(vdata, hid_mean_scaled)

    assert be.allclose(d_visible_loc, vis_derivs.loc), \
    "derivative of visible loc wrong in ising-ising rbm"

    assert be.allclose(d_hidden_loc, hid_derivs.loc), \
    "derivative of hidden loc wrong in ising-ising rbm"

    assert be.allclose(d_W, weight_derivs.matrix), \
    "derivative of weights wrong in ising-ising rbm"


def test_exponential_conditional_params():
    num_visible_units = 100
    num_hidden_units = 50
    batch_size = 25

    # set a seed for the random number generator
    be.set_seed()

    # set up some layer and model objects
    vis_layer = layers.ExponentialLayer(num_visible_units)
    hid_layer = layers.ExponentialLayer(num_hidden_units)
    rbm = model.Model([vis_layer, hid_layer])

    # randomly set the intrinsic model parameters
    # for the exponential layers, we need a > 0, b > 0, and W < 0
    a = be.rand((num_visible_units,))
    b = be.rand((num_hidden_units,))
    W = -be.rand((num_visible_units, num_hidden_units))

    rbm.layers[0].params.loc[:] = a
    rbm.layers[1].params.loc[:] = b
    rbm.weights[0].params.matrix[:] = W

    # generate a random batch of data
    vdata = rbm.layers[0].random((batch_size, num_visible_units))
    hdata = rbm.layers[1].random((batch_size, num_hidden_units))

    # compute conditional parameters
    hidden_rate = -be.dot(vdata, W) # (batch_size, num_hidden_units)
    hidden_rate += be.broadcast(b, hidden_rate)

    visible_rate = -be.dot(hdata, be.transpose(W)) # (batch_size, num_visible_units)
    visible_rate += be.broadcast(a, visible_rate)

    # compute the conditional parameters using the layer functions
    hidden_rate_func = rbm.layers[1]._conditional_params(
        [vdata], [rbm.weights[0].W()])
    visible_rate_func = rbm.layers[0]._conditional_params(
        [hdata], [rbm.weights[0].W_T()])

    assert be.allclose(hidden_rate, hidden_rate_func), \
    "hidden rate wrong in exponential-exponential rbm"

    assert be.allclose(visible_rate, visible_rate_func), \
    "visible rate wrong in exponential-exponential rbm"


def test_exponential_derivatives():
    num_visible_units = 100
    num_hidden_units = 50
    batch_size = 25

    # set a seed for the random number generator
    be.set_seed()

    # set up some layer and model objects
    vis_layer = layers.ExponentialLayer(num_visible_units)
    hid_layer = layers.ExponentialLayer(num_hidden_units)
    rbm = model.Model([vis_layer, hid_layer])

    # randomly set the intrinsic model parameters
    # for the exponential layers, we need a > 0, b > 0, and W < 0
    a = be.rand((num_visible_units,))
    b = be.rand((num_hidden_units,))
    W = -be.rand((num_visible_units, num_hidden_units))

    rbm.layers[0].params.loc[:] = a
    rbm.layers[1].params.loc[:] = b
    rbm.weights[0].params.matrix[:] = W

    # generate a random batch of data
    vdata = rbm.layers[0].random((batch_size, num_visible_units))
    vdata_scaled = rbm.layers[0].rescale(vdata)

    # compute the mean of the hidden layer
    hid_mean = rbm.layers[1].conditional_mean([vdata], [rbm.weights[0].W()])
    hid_mean_scaled = rbm.layers[1].rescale(hid_mean)

    # compute the derivatives
    d_visible_loc = be.mean(vdata, axis=0)
    d_hidden_loc = be.mean(hid_mean_scaled, axis=0)
    d_W = -be.batch_outer(vdata, hid_mean_scaled) / len(vdata)

    # compute the derivatives using the layer functions
    vis_derivs = rbm.layers[0].derivatives(vdata, [hid_mean_scaled],
                                            [rbm.weights[0].W_T()])

    hid_derivs = rbm.layers[1].derivatives(hid_mean, [vdata_scaled],
                                               [rbm.weights[0].W()])

    weight_derivs = rbm.weights[0].derivatives(vdata, hid_mean_scaled)

    assert be.allclose(d_visible_loc, vis_derivs.loc), \
    "derivative of visible loc wrong in exponential-exponential rbm"

    assert be.allclose(d_hidden_loc, hid_derivs.loc), \
    "derivative of hidden loc wrong in exponential-exponential rbm"

    assert be.allclose(d_W, weight_derivs.matrix), \
    "derivative of weights wrong in exponential-exponential rbm"


def test_gaussian_conditional_params():
    num_visible_units = 100
    num_hidden_units = 50
    batch_size = 25

    # set a seed for the random number generator
    be.set_seed()

    # set up some layer and model objects
    vis_layer = layers.GaussianLayer(num_visible_units)
    hid_layer = layers.GaussianLayer(num_hidden_units)
    rbm = model.Model([vis_layer, hid_layer])

    # randomly set the intrinsic model parameters
    a = be.randn((num_visible_units,))
    b = be.randn((num_hidden_units,))
    log_var_a = 0.1 * be.randn((num_visible_units,))
    log_var_b = 0.1 * be.randn((num_hidden_units,))
    W = be.randn((num_visible_units, num_hidden_units))

    rbm.layers[0].params.loc[:] = a
    rbm.layers[1].params.loc[:] = b
    rbm.layers[0].params.log_var[:] = log_var_a
    rbm.layers[1].params.log_var[:] = log_var_b
    rbm.weights[0].params.matrix[:] = W

    # generate a random batch of data
    vdata = rbm.layers[0].random((batch_size, num_visible_units))
    hdata = rbm.layers[1].random((batch_size, num_hidden_units))

    # compute the variance
    visible_var = be.exp(log_var_a)
    hidden_var = be.exp(log_var_b)

    # rescale the data
    vdata_scaled = vdata / be.broadcast(visible_var, vdata)
    hdata_scaled = hdata / be.broadcast(hidden_var, hdata)

    # test rescale
    assert be.allclose(vdata_scaled, rbm.layers[0].rescale(vdata)),\
    "visible rescale wrong in gaussian-gaussian rbm"

    assert be.allclose(hdata_scaled, rbm.layers[1].rescale(hdata)),\
    "hidden rescale wrong in gaussian-gaussian rbm"

    # compute the mean
    hidden_mean = be.dot(vdata_scaled, W) # (batch_size, num_hidden_units)
    hidden_mean += be.broadcast(b, hidden_mean)

    visible_mean = be.dot(hdata_scaled, be.transpose(W)) # (batch_size, num_hidden_units)
    visible_mean += be.broadcast(a, visible_mean)

    # update the conditional parameters using the layer functions
    vis_mean_func, vis_var_func = rbm.layers[0]._conditional_params(
        [hdata_scaled], [rbm.weights[0].W_T()])
    hid_mean_func, hid_var_func = rbm.layers[1]._conditional_params(
        [vdata_scaled], [rbm.weights[0].W()])

    assert be.allclose(visible_var, vis_var_func),\
    "visible variance wrong in gaussian-gaussian rbm"

    assert be.allclose(hidden_var, hid_var_func),\
    "hidden variance wrong in gaussian-gaussian rbm"

    assert be.allclose(visible_mean, vis_mean_func),\
    "visible mean wrong in gaussian-gaussian rbm"

    assert be.allclose(hidden_mean, hid_mean_func),\
    "hidden mean wrong in gaussian-gaussian rbm"


def test_gaussian_derivatives():
    num_visible_units = 100
    num_hidden_units = 50
    batch_size = 25

    # set a seed for the random number generator
    be.set_seed()

    # set up some layer and model objects
    vis_layer = layers.GaussianLayer(num_visible_units)
    hid_layer = layers.GaussianLayer(num_hidden_units)
    rbm = model.Model([vis_layer, hid_layer])

    # randomly set the intrinsic model parameters
    a = be.randn((num_visible_units,))
    b = be.randn((num_hidden_units,))
    log_var_a = 0.1 * be.randn((num_visible_units,))
    log_var_b = 0.1 * be.randn((num_hidden_units,))
    W = be.randn((num_visible_units, num_hidden_units))

    rbm.layers[0].params.loc[:] = a
    rbm.layers[1].params.loc[:] = b
    rbm.layers[0].params.log_var[:] = log_var_a
    rbm.layers[1].params.log_var[:] = log_var_b
    rbm.weights[0].params.matrix[:] = W

    # generate a random batch of data
    vdata = rbm.layers[0].random((batch_size, num_visible_units))
    visible_var = be.exp(log_var_a)
    vdata_scaled = vdata / be.broadcast(visible_var, vdata)

    # compute the mean of the hidden layer
    hid_mean = rbm.layers[1].conditional_mean(
        [vdata_scaled], [rbm.weights[0].W()])
    hidden_var = be.exp(log_var_b)
    hid_mean_scaled = rbm.layers[1].rescale(hid_mean)

    # compute the derivatives
    d_vis_loc = -be.mean(vdata_scaled, axis=0)
    d_vis_logvar = -0.5 * be.mean(be.square(be.subtract(a, vdata)), axis=0)
    d_vis_logvar += be.batch_dot(hid_mean_scaled, be.transpose(W), vdata,
                                 axis=0) / len(vdata)
    d_vis_logvar /= visible_var

    d_hid_loc = -be.mean(hid_mean_scaled, axis=0)

    d_hid_logvar = -0.5 * be.mean(be.square(hid_mean - be.broadcast(b, hid_mean)), axis=0)
    d_hid_logvar += be.batch_dot(vdata_scaled, W, hid_mean,
                                 axis=0) / len(hid_mean)
    d_hid_logvar /= hidden_var

    d_W = -be.batch_outer(vdata_scaled, hid_mean_scaled) / len(vdata_scaled)

    # compute the derivatives using the layer functions
    vis_derivs = rbm.layers[0].derivatives(vdata, [hid_mean_scaled],
                                            [rbm.weights[0].W_T()])

    hid_derivs = rbm.layers[1].derivatives(hid_mean, [vdata_scaled],
                                           [rbm.weights[0].W()])

    weight_derivs = rbm.weights[0].derivatives(vdata_scaled, hid_mean_scaled)

    assert be.allclose(d_vis_loc, vis_derivs.loc), \
    "derivative of visible loc wrong in gaussian-gaussian rbm"

    assert be.allclose(d_hid_loc, hid_derivs.loc), \
    "derivative of hidden loc wrong in gaussian-gaussian rbm"

    assert be.allclose(d_vis_logvar, vis_derivs.log_var, rtol=1e-05, atol=1e-01), \
    "derivative of visible log_var wrong in gaussian-gaussian rbm"

    assert be.allclose(d_hid_logvar, hid_derivs.log_var, rtol=1e-05, atol=1e-01), \
    "derivative of hidden log_var wrong in gaussian-gaussian rbm"

    assert be.allclose(d_W, weight_derivs.matrix), \
    "derivative of weights wrong in gaussian-gaussian rbm"


if __name__ == "__main__":
    pytest.main([__file__])
