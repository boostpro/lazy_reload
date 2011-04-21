The Lazy Python Reloader
========================

This is one way to control what happens when you reload.  Modules are
reloaded in the same order they would be if they were being loaded for
the first time, and for the same reasons, thus eliminating some of the
unpredictability associated with circular module references.

Usage
-----

::

  from lazy_reload import lazy_reload
  import foo.bar.baz
  lazy_reload(foo)
  from foo.bar import baz # <= foo, bar, and baz reloaded here

Motivation
----------

The problems with reloading modules in Python are legion and
well-known.  During the course of ordinary execution, references to
objects in the modules and to the modules themselves end up
distributed around the object graph in ways that can be hard to manage
and hard to predict.  As a result, it's very common to have old code
hanging around long after the reload, possibly referencing things you
expect to have reloaded.  This is not necessarily Python's fault: it's
just a hard problem to solve well.

As a result, most applications that need to update their code
dynamically find a way to start up a new python process for that
purpose. **I strongly recommend you do that if it's an option for
you**; you'll save yourself lots of debugging headaches in the long
run.  For the rest of us, there's ``lazy_reload``.

What Python's ``__builtin__.reload`` Does
-----------------------------------------

The ``reload()`` function supplied by Python is very simple-minded: it
causes the module's source file to be interpreted in the context of
the existing module object.  Any attributes of the module that aren't
overwritten by that interpretation remain in place.  So for example, a
module can detect that it's being reloaded as follows::

    if 'already_loaded' in globals():
        print 'I am being reloaded'
    already_loaded = True

Also, Python makes no attempt to update references to that module
elsewhere in your program.  Because the identity of the module object
doesn't change, direct module references will still work.  However,
any existing references to functions or classes defined within that
module will still point to the old definitions.  Objects created
before the reload still refer to outdated classes via their
``__class__`` attribute, and any local names that have been imported
into other modules still reference their old definitions.

What ``lazy_reload`` Does
-------------------------

``lazy_reload(foo)`` (or ``lazy_reload('foo')``) removes ``foo`` and
all of its submodules from ``sys.modules``, and arranges that the next
time any of them are imported, they will be reloaded.  Before a module
is automatically reloaded, any attributes that are direct submodules
will first be deleted, to prevent some forms of ``import`` from
picking those up instead of reloading the submodule.

What ``lazy_reload`` Doesn't Do
-------------------------------

* It doesn't eliminate references to the reloaded module from other
  modules.  In particular, having loaded this::

        # bar.py
        import foo
        def f():
            return foo.x
        
  the reference to ``foo`` is already present in ``bar``, so after
  ``lazy_unload(foo)``, a call to ``bar.f()`` will not cause ``foo``
  to be reloaded even though it is used there.  Thus, you are safest
  using ``lazy_unload`` on top-level modules that are not known to
  other parts of your program by name.
  
* It doesn't immediately cause anything to be reloaded.  Remember that
  the reload operation is *lazy*, and only happens when the module is
  being imported.

* It also doesn't cause anything to be "unloaded," nor does it do
  anything explicit to reclaim memory.  If the program is holding
  references to functions and classes, don't expect them to be
  garbage-collected.  (Watch out for backtraces; information from the
  last exception raised is one subtle way things can be kept alive
  longer than you'd like).

* It doesn't fold your laundry or wash your cats.  If you don't enjoy
  these activities yourself, consider the many affordable alternatives
  to pets and clothes.

