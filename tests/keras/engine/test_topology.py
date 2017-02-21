import pytest
import json
import numpy as np

from keras.layers import Dense, Dropout, InputLayer
from keras import layers
from keras.engine import Input, get_source_inputs
from keras.models import Model, Sequential
from keras import backend as K
from keras.models import model_from_json, model_from_yaml
from keras.utils.test_utils import keras_test


@keras_test
def test_get_updates_for():
    a = Input(shape=(2,))
    dense_layer = Dense(1)
    dense_layer.add_update(0, inputs=a)
    dense_layer.add_update(1, inputs=None)

    assert dense_layer.get_updates_for(a) == [0]
    assert dense_layer.get_updates_for(None) == [1]


@keras_test
def test_get_losses_for():
    a = Input(shape=(2,))
    dense_layer = Dense(1)
    dense_layer.add_loss(0, inputs=a)
    dense_layer.add_loss(1, inputs=None)

    assert dense_layer.get_losses_for(a) == [0]
    assert dense_layer.get_losses_for(None) == [1]


@keras_test
def test_trainable_weights():
    a = Input(shape=(2,))
    b = Dense(1)(a)
    model = Model(a, b)

    weights = model.weights
    assert model.trainable_weights == weights
    assert model.non_trainable_weights == []

    model.trainable = False
    assert model.trainable_weights == []
    assert model.non_trainable_weights == weights

    model.trainable = True
    assert model.trainable_weights == weights
    assert model.non_trainable_weights == []

    model.layers[1].trainable = False
    assert model.trainable_weights == []
    assert model.non_trainable_weights == weights

    # sequential model
    model = Sequential()
    model.add(Dense(1, input_dim=2))
    weights = model.weights

    assert model.trainable_weights == weights
    assert model.non_trainable_weights == []

    model.trainable = False
    assert model.trainable_weights == []
    assert model.non_trainable_weights == weights

    model.trainable = True
    assert model.trainable_weights == weights
    assert model.non_trainable_weights == []

    model.layers[0].trainable = False
    assert model.trainable_weights == []
    assert model.non_trainable_weights == weights


@keras_test
def test_learning_phase():
    a = Input(shape=(32,), name='input_a')
    b = Input(shape=(32,), name='input_b')

    a_2 = Dense(16, name='dense_1')(a)
    dp = Dropout(0.5, name='dropout')
    b_2 = dp(b)

    assert not a_2._uses_learning_phase
    assert b_2._uses_learning_phase

    # test merge
    m = layers.concatenate([a_2, b_2])
    assert m._uses_learning_phase

    # Test recursion
    model = Model([a, b], [a_2, b_2])
    print(model.input_spec)
    assert model.uses_learning_phase

    c = Input(shape=(32,), name='input_c')
    d = Input(shape=(32,), name='input_d')

    c_2, b_2 = model([c, d])
    assert c_2._uses_learning_phase
    assert b_2._uses_learning_phase

    # try actually running graph
    fn = K.function(model.inputs + [K.learning_phase()], model.outputs)
    input_a_np = np.random.random((10, 32))
    input_b_np = np.random.random((10, 32))
    fn_outputs_no_dp = fn([input_a_np, input_b_np, 0])
    fn_outputs_dp = fn([input_a_np, input_b_np, 1])
    # output a: nothing changes
    assert fn_outputs_no_dp[0].sum() == fn_outputs_dp[0].sum()
    # output b: dropout applied
    assert fn_outputs_no_dp[1].sum() != fn_outputs_dp[1].sum()


@keras_test
def test_layer_call_arguments():
    # Test the ability to pass and serialize arguments to `call`.
    inp = layers.Input(shape=(2,))
    x = layers.Dense(3)(inp)
    x = layers.Dropout(0.5)(x, training=True)
    model = Model(inp, x)
    assert not model.uses_learning_phase

    # Test that argument is kept when applying the model
    inp2 = layers.Input(shape=(2,))
    out2 = model(inp2)
    assert not out2._uses_learning_phase

    # Test that argument is kept after loading a model
    config = model.get_config()
    model = Model.from_config(config)
    assert not model.uses_learning_phase


