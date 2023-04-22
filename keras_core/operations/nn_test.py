import numpy as np
import pytest
import tensorflow as tf
from tensorflow.python.ops.numpy_ops import np_config

from keras_core import testing
from keras_core.backend import backend
from keras_core.backend.keras_tensor import KerasTensor
from keras_core.operations import nn as knn


@pytest.mark.skipif(
    backend() != "tensorflow",
    reason="Dynamic shapes are only supported in TensorFlow backend.",
)
class NNOpsDynamicShapeTest(testing.TestCase):
    def test_relu(self):
        x = KerasTensor([None, 2, 3])
        self.assertEqual(knn.relu(x).shape, (None, 2, 3))

    def test_relu6(self):
        x = KerasTensor([None, 2, 3])
        self.assertEqual(knn.relu6(x).shape, (None, 2, 3))

    def test_sigmoid(self):
        x = KerasTensor([None, 2, 3])
        self.assertEqual(knn.sigmoid(x).shape, (None, 2, 3))

    def test_softplus(self):
        x = KerasTensor([None, 2, 3])
        self.assertEqual(knn.softplus(x).shape, (None, 2, 3))

    def test_softsign(self):
        x = KerasTensor([None, 2, 3])
        self.assertEqual(knn.softsign(x).shape, (None, 2, 3))

    def test_silu(self):
        x = KerasTensor([None, 2, 3])
        self.assertEqual(knn.silu(x).shape, (None, 2, 3))

    def test_swish(self):
        x = KerasTensor([None, 2, 3])
        self.assertEqual(knn.swish(x).shape, (None, 2, 3))

    def test_log_sigmoid(self):
        x = KerasTensor([None, 2, 3])
        self.assertEqual(knn.log_sigmoid(x).shape, (None, 2, 3))

    def test_leaky_relu(self):
        x = KerasTensor([None, 2, 3])
        self.assertEqual(knn.leaky_relu(x).shape, (None, 2, 3))

    def test_hard_sigmoid(self):
        x = KerasTensor([None, 2, 3])
        self.assertEqual(knn.hard_sigmoid(x).shape, (None, 2, 3))

    def test_elu(self):
        x = KerasTensor([None, 2, 3])
        self.assertEqual(knn.elu(x).shape, (None, 2, 3))

    def test_selu(self):
        x = KerasTensor([None, 2, 3])
        self.assertEqual(knn.selu(x).shape, (None, 2, 3))

    def test_gelu(self):
        x = KerasTensor([None, 2, 3])
        self.assertEqual(knn.gelu(x).shape, (None, 2, 3))

    def test_softmax(self):
        x = KerasTensor([None, 2, 3])
        self.assertEqual(knn.softmax(x).shape, (None, 2, 3))
        self.assertEqual(knn.softmax(x, axis=1).shape, (None, 2, 3))
        self.assertEqual(knn.softmax(x, axis=-1).shape, (None, 2, 3))

    def test_log_softmax(self):
        x = KerasTensor([None, 2, 3])
        self.assertEqual(knn.log_softmax(x).shape, (None, 2, 3))
        self.assertEqual(knn.log_softmax(x, axis=1).shape, (None, 2, 3))
        self.assertEqual(knn.log_softmax(x, axis=-1).shape, (None, 2, 3))

    def test_max_pool(self):
        x = KerasTensor([None, 8, 3])
        self.assertEqual(knn.max_pool(x, 2, 1).shape, (None, 7, 3))
        self.assertEqual(
            knn.max_pool(x, 2, 2, padding="same").shape, (None, 4, 3)
        )

        x = KerasTensor([None, 8, 8, 3])
        self.assertEqual(knn.max_pool(x, 2, 1).shape, (None, 7, 7, 3))
        self.assertEqual(
            knn.max_pool(x, 2, 2, padding="same").shape, (None, 4, 4, 3)
        )
        self.assertEqual(
            knn.max_pool(x, (2, 2), (2, 2), padding="same").shape,
            (None, 4, 4, 3),
        )

    def test_average_pool(self):
        x = KerasTensor([None, 8, 3])
        self.assertEqual(knn.average_pool(x, 2, 1).shape, (None, 7, 3))
        self.assertEqual(
            knn.average_pool(x, 2, 2, padding="same").shape, (None, 4, 3)
        )

        x = KerasTensor([None, 8, 8, 3])
        self.assertEqual(knn.average_pool(x, 2, 1).shape, (None, 7, 7, 3))
        self.assertEqual(
            knn.average_pool(x, 2, 2, padding="same").shape, (None, 4, 4, 3)
        )
        self.assertEqual(
            knn.average_pool(x, (2, 2), (2, 2), padding="same").shape,
            (None, 4, 4, 3),
        )

    def test_conv(self):
        # Test 1D conv.
        inputs_1d = KerasTensor([None, 20, 3])
        kernel = KerasTensor([4, 3, 2])
        self.assertEqual(
            knn.conv(inputs_1d, kernel, 1, padding="valid").shape, (None, 17, 2)
        )
        self.assertEqual(
            knn.conv(inputs_1d, kernel, 1, padding="same").shape, (None, 20, 2)
        )
        self.assertEqual(
            knn.conv(inputs_1d, kernel, (2,), dilation_rate=2).shape,
            (None, 7, 2),
        )

        # Test 2D conv.
        inputs_2d = KerasTensor([None, 10, 10, 3])
        kernel = KerasTensor([2, 2, 3, 2])
        self.assertEqual(
            knn.conv(inputs_2d, kernel, 1, padding="valid").shape,
            (None, 9, 9, 2),
        )
        self.assertEqual(
            knn.conv(inputs_2d, kernel, 1, padding="same").shape,
            (None, 10, 10, 2),
        )
        self.assertEqual(
            knn.conv(inputs_2d, kernel, (2, 1), dilation_rate=(2, 1)).shape,
            (None, 4, 9, 2),
        )

        # Test 3D conv.
        inputs_3d = KerasTensor([None, 8, 8, 8, 3])
        kernel = KerasTensor([3, 3, 3, 3, 2])
        self.assertEqual(
            knn.conv(inputs_3d, kernel, 1, padding="valid").shape,
            (None, 6, 6, 6, 2),
        )
        self.assertEqual(
            knn.conv(inputs_3d, kernel, (2, 1, 2), padding="same").shape,
            (None, 4, 8, 4, 2),
        )
        self.assertEqual(
            knn.conv(
                inputs_3d, kernel, 1, padding="valid", dilation_rate=(1, 2, 2)
            ).shape,
            (None, 6, 4, 4, 2),
        )

    def test_depthwise_conv(self):
        # Test 1D depthwise conv.
        inputs_1d = KerasTensor([None, 20, 3])
        kernel = KerasTensor([4, 3, 1])
        self.assertEqual(
            knn.depthwise_conv(inputs_1d, kernel, 1, padding="valid").shape,
            (None, 17, 3),
        )
        self.assertEqual(
            knn.depthwise_conv(inputs_1d, kernel, (1,), padding="same").shape,
            (None, 20, 3),
        )
        self.assertEqual(
            knn.depthwise_conv(inputs_1d, kernel, 2, dilation_rate=2).shape,
            (None, 7, 3),
        )

        # Test 2D depthwise conv.
        inputs_2d = KerasTensor([None, 10, 10, 3])
        kernel = KerasTensor([2, 2, 3, 1])
        self.assertEqual(
            knn.depthwise_conv(inputs_2d, kernel, 1, padding="valid").shape,
            (None, 9, 9, 3),
        )
        self.assertEqual(
            knn.depthwise_conv(inputs_2d, kernel, (1, 2), padding="same").shape,
            (None, 10, 5, 3),
        )
        self.assertEqual(
            knn.depthwise_conv(inputs_2d, kernel, 2, dilation_rate=2).shape,
            (None, 4, 4, 3),
        )
        self.assertEqual(
            knn.depthwise_conv(
                inputs_2d, kernel, 2, dilation_rate=(2, 1)
            ).shape,
            (None, 4, 5, 3),
        )

    def test_separable_conv(self):
        # Test 1D separable conv.
        inputs_1d = KerasTensor([None, 20, 3])
        kernel = KerasTensor([4, 3, 2])
        pointwise_kernel = KerasTensor([1, 6, 5])
        self.assertEqual(
            knn.separable_conv(
                inputs_1d, kernel, pointwise_kernel, 1, padding="valid"
            ).shape,
            (None, 17, 5),
        )
        self.assertEqual(
            knn.separable_conv(
                inputs_1d, kernel, pointwise_kernel, 1, padding="same"
            ).shape,
            (None, 20, 5),
        )
        self.assertEqual(
            knn.separable_conv(
                inputs_1d, kernel, pointwise_kernel, 2, dilation_rate=2
            ).shape,
            (None, 7, 5),
        )

        # Test 2D separable conv.
        inputs_2d = KerasTensor([None, 10, 10, 3])
        kernel = KerasTensor([2, 2, 3, 2])
        pointwise_kernel = KerasTensor([1, 1, 6, 5])
        self.assertEqual(
            knn.separable_conv(
                inputs_2d, kernel, pointwise_kernel, 1, padding="valid"
            ).shape,
            (None, 9, 9, 5),
        )
        self.assertEqual(
            knn.separable_conv(
                inputs_2d, kernel, pointwise_kernel, (1, 2), padding="same"
            ).shape,
            (None, 10, 5, 5),
        )
        self.assertEqual(
            knn.separable_conv(
                inputs_2d, kernel, pointwise_kernel, 2, dilation_rate=(2, 1)
            ).shape,
            (None, 4, 5, 5),
        )

    def test_conv_transpose(self):
        inputs_1d = KerasTensor([None, 4, 3])
        kernel = KerasTensor([2, 5, 3])
        self.assertEqual(
            knn.conv_transpose(inputs_1d, kernel, 2).shape, (None, 8, 5)
        )
        self.assertEqual(
            knn.conv_transpose(inputs_1d, kernel, 2, padding="same").shape,
            (None, 8, 5),
        )
        self.assertEqual(
            knn.conv_transpose(
                inputs_1d, kernel, 5, padding="valid", output_padding=4
            ).shape,
            (None, 21, 5),
        )

        inputs_2d = KerasTensor([None, 4, 4, 3])
        kernel = KerasTensor([2, 2, 5, 3])
        self.assertEqual(
            knn.conv_transpose(inputs_2d, kernel, 2).shape, (None, 8, 8, 5)
        )
        self.assertEqual(
            knn.conv_transpose(inputs_2d, kernel, (2, 2), padding="same").shape,
            (None, 8, 8, 5),
        )
        self.assertEqual(
            knn.conv_transpose(
                inputs_2d, kernel, (5, 5), padding="valid", output_padding=4
            ).shape,
            (None, 21, 21, 5),
        )


