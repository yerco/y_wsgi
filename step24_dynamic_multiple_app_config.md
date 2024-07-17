# Dynamic and Multiple Application Configuration Loading

As we have multiple apps (each having their own modules)we need a way to load the configuration for each app
dynamically. 

## App naming
Our apps need to be named with the suffix `_app`, e.g.: `whatever_app`
That's the idea behind `src/utils/app_scanner.py`

## Configuration Loading
We will have a default configuration in `src/config.py` and each app can have its own
configuration file, e.g.: `whatever_app/config.py`

## Configuration Merging
When loading the configuration, we will merge the default configuration with the user-defined

## Singleton Pattern
The Singleton pattern ensures that a class has only one instance and provides a global point of access to 
that instance.

Why Use the Singleton Pattern?
- To control access to a single instance of a class. This is useful when exactly one object is needed 
  to coordinate actions across the system, such as configuration settings.

```python
class Singleton:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

if __name__ == "main":
    # Create the first instance
    singleton1 = Singleton()
    # Try to create a second instance
    singleton2 = Singleton()
    
    # Both variables should point to the same instance
    print(f"Singleton 1 ID: {id(singleton1)}")
    print(f"Singleton 2 ID: {id(singleton2)}")
    print(f"Are both instances the same? {'Yes' if singleton1 is singleton2 else 'No'}")
```

How is the Singleton Pattern Implemented in ConfigLoader?
- We use a class-level dictionary `_instances` to keep track of instances for each application. 
  This ensures that each application can have its own unique instance of ConfigLoader.
- The `__new__` method checks if an instance for the given app_name exists. If not, it creates a 
  new instance and stores it in the `_instances` dictionary.

## Other things to notice
1. Simple Factory
   The `load_config` function can bee seen as a **simple factory**, returning an instance of `ConfigLoader`. 
   It encapsulates the logic of creating and initializing the `ConfigLoader object.
