
from structpy import specification


other = None

@specification
class EnforcerDictSpec:
    """
    An extension of python `dict` with enforcment hooks that call functions
    whenever items are added/overwritten or removed/overwritten.
    """

    @specification.init
    def ENFORCER_DICT(EnforcerDict, dict_like=None, add_function=None, remove_function=None):
        """
        Build a dictionary with enforcement hooks.

        `add_function(added)` is a function that is called whenever a new (or replacement)
        key:value pair is added, and it should expect `added` to be a `iterable<tuple<key, value>>`
        as an argument. The return of `add_function(added)` should be an `iterable<tuple<key, value>>`,
        which represent the entries that will actually be added to the `enforcer_dict` object.

        `remove_function(removed)` is a function that is called whenever a key:value pair
        is removed  (including those overwritten by new value), and it should expect `removed` to be
        `iterable<tuple<key, value>>` as an argument. The return of `remove_function(removed)` should
        be an `iterable<tuple<key, value>>` which represents the entries that will actually be removed
        from the `enforcer_dict` object.
        """
        class Other:
            def __init__(self):
                self.keystring = ''
                self.valuesum = 0
            def add_function(self, items):
                for key, value in items:
                    self.valuesum += value
                    self.keystring += key
            def remove_function(self, items):
                for key, value in items:
                    self.valuesum -= value
                    self.keystring = self.keystring.replace(key, '')

        global other
        other = Other()

        enforcer_dict = EnforcerDict(
            dict(a=1, b=2, c=3),
            add_function=other.add_function,
            remove_function=other.remove_function
        )
        return enforcer_dict

    def add(enforcer_dict, key, value):
        """
        Adding or replacing key-value pairs in the enforcer dict results in a call
        to `add_function(pairs)` where `pairs` is an
        iterable<tuple<key, value>> of all newly added key-vlaue pairs.
        """
        enforcer_dict['d'] = 4
        assert other.keystring == 'abcd'
        assert other.valuesum == 10

        enforcer_dict.update(dict(e=5, f=6))
        assert other.keystring == 'abcdef'
        assert other.valuesum == 21

    def remove(enforcer_dict, key):
        """
        Removing or overwriting key-value from the enforcer dict results in a call
        to `remove_function(pairs)` where `pairs` is an
        iterable<tuple<key, value>> of all removed/overwritten key-value pairs.
        """
        del enforcer_dict['f']
        assert other.keystring == 'abcde'
        assert other.valuesum == 15

        enforcer_dict['a'] = 2
        assert other.keystring == 'bcdea'
        assert other.valuesum == 16

        enforcer_dict.clear()
        assert other.keystring == ''
        assert other.valuesum == 0


    @specification.init
    def ENFORCEMENT_FUNCTIONS_AS_MODIFIERS(EnforcerDict):
        """
        Enforcement functions `add_function` and `remove_function` can
        modify items added/removed by returning an updated items iterable.
        """

        class Other:
            def __init__(self):
                self.keystring = ''
                self.valuesum = 0
            def add_function(self, items):
                for key, value in items:
                    if value % 2 == 0 and key.islower():
                        self.valuesum += value
                        self.keystring += key
                        yield key, value
            # noinspection PyUnreachableCode
            def remove_function(self, items):
                return
                yield

        global other
        other = Other()

        enforcer_dict = EnforcerDict(
            dict(A=1, b=2, c=3, D=4),
            add_function=other.add_function,
            remove_function=other.remove_function
        )

        assert other.keystring == 'b'
        assert other.valuesum == 2

        del enforcer_dict['b']

        assert other.keystring == 'b'
        assert other.valuesum == 2

        return enforcer_dict












