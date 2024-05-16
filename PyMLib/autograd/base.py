from __future__ import annotations

import math


class Variable:
    """A class of variables with automatic calculation of derivatives.

     Parameters
        ----------
        value : float or int
            Variable value.

        requires_grad : bool, default=False
            If the value is equal `True` it calculates the derivative.

        variables : list, default=None
            Variables dependent on a given variable and operations on them.
     """

    def __init__(self, value,
                 requires_grad=False,
                 operation=None,
                 variables=None):
        self.value = value
        self.requires_grad = requires_grad
        self.operation = operation
        self.variables = variables
        self.grad = 0

    def __add__(self, other) -> Variable:
        return Variable(
            self.value + other.value,
            requires_grad=self.requires_grad or other.requires_grad,
            operation=self._add_back,
            variables=[self, other]
        )

    def __sub__(self, other) -> Variable:
        return Variable(
            self.value - other.value,
            requires_grad=self.requires_grad or other.requires_grad,
            operation=self._sub_back,
            variables=[self, other]
        )

    def __mul__(self, other) -> Variable:
        return Variable(
            self.value * other.value,
            requires_grad=self.requires_grad or other.requires_grad,
            operation=self._mul_back,
            variables=[self, other]
        )

    def __truediv__(self, other) -> Variable:
        return Variable(
            self.value / other.value,
            requires_grad=self.requires_grad or other.requires_grad,
            operation=self._truediv_back,
            variables=[self, other]
        )

    def __pow__(self, other) -> Variable:
        return Variable(
            self.value ** other.value,
            requires_grad=self.requires_grad or other.requires_grad,
            operation=self._pow_back,
            variables=[self, other]
        )

    def exp(self) -> Variable:
        return Variable(
            math.exp(self.value),
            requires_grad=self.requires_grad,
            operation=self._add_back,
            variables=[self]
        )

    def __str__(self) -> str:
        return f"{self.value}"

    @staticmethod
    def _add_back(variable0, variable1, variable2) -> None:
        variable1.grad += variable0.grad if variable1.requires_grad else 0
        variable2.grad += variable0.grad if variable2.requires_grad else 0

    @staticmethod
    def _sub_back(variable0, variable1, variable2) -> None:
        variable1.grad += variable0.grad if variable1.requires_grad else 0
        variable2.grad -= variable0.grad if variable2.requires_grad else 0

    @staticmethod
    def _mul_back(variable0, variable1, variable2) -> None:
        variable1.grad += variable2.value * variable0.grad if variable1.requires_grad else 0
        variable2.grad += variable1.value * variable0.grad if variable2.requires_grad else 0

    @staticmethod
    def _truediv_back(variable0, variable1, variable2) -> None:
        if variable1.requires_grad:
            variable1.grad += 1 / variable2.value * variable0.grad
        if variable2.requires_grad:
            variable2.grad -= variable1.value / variable2.value ** 2

    @staticmethod
    def _pow_back(variable0, variable1, variable2) -> None:
        if variable1.requires_grad:
            variable1.grad += variable2.value * variable1.value ** (variable2.value - 1) * variable0.grad
        if variable2.requires_grad:
            variable2.grad += variable1.value * variable0.grad

    @staticmethod
    def _exp_back(variable0, variable1) -> None:
        if variable1.requires_grad:
            variable1.grad += math.exp(variable1.value) * variable0.grad

    def backward(self) -> None:
        """Performs a reverse pass. Calculates the gradient over all variables with `requires_grad`=True."""
        self.grad = int(self.requires_grad) if self.grad == 0 else self.grad
        if self.variables:
            self.operation(self, *self.variables)

            for variable in self.variables:
                variable.backward()