@keras_test
def test_node_construction():
    ####################################################
    # test basics

    a = Input(shape=(32,), name='input_a')
    b = Input(shape=(32,), name='input_b')

    assert a._keras_shape == (None, 32)
    a_layer, a_node_index, a_tensor_index = a._keras_history
    b_layer, b_node_index, b_tensor_index = b._keras_history
    assert len(a_layer.inbound_nodes) == 1
    assert a_tensor_index is 0
    node = a_layer.inbound_nodes[a_node_index]
    assert node.outbound_layer == a_layer

    assert type(node.inbound_layers) is list
    assert node.inbound_layers == []
    assert type(node.input_tensors) is list
    assert node.input_tensors == [a]
    assert type(node.input_masks) is list
    assert node.input_masks == [None]
    assert type(node.input_shapes) is list
    assert node.input_shapes == [(None, 32)]

    assert type(node.output_tensors) is list
    assert node.output_tensors == [a]
    assert type(node.output_shapes) is list
    assert node.output_shapes == [(None, 32)]
    assert type(node.output_masks) is list
    assert node.output_masks == [None]

    dense = Dense(16, name='dense_1')
    a_2 = dense(a)
    b_2 = dense(b)

    assert len(dense.inbound_nodes) == 2
    assert len(dense.outbound_nodes) == 0
    assert dense.inbound_nodes[0].inbound_layers == [a_layer]
    assert dense.inbound_nodes[0].outbound_layer == dense
    assert dense.inbound_nodes[1].inbound_layers == [b_layer]
    assert dense.inbound_nodes[1].outbound_layer == dense

    assert dense.inbound_nodes[0].input_tensors == [a]
    assert dense.inbound_nodes[1].input_tensors == [b]

    # test layer properties
    test_layer = Dense(16, name='test_layer')
    a_test = test_layer(a)
    assert K.int_shape(test_layer.kernel) == (32, 16)
    assert test_layer.input == a
    assert test_layer.output == a_test
    assert test_layer.input_mask is None
    assert test_layer.output_mask is None
    assert test_layer.input_shape == (None, 32)
    assert test_layer.output_shape == (None, 16)

    with pytest.raises(Exception):
        dense.input
    with pytest.raises(Exception):
        dense.output
    with pytest.raises(Exception):
        dense.input_mask
    with pytest.raises(Exception):
        dense.output_mask

    assert dense.get_input_at(0) == a
    assert dense.get_input_at(1) == b
    assert dense.get_output_at(0) == a_2
    assert dense.get_output_at(1) == b_2
    assert dense.get_input_shape_at(0) == (None, 32)
    assert dense.get_input_shape_at(1) == (None, 32)
    assert dense.get_output_shape_at(0) == (None, 16)
    assert dense.get_output_shape_at(1) == (None, 16)
    assert dense.get_input_mask_at(0) is None
    assert dense.get_input_mask_at(1) is None
    assert dense.get_output_mask_at(0) is None
    assert dense.get_output_mask_at(1) is None


