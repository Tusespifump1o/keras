#Constraints

## Usage of constraints

Regularizers allow the use of penalties on particular sets of parameters during optimization.

A constraint is initilized with the value of the constraint. 
For example `maxnorm(3)` will constrain the weight vector to each hidden unit to have a maximum norm of 3.
The keyword arguments used for passing constraints to parameters in a layer will depend on the layer. 
For weights in the `Dense` layer it is simply `W_constraint`.
For biases in the `Dense` layer it is simply `b_constraint`.

```python
model.add(Dense(64, 64, W_constraint = maxnorm(2)))
```

## Available constraints

- __maxnorm__: maximum-norm constraint
- __nonneg__: non-negative constraint