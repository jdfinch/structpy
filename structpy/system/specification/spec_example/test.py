
from structpy.system.specification import spec
import structpy.system.specification.spec_example as spec_example

if __name__ == '__main__':
    # Collect all specifications in subpackage and test
    spec.verify(spec_example)

