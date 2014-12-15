import sys
from setuptools import setup

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

setup(name='autoscale',
      version="0.0.2",
      description='Extensible library to manage scaling logic and actions',
      author='Mike Babineau',
      author_email='michael.babineau@gmail.com',
      install_requires=[ 'requests>=2.0.0', 'boto>=2.1.0' ],
      url='https://github.com/thefactory/autoscale-python',
      license='MIT',
      platforms='Posix; MacOS X; Windows',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Intended Audience :: System Administrators',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Topic :: Software Development :: Libraries :: Python Modules'],
      **extra
)