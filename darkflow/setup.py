from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize
import numpy
import os

# Define the Cython extensions
# These modules will be compiled from .pyx to .c files and then to binaries
ext_modules = [
    Extension(
        "darkflow.cython_utils.nms",
        sources=["darkflow/cython_utils/nms.pyx"],
        include_dirs=[numpy.get_include()],
        libraries=["m"] if os.name == 'posix' else []
    ),
    Extension(
        "darkflow.cython_utils.cy_yolo2_findboxes",
        sources=["darkflow/cython_utils/cy_yolo2_findboxes.pyx"],
        include_dirs=[numpy.get_include()],
        libraries=["m"] if os.name == 'posix' else []
    ),
    Extension(
        "darkflow.cython_utils.cy_yolo_findboxes",
        sources=["darkflow/cython_utils/cy_yolo_findboxes.pyx"],
        include_dirs=[numpy.get_include()],
        libraries=["m"] if os.name == 'posix' else []
    )
]

setup(
    name='darkflow',
    version='1.0',
    description='A TensorFlow wrapper for Darknet YOLO models',
    license='GPLv3',
    url='https://github.com/thtrieu/darkflow',
    packages=find_packages(),
    scripts=['flow'],
    ext_modules=cythonize(ext_modules)
)