

class UnitTest:

    def __init__(self,
                 test_function,
                 subtests=None,
                 is_constructor=None,
                 is_disabled=None,
                 is_silent=None,
                 is_property=None,
                 tags=None):
        self.test_function = test_function
        self.subtests = [] if subtests is None else list(subtests)
        self.is_constructor = self._init_arg(is_constructor, self._is_constructor)
        self.is_disabled = self._init_arg(is_disabled, self._is_disabled)
        self.is_silent = self._is_silent() if is_silent is None else is_silent
        self.is_property = self._is_property() if is_property is None else is_property
        self.tags = set() if tags is None else set(tags)


    def _is_constructor(self):
        return False

    def _is_disabled(self):
        return False

    def _is_silent(self):
        return False

    def _is_property(self):
        return False

    @property
    def display_name(self):
        return