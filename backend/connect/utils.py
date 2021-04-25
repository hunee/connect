#print('__FILE__: ', __file__)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        #else:  # 매번 __init__ 호출하고 싶으면
        #    cls._instances[cls].__init__(*args, **kwargs)
        return cls._instances[cls]

