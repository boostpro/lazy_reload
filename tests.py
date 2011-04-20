import sys
import __builtin__


#
# Record the history of reloads
#
reload_history = []

real_reload = __builtin__.reload
def reload_recorder(module):
    reload_history.append(module.__name__)
    real_reload(module)
__builtin__.reload = reload_recorder

from lazy_reload import *

def assert_reload_history(*l):
    global reload_history
    if tuple(reload_history) != l:
        raise AssertionError, reload_history
    reload_history = []

from lazy_reload import *

# An ordinary import of something already loaded shouldn't cause a
# reload
import lazy_reload as lr
assert_reload_history()

#
# Test that lazy_reload itself can be reloaded
#
lazy_reload('lazy_reload')
# Test that it's actually lazy
assert_reload_history()

import lazy_reload as lr
assert_reload_history('lazy_reload')

lazy_reload('lazy_reload')
from lazy_reload import *
assert_reload_history('lazy_reload')

lazy_reload('lazy_reload')
from lazy_reload import lazy_reload
assert_reload_history('lazy_reload')

#
# Some more complex cases
#
import test.a
assert_reload_history()

import test
assert_reload_history()

lazy_reload('test.a')
import test.b
assert_reload_history()

del test.a
from test import a
assert_reload_history('test.a')

lazy_reload(test)
from test import a
assert_reload_history('test', 'test.a')

#
# Check a case with circular references
#
import test.c
assert test.c.d.test.c is test.c

lazy_reload(test)
import test.c.d
assert_reload_history('test', 'test.c', 'test.c.d')

assert test.c.d.test.c is test.c

#
# Test sibling references
#
from test import e, a
reload_history = []
lazy_reload(test.a)
lazy_reload(test.b)

reload(e)
# e's attempt to directly import a should cause test.a to reload
#
# *However*, e's "from test import b" is not expected to cause test.b
# to be reloaded.  Is this a desired behavior?
assert_reload_history('test.e', 'test.a')

print '****** PASSED ******'
