import warnings

from keras_core import backend
from keras_core.api_export import keras_core_export
from keras_core.layers.layer import Layer
from keras_core.ops.node import Node


@keras_core_export("keras_core.layers.InputLayer")
class InputLayer(Layer):
    def __init__(
        self,
        shape=None,
        batch_size=None,
        dtype=None,
        batch_shape=None,
        input_tensor=None,
        name=None,
        **kwargs,
    ):
        # TODO: support for sparse, ragged.
        super().__init__(name=name)
        if "input_shape" in kwargs:
            warnings.warn(
                "Argument `input_shape` is deprecated. Use `shape` instead."
            )
            shape = kwargs.pop("input_shape")

        if shape is not None and batch_shape is not None:
            raise ValueError(
                "You cannot pass both `shape` and `batch_shape` at the "
                "same time."
            )
        if batch_size is not None and batch_shape is not None:
            raise ValueError(
                "You cannot pass both `batch_size` and `batch_shape` at the "
                "same time."
            )
        if shape is None and batch_shape is None:
            raise ValueError("You must pass a `shape` argument.")

        if shape is not None:
            shape = backend.standardize_shape(shape)
            batch_shape = (batch_size,) + shape
        self.batch_shape = tuple(batch_shape)
        self._dtype = backend.standardize_dtype(dtype)

        if input_tensor is not None:
            if not isinstance(input_tensor, backend.KerasTensor):
                raise ValueError(
                    "Argument `input_tensor` must be a KerasTensor. "
                    f"Received invalid type: input_tensor={input_tensor} "
                    f"(of type {type(input_tensor)})"
                )
        else:
            input_tensor = backend.KerasTensor(
                shape=batch_shape, dtype=dtype, name=name
            )
        self._input_tensor = input_tensor
        Node(operation=self, call_args=(), call_kwargs={}, outputs=input_tensor)
        self.built = True

    def call(self):
        return

    @property
    def dtype(self):
        return self._dtype

    def get_config(self):
        return {
            "batch_shape": self.batch_shape,
            "dtype": self.dtype,
            "name": self.name,
        }


@keras_core_export(["keras_core.layers.Input", "keras_core.Input"])
def Input(
    shape=None,
    batch_size=None,
    dtype=None,
    batch_shape=None,
    name=None,
    tensor=None,
):
    """Used to instantiate a Keras tensor.

    A Keras tensor is a symbolic tensor-like object, which we augment with
    certain attributes that allow us to build a Keras model just by knowing the
    inputs and outputs of the model.

    For instance, if `a`, `b` and `c` are Keras tensors,
    it becomes possible to do:
    `model = Model(input=[a, b], output=c)`

    Args:
        shape: A shape tuple (tuple of integers or `None` objects),
            not including the batch size.
            For instance, `shape=(32,)` indicates that the expected input
            will be batches of 32-dimensional vectors. Elements of this tuple
            can be `None`; `None` elements represent dimensions where the shape
            is not known and may vary (e.g. sequence length).
        batch_size: Optional static batch size (integer).
        dtype: The data type expected by the input, as a string
            (e.g. `"float32"`, `"int32"`...)
        name: Optional name string for the layer.
            Should be unique in a model (do not reuse the same name twice).
            It will be autogenerated if it isn't provided.
        tensor: Optional existing tensor to wrap into the `Input` layer.
            If set, the layer will use this tensor rather
            than creating a new placeholder tensor.

    Returns:
      A Keras tensor.

    Example:

    ```python
    # This is a logistic regression in Keras
    x = Input(shape=(32,))
    y = Dense(16, activation='softmax')(x)
    model = Model(x, y)
    ```
    """
    layer = InputLayer(
        shape=shape,
        batch_size=batch_size,
        dtype=dtype,
        batch_shape=batch_shape,
        name=name,
        input_tensor=tensor,
    )
    return layer.output
