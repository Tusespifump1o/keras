from keras_core import backend
from keras_core.layers.layer import Layer
from keras_core.operations.node import Node


class InputLayer(Layer):
    def __init__(
        self,
        shape=None,
        batch_size=None,
        dtype=None,
        batch_shape=None,
        input_tensor=None,
        name=None,
    ):
        # TODO: support for sparse, ragged.
        super().__init__(name=name)
        if shape is not None and batch_shape is not None:
            raise ValueError(
                "You cannot pass both `shape` and `batch_shape` at the same time."
            )
        if batch_size is not None and batch_shape is not None:
            raise ValueError(
                "You cannot pass both `batch_size` and `batch_shape` at the same time."
            )
        if shape is None and batch_shape is None:
            raise ValueError("You must pass a `shape` argument.")

        if shape:
            shape = backend.standardize_shape(shape)
            batch_shape = (batch_size,) + shape
        self.batch_shape = batch_shape
        self._dtype = backend.standardize_dtype(dtype)

        if input_tensor is not None:
            if not isinstance(input_tensor, backend.KerasTensor):
                raise ValueError(
                    "Argument `input_tensor` must be a KerasTensor. "
                    f"Received invalid type: input_tensor={input_tensor} (of type {type(input_tensor)})"
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


def Input(shape=None, batch_size=None, dtype=None, batch_shape=None, name=None):
    layer = InputLayer(
        shape=shape,
        batch_size=batch_size,
        dtype=dtype,
        batch_shape=batch_shape,
        name=name,
    )
    return layer.output