@keras_test
def test_multi_input_layer():
    ####################################################
    # test multi-input layer
    a = Input(shape=(32,), name='input_a')
    b = Input(shape=(32,), name='input_b')

    dense = Dense(16, name='dense_1')
    a_2 = dense(a)
    b_2 = dense(b)

    merged = layers.concatenate([a_2, b_2], name='merge')
    assert merged._keras_shape == (None, 16 * 2)
    merge_layer, merge_node_index, merge_tensor_index = merged._keras_history

    assert merge_node_index == 0
    assert merge_tensor_index == 0

    assert len(merge_layer.inbound_nodes) == 1
    assert len(merge_layer.outbound_nodes) == 0

    assert len(merge_layer.inbound_nodes[0].input_tensors) == 2
    assert len(merge_layer.inbound_nodes[0].inbound_layers) == 2

    c = Dense(64, name='dense_2')(merged)
    d = Dense(5, name='dense_3')(c)

    model = Model(inputs=[a, b], outputs=[c, d], name='model')
    assert len(model.layers) == 6
    print('model.input_layers:', model.input_layers)
    print('model.input_layers_node_indices:', model.input_layers_node_indices)
    print('model.input_layers_tensor_indices:', model.input_layers_tensor_indices)
    print('model.output_layers', model.output_layers)

    print('output_shape:', model.compute_output_shape([(None, 32), (None, 32)]))
    assert model.compute_output_shape([(None, 32), (None, 32)]) == [(None, 64), (None, 5)]

    print('mask:', model.compute_mask([a, b], [None, None]))
    assert model.compute_mask([a, b], [None, None]) == [None, None]

    print('output_shape:', model.compute_output_shape([(None, 32), (None, 32)]))
    assert model.compute_output_shape([(None, 32), (None, 32)]) == [(None, 64), (None, 5)]

    # we don't check names of first 2 layers (inputs) because
    # ordering of same-level layers is not fixed
    print('layers:', [layer.name for layer in model.layers])
    assert [l.name for l in model.layers][2:] == ['dense_1', 'merge', 'dense_2', 'dense_3']
    print('input_layers:', [l.name for l in model.input_layers])
    assert [l.name for l in model.input_layers] == ['input_a', 'input_b']
    print('output_layers:', [l.name for l in model.output_layers])
    assert [l.name for l in model.output_layers] == ['dense_2', 'dense_3']

    # actually run model
    fn = K.function(model.inputs, model.outputs)
    input_a_np = np.random.random((10, 32))
    input_b_np = np.random.random((10, 32))
    fn_outputs = fn([input_a_np, input_b_np])
    assert [x.shape for x in fn_outputs] == [(10, 64), (10, 5)]

    # test get_source_inputs
    print(get_source_inputs(c))
    assert get_source_inputs(c) == [a, b]

    # serialization / deserialization
    json_config = model.to_json()
    recreated_model = model_from_json(json_config)
    recreated_model.compile('rmsprop', 'mse')

    print('recreated:')
    print([layer.name for layer in recreated_model.layers])
    print([layer.name for layer in recreated_model.input_layers])
    print([layer.name for layer in recreated_model.output_layers])
    assert [l.name for l in recreated_model.layers][2:] == ['dense_1', 'merge', 'dense_2', 'dense_3']
    assert [l.name for l in recreated_model.input_layers] == ['input_a', 'input_b']
    assert [l.name for l in recreated_model.output_layers] == ['dense_2', 'dense_3']

    fn = K.function(recreated_model.inputs, recreated_model.outputs)
    input_a_np = np.random.random((10, 32))
    input_b_np = np.random.random((10, 32))
    fn_outputs = fn([input_a_np, input_b_np])
    assert [x.shape for x in fn_outputs] == [(10, 64), (10, 5)]


