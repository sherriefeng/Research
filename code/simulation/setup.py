from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

ext_modules = [Extension("divisionGame", ["divisionGame.pyx"], include_dirs=[numpy.get_include()])]

setup(
  name = 'Num Solutions app',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules,
  include_dirs = [numpy.get_include()]
)