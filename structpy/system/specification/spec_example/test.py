
from structpy.system.specification import spec
import structpy.system.specification.spec_example as spec_example
import structpy.system.specification.spec_example.bar_spec as bar

if __name__ == '__main__':
    # Collect all specifications in subpackage and test
     spec.verify(bar)

