import math


class Value:
    def __init__(self, data, _children=(), _op="", label=""):
        self.data = data
        # Children is here for plotting the DAG.
        self._prev = set(_children)
        self._op = _op
        self.label = label
        # gradients and backward
        self.grad = 0
        # _backward is a method that we can chain.
        self._backward = lambda: None

    def __repr__(self):
        return f"Value=({self.data})"

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), "+")

        def _backward():
            # Meant to update self and other's gradients
            # += to avoid
            self.grad += 1 * out.grad
            other.grad += 1 * out.grad

        # Definition of a backward pass
        out._backward = _backward

        return out

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data * other.data, (self, other), "*")

        def _backward():
            self.grad += other.data * out.grad
            other.grad += self.data * out.grad

        out._backward = _backward

        return out

    def __rmul__(self, other):
        return self * other

    def __sub__(self, other):
        return self + (-other)

    def __pow__(self, other):
        assert isinstance(other, (int, float))
        out = Value(self.data**other, (self,), f"**{other}")

        def _backward():
            self.grad += (other * (self.data ** (other - 1))) * out.grad

        out._backward = _backward

        return out

    def __truediv__(self, other):
        return self * (other**-1)

    def exp(self):
        out = Value(math.exp(self.data), (self,), "exp")

        def _backward():
            self.grad += out.data * out.grad

        out._backward = _backward

        return out

    def tanh(self):
        x = self.data
        t = (math.exp(2.0 * x) - 1) / (math.exp(2.0 * x) + 1)
        out = Value(t, (self,), "tanh")

        def _backward():
            self.grad += (1 - (t**2)) * out.grad

        out._backward = _backward

        return out

    def backward(self):
        # Automating the manual _backward() calls using topological sort.
        # Sort the DAG such that o is last.
        # Call _backward on the queue.
        topo = []
        visited = set()

        def build_topo(v):
            if v not in visited:
                visited.add(v)
            for child in v._prev:
                build_topo(child)
            topo.append(v)

        build_topo(self)
        self.grad = 1.0
        for node in reversed(topo):
            node._backward()

    # def relu(self):
