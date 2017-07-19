from distutils.core import setup, Extension
from Cython.Distutils import build_ext
import numpy as np

setup(name='graph_m', version='1.0',  \
      ext_modules=[
	Extension('graph_m', 
	['graph_module.c'], 
	include_dirs=[np.get_include()]
		)
	]
)
#module name, function name, source file name, numpy into c include