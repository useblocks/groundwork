class Singleton(type):
    """
    Utility class to create a singleton of a class and to prohibit multi class instances.

    Usage::

        class MyClass(metaclass=Singelton):
            pass

        my_instance = MyClass()
        my_instance2 = MyClass()
        assertEqual(my_instance, my_instance2)

    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

