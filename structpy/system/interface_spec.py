
from structpy.system.specification.spec import specification


@specification
class InterfaceSpec:
    """
    Interface wraps an object using composition, but preserving the entire
    public interface of the inner object on the wrapper.

    This allows object-level method overriding without contaminating
    class data.

    Note that the object comparator `is` will not recognize an interface
    as the original (wrapped) object.
    """

    @specification.init
    def I(I, obj):
        """
        Create an interface using `I(obj, **attributes)` notation.
        """
        obj = [1, 2, 3]
        interface = I(
            obj,
            sum=(lambda self: sum(self)),
            append=(lambda self, item: self.extend([item, item]))
        )
        return interface

    def get_attribute(interface, attribute):
        """
        The public interface of the wrapped object is
        represented fully in the interface object.
        """
        assert len(interface) == 3
        assert interface[0] == 1
        assert interface[1] == 2

        assert interface.pop() == 3
        assert len(interface) == 2

        assert interface.sum() == 3
        interface.append(5)
        assert interface == [1, 2, 5, 5]