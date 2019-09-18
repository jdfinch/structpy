
class PointerFunnel:

    def __init__(self, item=None, level=None):
        self.pf_item = None
        self.pf_target = None
        self.pf_sources = set()
        if item is not None:
            self.pf_point(item, level)

    def pf_point(self, item, level=None):
        if isinstance(item, PointerFunnel):
            if level is not None:
                actual_item = item.pf_item
                ptrs = []
                while item is not None:
                    ptrs.append(item)
                    item = item.pf_target
                ptrs.append(actual_item)
                return self.pf_point(ptrs[-1-level])
            item.pf_sources.add(self)
            self.pf_target = item
            self.pf_update()
        else:
            self.pf_update(item)
            if self.pf_target is not None:
                self.pf_target.pf_sources.remove(self)
            self.pf_target = None

    def pf_delete(self):
        for source in self.pf_sources:
            source.pf_target = self.pf_target
        self.pf_item = None
        if self.pf_target is not None:
            self.pf_target.pf_sources.remove(self)
            self.pf_target = None

    def pf_update(self, item=None):
        if item is None:
            item = self.pf_target.pf_item
        self.pf_item = item
        for source in self.pf_sources:
            source.pf_update()

    def pf_level(self):
        if self.pf_target is None:
            return 1
        else:
            return 1 + self.pf_target.pf_level()

    def __str__(self):
        return '<PointerFunnel to ' + str(self.pf_item) + '>'


class PointerFunnelItem(PointerFunnel):

    def __getattr__(self, e):
        return self.pf_item.__getattribute__(e)