@pytest.mark.skipif(
    backend() != "tensorflow",
    reason="Not have other backend support yet.",
)
class NNOpsStaticShapeTest(testing.TestCase):
    def test_relu(self):
        x = KerasTensor([1, 2, 3])
        self.assertEqual(knn.relu(x).shape, (1, 2, 3))

    def test_relu6(self):
        x = KerasTensor([1, 2, 3])
        self.assertEqual(knn.relu6(x).shape, (1, 2, 3))

    def test_sigmoid(self):
        x = KerasTensor([1, 2, 3])
        self.assertEqual(knn.sigmoid(x).shape, (1, 2, 3))

    def test_softplus(self):
        x = KerasTensor([1, 2, 3])
        self.assertEqual(knn.softplus(x).shape, (1, 2, 3))

    def test_softsign(self):
        x = KerasTensor([1, 2, 3])
        self.assertEqual(knn.softsign(x).shape, (1, 2, 3))

    def test_silu(self):
        x = KerasTensor([1, 2, 3])
        self.assertEqual(knn.silu(x).shape, (1, 2, 3))

    def test_swish(self):
        x = KerasTensor([1, 2, 3])
        self.assertEqual(knn.swish(x).shape, (1, 2, 3))

    def test_log_sigmoid(self):
        x = KerasTensor([1, 2, 3])
        self.assertEqual(knn.log_sigmoid(x).shape, (1, 2, 3))

    def test_leaky_relu(self):
        x = KerasTensor([1, 2, 3])
        self.assertEqual(knn.leaky_relu(x).shape, (1, 2, 3))

    def test_hard_sigmoid(self):
        x = KerasTensor([1, 2, 3])
        self.assertEqual(knn.hard_sigmoid(x).shape, (1, 2, 3))

    def test_elu(self):
        x = KerasTensor([1, 2, 3])
        self.assertEqual(knn.elu(x).shape, (1, 2, 3))

    def test_selu(self):
        x = KerasTensor([1, 2, 3])
        self.assertEqual(knn.selu(x).shape, (1, 2, 3))

    def test_gelu(self):
        x = KerasTensor([1, 2, 3])
        self.assertEqual(knn.gelu(x).shape, (1, 2, 3))

    def test_softmax(self):
        x = KerasTensor([1, 2, 3])
        self.assertEqual(knn.softmax(x).shape, (1, 2, 3))
        self.assertEqual(knn.softmax(x, axis=1).shape, (1, 2, 3))
        self.assertEqual(knn.softmax(x, axis=-1).shape, (1, 2, 3))

    def test_log_softmax(self):
        x = KerasTensor([1, 2, 3])
        self.assertEqual(knn.log_softmax(x).shape, (1, 2, 3))
        self.assertEqual(knn.log_softmax(x, axis=1).shape, (1, 2, 3))
        self.assertEqual(knn.log_softmax(x, axis=-1).shape, (1, 2, 3))

    def test_max_pool(self):
        x = KerasTensor([1, 8, 3])
        self.assertEqual(knn.max_pool(x, 2, 1).shape, (1, 7, 3))
        self.assertEqual(knn.max_pool(x, 2, 2, padding="same").shape, (1, 4, 3))

        x = KerasTensor([1, 8, 8, 3])
        self.assertEqual(knn.max_pool(x, 2, 1).shape, (1, 7, 7, 3))
        self.assertEqual(
            knn.max_pool(x, 2, 2, padding="same").shape, (1, 4, 4, 3)
        )
        self.assertEqual(
            knn.max_pool(x, (2, 2), (2, 2), padding="same").shape, (1, 4, 4, 3)
        )

    def test_average_pool(self):
        x = KerasTensor([1, 8, 3])
        self.assertEqual(knn.average_pool(x, 2, 1).shape, (1, 7, 3))
        self.assertEqual(
            knn.average_pool(x, 2, 2, padding="same").shape, (1, 4, 3)
        )

        x = KerasTensor([1, 8, 8, 3])
        self.assertEqual(knn.average_pool(x, 2, 1).shape, (1, 7, 7, 3))
        self.assertEqual(
            knn.average_pool(x, 2, 2, padding="same").shape, (1, 4, 4, 3)
        )
        self.assertEqual(
            knn.average_pool(x, (2, 2), (2, 2), padding="same").shape,
            (1, 4, 4, 3),
        )

    def test_conv(self):
        # Test 1D conv.
        inputs_1d = KerasTensor([2, 20, 3])
        kernel = KerasTensor([4, 3, 2])
        self.assertEqual(
            knn.conv(inputs_1d, kernel, 1, padding="valid").shape, (2, 17, 2)
        )
        self.assertEqual(
            knn.conv(inputs_1d, kernel, 1, padding="same").shape, (2, 20, 2)
        )
        self.assertEqual(
            knn.conv(inputs_1d, kernel, (2,), dilation_rate=2).shape, (2, 7, 2)
        )

        # Test 2D conv.
        inputs_2d = KerasTensor([2, 10, 10, 3])
        kernel = KerasTensor([2, 2, 3, 2])
        self.assertEqual(
            knn.conv(inputs_2d, kernel, 1, padding="valid").shape, (2, 9, 9, 2)
        )
        self.assertEqual(
            knn.conv(inputs_2d, kernel, 1, padding="same").shape, (2, 10, 10, 2)
        )
        self.assertEqual(
            knn.conv(inputs_2d, kernel, (2, 1), dilation_rate=(2, 1)).shape,
            (2, 4, 9, 2),
        )

        # Test 3D conv.
        inputs_3d = KerasTensor([2, 8, 8, 8, 3])
        kernel = KerasTensor([3, 3, 3, 3, 2])
        self.assertEqual(
            knn.conv(inputs_3d, kernel, 1, padding="valid").shape,
            (2, 6, 6, 6, 2),
        )
        self.assertEqual(
            knn.conv(inputs_3d, kernel, (2, 1, 2), padding="same").shape,
            (2, 4, 8, 4, 2),
        )
        self.assertEqual(
            knn.conv(
                inputs_3d, kernel, 1, padding="valid", dilation_rate=(1, 2, 2)
            ).shape,
            (2, 6, 4, 4, 2),
        )

    def test_depthwise_conv(self):
        # Test 1D depthwise conv.
        inputs_1d = KerasTensor([2, 20, 3])
        kernel = KerasTensor([4, 3, 1])
        self.assertEqual(
            knn.depthwise_conv(inputs_1d, kernel, 1, padding="valid").shape,
            (2, 17, 3),
        )
        self.assertEqual(
            knn.depthwise_conv(inputs_1d, kernel, (1,), padding="same").shape,
            (2, 20, 3),
        )
        self.assertEqual(
            knn.depthwise_conv(inputs_1d, kernel, 2, dilation_rate=2).shape,
            (2, 7, 3),
        )

        # Test 2D depthwise conv.
        inputs_2d = KerasTensor([2, 10, 10, 3])
        kernel = KerasTensor([2, 2, 3, 1])
        self.assertEqual(
            knn.depthwise_conv(inputs_2d, kernel, 1, padding="valid").shape,
            (2, 9, 9, 3),
        )
        self.assertEqual(
            knn.depthwise_conv(inputs_2d, kernel, (1, 2), padding="same").shape,
            (2, 10, 5, 3),
        )
        self.assertEqual(
            knn.depthwise_conv(inputs_2d, kernel, 2, dilation_rate=2).shape,
            (2, 4, 4, 3),
        )
        self.assertEqual(
            knn.depthwise_conv(
                inputs_2d, kernel, 2, dilation_rate=(2, 1)
            ).shape,
            (2, 4, 5, 3),
        )

    def test_separable_conv(self):
        # Test 1D separable conv.
        inputs_1d = KerasTensor([2, 20, 3])
        kernel = KerasTensor([4, 3, 2])
        pointwise_kernel = KerasTensor([1, 6, 5])
        self.assertEqual(
            knn.separable_conv(
                inputs_1d, kernel, pointwise_kernel, 1, padding="valid"
            ).shape,
            (2, 17, 5),
        )
        self.assertEqual(
            knn.separable_conv(
                inputs_1d, kernel, pointwise_kernel, 1, padding="same"
            ).shape,
            (2, 20, 5),
        )
        self.assertEqual(
            knn.separable_conv(
                inputs_1d, kernel, pointwise_kernel, 2, dilation_rate=2
            ).shape,
            (2, 7, 5),
        )

        # Test 2D separable conv.
        inputs_2d = KerasTensor([2, 10, 10, 3])
        kernel = KerasTensor([2, 2, 3, 2])
        pointwise_kernel = KerasTensor([1, 1, 6, 5])
        self.assertEqual(
            knn.separable_conv(
                inputs_2d, kernel, pointwise_kernel, 1, padding="valid"
            ).shape,
            (2, 9, 9, 5),
        )
        self.assertEqual(
            knn.separable_conv(
                inputs_2d, kernel, pointwise_kernel, (1, 2), padding="same"
            ).shape,
            (2, 10, 5, 5),
        )
        self.assertEqual(
            knn.separable_conv(
                inputs_2d, kernel, pointwise_kernel, 2, dilation_rate=(2, 1)
            ).shape,
            (2, 4, 5, 5),
        )

    def test_conv_transpose(self):
        inputs_1d = KerasTensor([2, 4, 3])
        kernel = KerasTensor([2, 5, 3])
        self.assertEqual(
            knn.conv_transpose(inputs_1d, kernel, 2).shape, (2, 8, 5)
        )
        self.assertEqual(
            knn.conv_transpose(inputs_1d, kernel, 2, padding="same").shape,
            (2, 8, 5),
        )
        self.assertEqual(
            knn.conv_transpose(
                inputs_1d, kernel, 5, padding="valid", output_padding=4
            ).shape,
            (2, 21, 5),
        )

        inputs_2d = KerasTensor([2, 4, 4, 3])
        kernel = KerasTensor([2, 2, 5, 3])
        self.assertEqual(
            knn.conv_transpose(inputs_2d, kernel, 2).shape, (2, 8, 8, 5)
        )
        self.assertEqual(
            knn.conv_transpose(inputs_2d, kernel, (2, 2), padding="same").shape,
            (2, 8, 8, 5),
        )
        self.assertEqual(
            knn.conv_transpose(
                inputs_2d, kernel, (5, 5), padding="valid", output_padding=4
            ).shape,
            (2, 21, 21, 5),
        )


