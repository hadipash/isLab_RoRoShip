# -*- coding: utf-8 -*-
from distutils.core import setup, Extension
#from Cython.Distutils import build_ext
import numpy as np
from distutils import msvc9compiler
msvc9compiler.VERSION = 12.0 #윈도우에서는 주석제거 해서 python setup.py install 사용

setup(name='graph_m', version='1.0',  \
      ext_modules=[
	Extension('graph_m', 
	['graph_module.c'], 
	include_dirs=[np.get_include()]
		)
	]
)
#module name, function name, source file name, numpy into c include
