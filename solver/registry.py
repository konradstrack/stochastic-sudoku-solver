from collections import defaultdict

registry = defaultdict(dict)


def register(group, name):
    def insert(cls):
        registry[group][name] = cls
        return cls

    return insert

