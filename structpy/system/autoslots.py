
class Autoslots:

    __slots = {}

    def __enter__(self):
        if self.__class__ not in Autoslots.__slots:
            slots = set()
            for supercls in self.__class__.mro():
                slots.update(Autoslots.__slots.get(supercls, []))
            Autoslots.__slots[self.__class__] = slots
        self.__dict_state = set(self.__dict__)

    def __exit__(self, exc_type, exc_val, exc_tb):
        slots = set(self.__dict__) - self.__dict_state
        Autoslots.__slots[self.__class__].update(slots)
        del self.__dict_state