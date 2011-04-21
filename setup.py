from distutils.core import setup

version = __import__('lazy_reload').__version__

setup(
    name = 'lazy-reload',
    version = version,
    description = 'The Lazy Python Reloader',
    author = 'Dave Abrahams',
    author_email = 'dave@boostpro.com',
    license = "Boost License 1.0",
    url = "http://github.com/boostpro/lazy_reload",
    classifiers = ['Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python'],
    py_modules = ['lazy_reload'],
    long_description = open('README.rst').read(),
)
