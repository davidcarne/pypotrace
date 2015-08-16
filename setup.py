#!/usr/bin/env python

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy
import os
import subprocess

have_pkgconfig = False
try:
    import pkgconfig
    have_pkgconfig = True
except ImportError:
    if os.name != 'nt':
        print("If installing on Linux or Mac OS X, the python pkgconfig module is recommended for build.")


# Poor version of pkgconfig package.
def try_lib_named(pkgconfig_name, libname):
    try:
        libs = subprocess.check_output(['pkg-config', '--libs-only-l', pkgconfig_name]).strip().split()
        libs_r = []
        for i in libs:
            i = i.decode('ascii')
            assert i.startswith('-l')
            libs_r.append(i[2:])
        return libs_r
    except subprocess.CalledProcessError:
        return [libname]

if have_pkgconfig:
    potrace_lib = pkgconfig.parse('potrace')['libraries']
    agg_lib = pkgconfig.parse('agg')['libraries']
else:
    agg_lib = try_lib_named('libagg', 'agg')
    potrace_lib = try_lib_named('potrace', 'potrace')

ext_modules = [
        Extension("potrace._potrace", ["potrace/_potrace.pyx"], 
            libraries=potrace_lib, include_dirs=[numpy.get_include()]),
        Extension("potrace.bezier", ["potrace/bezier.pyx"],
            libraries=agg_lib, language="c++", include_dirs=[numpy.get_include()]),
        Extension("potrace.agg.curves", ["potrace/agg/curves.pyx"],
            libraries=agg_lib, language="c++"),
    ]


setup(
    name = "pypotrace",
    author = "Luper Rouch",
    author_email = "luper.rouch@gmail.com",
    url = "http://github.com/flupke/pypotrace",
    description = "potrace Python bindings",
    long_description = open("README.rst").read(),
    version = "0.1.2+dcpatch",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
    ],

    packages = ["potrace", "potrace.agg"],
    ext_modules = ext_modules,
    cmdclass = {"build_ext": build_ext},
)
