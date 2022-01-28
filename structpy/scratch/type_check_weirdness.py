from typing import Iterable, Iterator, Protocol, Any

test_value = object()

a: ... = {}  # okay


def foo() -> ...: return test_value


b: ... = foo()  # okay


class BarProtocol(Protocol):
    def bat(self) -> Any: return []


class Bar:
    def bat(self): return test_value


c: BarProtocol = Bar()  # type check error? why?