@pytest.mark.skipif(
    backend() != "tensorflow",
    reason="Not have other backend support yet.",
)
class NNOpsCorrectnessTest(testing.TestCase):
    def test_relu(self):
        x = np.array([-1, 0, 1, 2, 3], dtype=np.float32)
        self.assertAllClose(knn.relu(x), [0, 0, 1, 2, 3])

    def test_relu6(self):
        x = np.array([-1, 0, 1, 2, 3, 4, 5, 6, 7], dtype=np.float32)
        self.assertAllClose(knn.relu6(x), [0, 0, 1, 2, 3, 4, 5, 6, 6])

    def test_sigmoid(self):
        x = np.array([-1, 0, 1, 2, 3], dtype=np.float32)
        self.assertAllClose(
            knn.sigmoid(x), [0.26894143, 0.5, 0.7310586, 0.880797, 0.95257413]
        )

    def test_softplus(self):
        x = np.array([-1, 0, 1, 2, 3], dtype=np.float32)
        self.assertAllClose(
            knn.softplus(x),
            [0.31326166, 0.6931472, 1.3132616, 2.126928, 3.0485873],
        )

    def test_softsign(self):
        x = np.array([-1, 0, 1, 2, 3], dtype=np.float32)
        self.assertAllClose(knn.softsign(x), [-0.5, 0, 0.5, 0.6666667, 0.75])

    def test_silu(self):
        x = np.array([-1, 0, 1, 2, 3], dtype=np.float32)
        self.assertAllClose(
            knn.silu(x),
            [-0.26894143, 0, 0.7310586, 1.7615942, 2.8577223],
        )

    def test_swish(self):
        x = np.array([-1, 0, 1, 2, 3], dtype=np.float32)
        self.assertAllClose(
            knn.swish(x), [-0.26894143, 0.0, 0.7310586, 1.7615943, 2.8577223]
        )

    def test_log_sigmoid(self):
        x = np.array([-1, 0, 1, 2, 3], dtype=np.float32)
        self.assertAllClose(
            knn.log_sigmoid(x),
            [-1.3132616, -0.6931472, -0.31326166, -0.126928, -0.04858732],
        )

    def test_leaky_relu(self):
        x = np.array([-1, 0, 1, 2, 3], dtype=np.float32)
        self.assertAllClose(
            knn.leaky_relu(x),
            [-0.2, 0, 1, 2, 3],
        )

    def test_hard_sigmoid(self):
        x = np.array([-1, 0, 1, 2, 3], dtype=np.float32)
        self.assertAllClose(
            knn.hard_sigmoid(x),
            [0.33333334, 0.5, 0.6666667, 0.8333334, 1.0],
        )

    def test_elu(self):
        x = np.array([-1, 0, 1, 2, 3], dtype=np.float32)
        self.assertAllClose(
            knn.elu(x),
            [-0.63212055, 0, 1, 2, 3],
        )

    def test_selu(self):
        x = np.array([-1, 0, 1, 2, 3], dtype=np.float32)
        self.assertAllClose(
            knn.selu(x),
            [-1.1113307, 0.0, 1.050701, 2.101402, 3.152103],
        )

    def test_gelu(self):
        x = np.array([-1, 0, 1, 2, 3], dtype=np.float32)
        self.assertAllClose(
            knn.gelu(x),
            [-0.15880796, 0.0, 0.841192, 1.9545977, 2.9963627],
        )

    def test_softmax(self):
        x = np.array([1, 2, 3], dtype=np.float32)
        self.assertAllClose(
            knn.softmax(x),
            [0.09003057, 0.24472848, 0.66524094],
        )
        self.assertAllClose(
            knn.softmax(x, axis=0),
            [0.09003057, 0.24472848, 0.66524094],
        )
        self.assertAllClose(
            knn.softmax(x, axis=-1),
            [0.09003057, 0.24472848, 0.66524094],
        )

    def test_log_softmax(self):
        x = np.array([1, 2, 3], dtype=np.float32)
        self.assertAllClose(
            knn.log_softmax(x),
            [-2.407606, -1.4076059, -0.4076059],
        )
        self.assertAllClose(
            knn.log_softmax(x, axis=0),
            [-2.407606, -1.4076059, -0.4076059],
        )
        self.assertAllClose(
            knn.log_softmax(x, axis=-1),
            [-2.407606, -1.4076059, -0.4076059],
        )

    def test_max_pool(self):
        # Test 1D max pooling.
        x = np.arange(120, dtype=float).reshape([2, 20, 3])
        self.assertAllClose(
            knn.max_pool(x, 2, 1, padding="valid"),
            tf.nn.max_pool1d(x, 2, 1, padding="VALID"),
        )
        self.assertAllClose(
            knn.max_pool(x, 2, 2, padding="same"),
            tf.nn.max_pool1d(x, 2, 2, padding="SAME"),
        )

        # Test 2D max pooling.
        x = np.arange(540, dtype=float).reshape([2, 10, 9, 3])
        self.assertAllClose(
            knn.max_pool(x, 2, 1, padding="valid"),
            tf.nn.max_pool2d(x, 2, 1, padding="VALID"),
        )
        self.assertAllClose(
            knn.max_pool(x, 2, (2, 1), padding="same"),
            tf.nn.max_pool2d(x, 2, (2, 1), padding="SAME"),
        )

    def test_average_pool(self):
        # Test 1D max pooling.
        x = np.arange(120, dtype=float).reshape([2, 20, 3])
        self.assertAllClose(
            knn.average_pool(x, 2, 1, padding="valid"),
            tf.nn.avg_pool1d(x, 2, 1, padding="VALID"),
        )
        self.assertAllClose(
            knn.average_pool(x, 2, 2, padding="same"),
            tf.nn.avg_pool1d(x, 2, 2, padding="SAME"),
        )

        # Test 2D max pooling.
        x = np.arange(540, dtype=float).reshape([2, 10, 9, 3])
        self.assertAllClose(
            knn.average_pool(x, 2, 1, padding="valid"),
            tf.nn.avg_pool2d(x, 2, 1, padding="VALID"),
        )
        self.assertAllClose(
            knn.average_pool(x, 2, (2, 1), padding="same"),
            tf.nn.avg_pool2d(x, 2, (2, 1), padding="SAME"),
        )

    def test_conv(self):
        # Test 1D conv.
        inputs_1d = np.arange(120, dtype=float).reshape([2, 20, 3])
        kernel = np.arange(24, dtype=float).reshape([4, 3, 2])

        outputs = knn.conv(inputs_1d, kernel, 1, padding="valid")
        expected = tf.nn.conv1d(inputs_1d, kernel, 1, padding="VALID")
        self.assertAllClose(outputs, expected)

        outputs = knn.conv(inputs_1d, kernel, 2, padding="same")
        expected = tf.nn.conv1d(inputs_1d, kernel, 2, padding="SAME")
        self.assertAllClose(outputs, expected)

        outputs = knn.conv(
            inputs_1d, kernel, 1, padding="same", dilation_rate=2
        )
        expected = tf.nn.conv1d(
            inputs_1d, kernel, 1, padding="SAME", dilations=2
        )
        self.assertAllClose(outputs, expected)

        # Test 2D conv.
        inputs_2d = np.arange(600, dtype=float).reshape([2, 10, 10, 3])
        kernel = np.arange(24, dtype=float).reshape([2, 2, 3, 2])

        outputs = knn.conv(inputs_2d, kernel, 1, padding="valid")
        expected = tf.nn.conv2d(inputs_2d, kernel, 1, padding="VALID")
        self.assertAllClose(outputs, expected)

        outputs = knn.conv(inputs_2d, kernel, (1, 2), padding="valid")
        expected = tf.nn.conv2d(inputs_2d, kernel, (1, 2), padding="VALID")
        self.assertAllClose(outputs, expected)

        outputs = knn.conv(inputs_2d, kernel, 2, padding="same")
        expected = tf.nn.conv2d(inputs_2d, kernel, 2, padding="SAME")
        self.assertAllClose(outputs, expected)

        outputs = knn.conv(
            inputs_2d, kernel, 1, padding="same", dilation_rate=2
        )
        expected = tf.nn.conv2d(
            inputs_2d, kernel, 1, padding="SAME", dilations=2
        )
        self.assertAllClose(outputs, expected)

        outputs = knn.conv(
            inputs_2d,
            kernel,
            1,
            padding="same",
            dilation_rate=(2, 1),
        )
        expected = tf.nn.conv2d(
            inputs_2d,
            kernel,
            1,
            padding="SAME",
            dilations=(2, 1),
        )
        self.assertAllClose(outputs, expected)

        # Test 3D conv.
        inputs_3d = np.arange(3072, dtype=float).reshape([2, 8, 8, 8, 3])
        kernel = np.arange(162, dtype=float).reshape([3, 3, 3, 3, 2])

        outputs = knn.conv(inputs_3d, kernel, 1, padding="valid")
        expected = tf.nn.conv3d(
            inputs_3d, kernel, (1, 1, 1, 1, 1), padding="VALID"
        )
        self.assertAllClose(outputs, expected)

        outputs = knn.conv(
            inputs_3d,
            kernel,
            (1, 1, 1),
            padding="valid",
            dilation_rate=(1, 1, 1),
        )
        expected = tf.nn.conv3d(
            inputs_3d,
            kernel,
            (1, 1, 1, 1, 1),
            padding="VALID",
            dilations=(1, 1, 1, 1, 1),
        )
        self.assertAllClose(outputs, expected)

        outputs = knn.conv(inputs_3d, kernel, 2, padding="same")
        expected = tf.nn.conv3d(
            inputs_3d, kernel, (1, 2, 2, 2, 1), padding="SAME"
        )
        self.assertAllClose(outputs, expected)

    def test_depthwise_conv(self):
        # Test 2D conv.
        inputs_2d = np.arange(600, dtype=float).reshape([2, 10, 10, 3])
        kernel = np.arange(24, dtype=float).reshape([2, 2, 3, 2])

        outputs = knn.depthwise_conv(inputs_2d, kernel, 1, padding="valid")
        expected = tf.nn.depthwise_conv2d(
            inputs_2d, kernel, (1, 1, 1, 1), padding="VALID"
        )
        self.assertAllClose(outputs, expected)

        outputs = knn.depthwise_conv(inputs_2d, kernel, (1, 1), padding="valid")
        expected = tf.nn.depthwise_conv2d(
            inputs_2d, kernel, (1, 1, 1, 1), padding="VALID"
        )
        self.assertAllClose(outputs, expected)

        outputs = knn.depthwise_conv(inputs_2d, kernel, (2, 2), padding="same")
        expected = tf.nn.depthwise_conv2d(
            inputs_2d, kernel, (1, 2, 2, 1), padding="SAME"
        )
        self.assertAllClose(outputs, expected)

        outputs = knn.depthwise_conv(
            inputs_2d, kernel, 1, padding="same", dilation_rate=(2, 2)
        )
        expected = tf.nn.depthwise_conv2d(
            inputs_2d, kernel, (1, 1, 1, 1), padding="SAME", dilations=(2, 2)
        )
        self.assertAllClose(outputs, expected)

    def test_separable_conv(self):
        # Test 2D conv.
        inputs_2d = np.arange(600, dtype=float).reshape([2, 10, 10, 3])
        depthwise_kernel = np.arange(24, dtype=float).reshape([2, 2, 3, 2])
        pointwise_kernel = np.arange(72, dtype=float).reshape([1, 1, 6, 12])

        outputs = knn.separable_conv(
            inputs_2d, depthwise_kernel, pointwise_kernel, 1, padding="valid"
        )
        expected = tf.nn.separable_conv2d(
            inputs_2d,
            depthwise_kernel,
            pointwise_kernel,
            (1, 1, 1, 1),
            padding="VALID",
        )
        self.assertAllClose(outputs, expected)

        outputs = knn.separable_conv(
            inputs_2d,
            depthwise_kernel,
            pointwise_kernel,
            (1, 1),
            padding="valid",
        )
        expected = tf.nn.separable_conv2d(
            inputs_2d,
            depthwise_kernel,
            pointwise_kernel,
            (1, 1, 1, 1),
            padding="VALID",
        )
        self.assertAllClose(outputs, expected)

        outputs = knn.separable_conv(
            inputs_2d, depthwise_kernel, pointwise_kernel, 2, padding="same"
        )
        expected = tf.nn.separable_conv2d(
            inputs_2d,
            depthwise_kernel,
            pointwise_kernel,
            (1, 2, 2, 1),
            padding="SAME",
        )
        self.assertAllClose(outputs, expected)

        outputs = knn.separable_conv(
            inputs_2d,
            depthwise_kernel,
            pointwise_kernel,
            1,
            padding="same",
            dilation_rate=(2, 2),
        )
        expected = tf.nn.separable_conv2d(
            inputs_2d,
            depthwise_kernel,
            pointwise_kernel,
            (1, 1, 1, 1),
            padding="SAME",
            dilations=(2, 2),
        )
        self.assertAllClose(outputs, expected)

    def test_conv_transpose(self):
        # Test 1D conv.
        inputs_1d = np.arange(24, dtype=float).reshape([2, 4, 3])
        kernel = np.arange(30, dtype=float).reshape([2, 5, 3])
        outputs = knn.conv_transpose(inputs_1d, kernel, 2, padding="valid")
        expected = tf.nn.conv_transpose(
            inputs_1d, kernel, [2, 8, 5], 2, padding="VALID"
        )
        self.assertAllClose(outputs, expected)

        outputs = knn.conv_transpose(inputs_1d, kernel, 2, padding="same")
        expected = tf.nn.conv_transpose(
            inputs_1d, kernel, [2, 8, 5], 2, padding="SAME"
        )
        self.assertAllClose(outputs, expected)

        outputs = knn.conv_transpose(
            inputs_1d, kernel, 5, output_padding=4, padding="valid"
        )
        expected = tf.nn.conv_transpose(
            inputs_1d, kernel, [2, 21, 5], 5, padding="VALID"
        )
        self.assertAllClose(outputs, expected)

        # Test 2D conv.
        inputs_2d = np.arange(96, dtype=float).reshape([2, 4, 4, 3])
        kernel = np.arange(60, dtype=float).reshape([2, 2, 5, 3])

        outputs = knn.conv_transpose(inputs_2d, kernel, (2, 2), padding="valid")
        expected = tf.nn.conv_transpose(
            inputs_2d, kernel, [2, 8, 8, 5], (2, 2), padding="VALID"
        )
        self.assertAllClose(outputs, expected)

        outputs = knn.conv_transpose(inputs_2d, kernel, 2, padding="same")
        expected = tf.nn.conv_transpose(
            inputs_2d, kernel, [2, 8, 8, 5], 2, padding="SAME"
        )
        self.assertAllClose(outputs, expected)

        outputs = knn.conv_transpose(
            inputs_2d,
            kernel,
            5,
            output_padding=4,
            padding="valid",
            dilation_rate=(1, 1),
        )
        expected = tf.nn.conv_transpose(
            inputs_2d,
            kernel,
            [2, 21, 21, 5],
            5,
            padding="VALID",
            dilations=(1, 1),
        )
        self.assertAllClose(outputs, expected)
