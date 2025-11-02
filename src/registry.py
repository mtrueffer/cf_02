CLASS_REGISTRY = {}

def register_class(cls):
    CLASS_REGISTRY[cls.__name__] = cls
    return cls

def get_class(name):
    if name not in CLASS_REGISTRY:
        raise ValueError(f"Class '{name}' not found in registry")
    return CLASS_REGISTRY[name]
