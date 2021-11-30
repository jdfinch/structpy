"""
My thing.
"""

import structpy.system.specification.spec as spec

if __name__ == '__main__':

    # Verify all specs encoded by __main__ module and any submodules
    spec.verify()