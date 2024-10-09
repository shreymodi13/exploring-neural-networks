#Here we build the gradient engine which would help us in doing backprop

#We treat each scalar as an object. We define the class here. This file also shows the operations supported.

class Value():
    def __init__(self, data, _children = (), _op =''):
        self.data = data
        self.grad = 0
        self._backward = lambda: None #for assigning how to backward prop this node. Basically which function needs to be called to assign its grad
        self._prev = set(_children)

    def __repr__(self) -> str:
        pass

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)

        out = Value(self.data + other.data, (self, other), '+')

        def _backward(self):

            other.grad += 1.0*out.grad
            self.grad += 1.0*out.grad
        out._backward = _backward

        return out

    def __mul__(self, other):
        other = other if isinstance(other, Value) else Value(other)

        out = Value(self.data * other.data, (self, other), '*')

        def _backward(self):
            self.grad += other.data*out.grad
            other.grad +=self.data*out.grad
        
        out._backward = _backward

        return out
    
    def __pow__(self, other):

        assert isinstance(other, (int, float)), "only supporting int/float powers for now"
        out = Value(self.data**other, (self,), f'**{other}')

        def _backward():
            self.grad += (other * self.data**(other-1)) * out.grad
        out._backward = _backward

        return out

    def relu(self):
        out = Value(0 if self.data < 0 else self.data, (self,), 'ReLU')

        def _backward():
            self.grad += (out.data > 0) * out.grad
        out._backward = _backward

        return out

    def __rmul__(self, other):
        return self*other

    def __neg__(self): # -self
        return self * -1

    def __radd__(self, other): # other + self
        return self + other

    def __sub__(self, other): # self - other
        return self + (-other)

    def __rsub__(self, other): # other - self
        return other + (-self)

    def __truediv__(self, other): # self / other
        return self * other**-1

    def __rtruediv__(self, other): # other / self
        return other * self**-1

    def __repr__(self):
        return f"Value(data={self.data}, grad={self.grad})"

    def backward(self):

        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)
        self.grad = 1
        for v in reversed(topo):
            v._backward()


        

