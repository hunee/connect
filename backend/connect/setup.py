#python3 setup.py build_ext --inplace

from setuptools import setup, Extension

ext_modules = [
    Extension(
        'post_c',
        sources=['post_c.pyx'],
        extra_compile_args=['-O3'],
        #extra_compile_args=["-D_GNU_SOURCE"],
        extra_link_args=["-lstdc++", "-lm"],

        include_dirs=['.']
        #define_macros = [('MAJOR_VERSION', '1'),
        #                 ('MINOR_VERSION', '0')],
        #include_dirs = ['/usr/local/include'],
        #libraries = ['tcl83'],
        #library_dirs = ['/usr/local/lib'],        
    )
]

setup(
  ext_modules = ext_modules,
)