@keras_test
def test_recursion():
    ####################################################
    # test recursion

    a = Input(shape=(32,), name='input_a')
    b = Input(shape=(32,), name='input_b')

    dense = Dense(16, name='dense_1')
    a_2 = dense(a)
    b_2 = dense(b)
    merged = layers.concatenate([a_2, b_2], name='merge')
    c = Dense(64, name='dense_2')(merged)
    d = Dense(5, name='dense_3')(c)

    model = Model(inputs=[a, b], outputs=[c, d], name='model')

    e = Input(shape=(32,), name='input_e')
    f = Input(shape=(32,), name='input_f')
    g, h = model([e, f])

    # g2, h2 = model([e, f])

    assert g._keras_shape == c._keras_shape
    assert h._keras_shape == d._keras_shape

    # test separate manipulation of different layer outputs
    i = Dense(7, name='dense_4')(h)

    final_model = Model(inputs=[e, f], outputs=[i, g], name='final')
    assert len(final_model.inputs) == 2
    assert len(final_model.outputs) == 2
    assert len(final_model.layers) == 4

    # we don't check names of first 2 layers (inputs) because
    # ordering of same-level layers is not fixed
    print('final_model layers:', [layer.name for layer in final_model.layers])
    assert [layer.name for layer in final_model.layers][2:] == ['model', 'dense_4']

    print(model.compute_mask([e, f], [None, None]))
    assert model.compute_mask([e, f], [None, None]) == [None, None]

    print(final_model.compute_output_shape([(10, 32), (10, 32)]))
    assert final_model.compute_output_shape([(10, 32), (10, 32)]) == [(10, 7), (10, 64)]

    # run recursive model
    fn = K.function(final_model.inputs, final_model.outputs)
    input_a_np = np.random.random((10, 32))
    input_b_np = np.random.random((10, 32))
    fn_outputs = fn([input_a_np, input_b_np])
    assert [x.shape for x in fn_outputs] == [(10, 7), (10, 64)]

    # test serialization
    model_config = final_model.get_config()
    print(json.dumps(model_config, indent=4))
    recreated_model = Model.from_config(model_config)

    fn = K.function(recreated_model.inputs, recreated_model.outputs)
    input_a_np = np.random.random((10, 32))
    input_b_np = np.random.random((10, 32))
    fn_outputs = fn([input_a_np, input_b_np])
    assert [x.shape for x in fn_outputs] == [(10, 7), (10, 64)]

    ####################################################
    # test multi-input multi-output

    j = Input(shape=(32,), name='input_j')
    k = Input(shape=(32,), name='input_k')
    m, n = model([j, k])

    o = Input(shape=(32,), name='input_o')
    p = Input(shape=(32,), name='input_p')
    q, r = model([o, p])

    assert n._keras_shape == (None, 5)
    assert q._keras_shape == (None, 64)
    s = layers.concatenate([n, q], name='merge_nq')
    assert s._keras_shape == (None, 64 + 5)

    # test with single output as 1-elem list
    multi_io_model = Model([j, k, o, p], [s])

    fn = K.function(multi_io_model.inputs, multi_io_model.outputs)
    fn_outputs = fn([np.random.random((10, 32)), np.random.random((10, 32)),
                     np.random.random((10, 32)), np.random.random((10, 32))])
    assert [x.shape for x in fn_outputs] == [(10, 69)]

    # test with single output as tensor
    multi_io_model = Model([j, k, o, p], s)

    fn = K.function(multi_io_model.inputs, multi_io_model.outputs)
    fn_outputs = fn([np.random.random((10, 32)), np.random.random((10, 32)),
                     np.random.random((10, 32)), np.random.random((10, 32))])
    # note that the output of the K.function will still be a 1-elem list
    assert [x.shape for x in fn_outputs] == [(10, 69)]

    # test serialization
    print('multi_io_model.layers:', multi_io_model.layers)
    print('len(model.inbound_nodes):', len(model.inbound_nodes))
    print('len(model.outbound_nodes):', len(model.outbound_nodes))
    model_config = multi_io_model.get_config()
    print(model_config)
    print(json.dumps(model_config, indent=4))
    recreated_model = Model.from_config(model_config)

    fn = K.function(recreated_model.inputs, recreated_model.outputs)
    fn_outputs = fn([np.random.random((10, 32)), np.random.random((10, 32)),
                     np.random.random((10, 32)), np.random.random((10, 32))])
    # note that the output of the K.function will still be a 1-elem list
    assert [x.shape for x in fn_outputs] == [(10, 69)]

    config = model.get_config()
    Model.from_config(config)

    model.summary()
    json_str = model.to_json()
    model_from_json(json_str)

    yaml_str = model.to_yaml()
    model_from_yaml(yaml_str)

    ####################################################
    # test invalid graphs

    # input is not an Input tensor
    j = Input(shape=(32,), name='input_j')
    j = Dense(32)(j)
    k = Input(shape=(32,), name='input_k')
    m, n = model([j, k])

    with pytest.raises(Exception):
        Model([j, k], [m, n])

    # disconnected graph
    j = Input(shape=(32,), name='input_j')
    k = Input(shape=(32,), name='input_k')
    m, n = model([j, k])
    with pytest.raises(Exception) as e:
        Model([j], [m, n])

    # redudant outputs
    j = Input(shape=(32,), name='input_j')
    k = Input(shape=(32,), name='input_k')
    m, n = model([j, k])
    # this should work lol
    # TODO: raise a warning
    Model([j, k], [m, n, n])

    # redundant inputs
    j = Input(shape=(32,), name='input_j')
    k = Input(shape=(32,), name='input_k')
    m, n = model([j, k])
    with pytest.raises(Exception):
        Model([j, k, j], [m, n])

    # i have not idea what I'm doing: garbage as inputs/outputs
    j = Input(shape=(32,), name='input_j')
    k = Input(shape=(32,), name='input_k')
    m, n = model([j, k])
    with pytest.raises(Exception):
        Model([j, k], [m, n, 0])

    ####################################################
    # test calling layers/models on TF tensors

    if K._BACKEND == 'tensorflow':
        import tensorflow as tf
        j = Input(shape=(32,), name='input_j')
        k = Input(shape=(32,), name='input_k')
        m, n = model([j, k])
        tf_model = Model([j, k], [m, n])

        j_tf = tf.placeholder(dtype=K.floatx())
        k_tf = tf.placeholder(dtype=K.floatx())
        m_tf, n_tf = tf_model([j_tf, k_tf])
        assert m_tf.get_shape().as_list() == [None, 64]
        assert n_tf.get_shape().as_list() == [None, 5]

        # test merge
        layers.concatenate([j_tf, k_tf], axis=1)
        layers.sum([j_tf, k_tf])

        # test tensor input
        x = tf.placeholder(shape=(None, 2), dtype=K.floatx())
        InputLayer(input_tensor=x)

        x = Input(tensor=x)
        Dense(2)(x)


if __name__ == '__main__':
    pytest.main([__file__])
