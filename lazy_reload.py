# Copyright Dave Abrahams 2011
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__author__ = 'Dave Abrahams <dave@boostpro.com>'
__version__ = '1.0'

import sys

# If this module is itself lazy_reload'ed, the following attributes
# will survive until we explicitly overwrite them.
__all__ = ['lazy_reload']

# Are we being reloaded ourselves?
if 'LazyReloader' in globals():
    # remove any existing reloader from sys.meta_path
    sys.meta_path = [ f for f in sys.meta_path if type(f) is not LazyReloader ]
else:
    # The first load must initialize the list of modules to be loaded
    modules_to_reload = {}

def is_submodule_name( name, root_name ):
    return (name + '.').startswith(root_name + '.')

def lazy_reload(root_module):
    """
    If the module (or any of its submodules) has been loaded, the next
    time it is imported, it will first be reloaded.  root_module can
    either be an actual module or the name of a module.
    """
    if isinstance(root_module,type(sys)):
        root_module_name = root_module.__name__
    else:
        root_module_name = root_module

    for k,v in sys.modules.items():
        if v and is_submodule_name(k, root_module_name):
            # save a record of the module
            modules_to_reload[k] = sys.modules.pop(k)

class LazyReloader(object):
    """
    A finder/loader type (see
    http://www.python.org/dev/peps/pep-0302/) that implements our lazy
    reload semantics
    """
    def find_module(self, fullname, path=None):
        if fullname in modules_to_reload:
            return self # we can handle this one
        return None

    def load_module(self, fullname):
        m = modules_to_reload.pop(fullname)

        # stuff the module back in sys.modules
        sys.modules[fullname] = m

        # Toss out any attributes that indicate modules
        #
        # The builtin reload function preserves attributes, just
        # allowing them to be overwritten.  Unfortunately, that means
        # 'from <fullname> import <submodule>' will find the old
        # submodule contents rather than causing a reload.
        module_type = type(sys)
        for k,v in m.__dict__.items():
            if isinstance(v, module_type) \
                    and hasattr(v, '__name__') \
                    and v.__name__.startswith(m.__name__ + '.'):
                del m.__dict__[k]
    
        # Now, a fresh reload
        reload(m)
        return m

sys.meta_path.append(LazyReloader())
