from setuptools import setup, find_packages

setup(name='sbmtools',
      version='0.1',
      description='''sbmtools is a simple python package for creating, modifying, and 
      maintaining input files for native Structure-Based Model simulations to be used with 
      the popular simulation software GROMACS.''',
      url='https://github.com/c-sinner/sbm-tools',
      author='Claude Sinner',
      author_email='claude.sinner@utdallas.edu',
      license='GPLv3',
      packages=find_packages(),
      zip_safe=False)
