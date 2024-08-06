# Composite

The Composite pattern allows you to treat individual objects and compositions of objects uniformly. 
It’s useful when you have a tree structure and want to handle both simple and complex elements in the same way.

At our `Field` class we already have a `validate` method, we could think on defining an interface like this:
```python
class FieldComponent(ABC):
    @abstractmethod
    def validate(self, data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def render(self) -> str:
        pass
```
And it magically fits with our `Field` class, so we can make it a subclass of `FieldComponent`
