from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='bcryptwrapper',
      version=version,
      description="Programmatic control of bcrypt commandline utility",
      long_description="""\
A quick and dirty library for encrypting files usuing bcrypt. This was prompted by the facts that (a) despite there being several bcrypt libraries for Python, all of them are for password generation and validation, none of them for encryption, and (b) the bcrypt commandline needs the password to  be interactively entered (i.e. typed in) and cannot be passed aon the commandline. Obviously, there's a security angle here, but I'd like to encrypt things within scripts.""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='bcrypt encryption',
      author='Paul Agapow',
      author_email='paul@agapow.net',
      url='http://www.agapow.nnet/software/bcryptwrapper/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
