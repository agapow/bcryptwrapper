from setuptools import setup, find_packages
import sys, os

from bcryptwrapper import __version__ as version

setup (
   name='bcryptwrapper',
   version=version,
   description="Programmatic control of bcrypt commandline utility",
   long_description="""\
A quick and dirty library for encrypting files using bcrypt. This was prompted
by the facts that:

* despite there being several bcrypt libraries for Python, all of them are for
   password generation and validation, none for encryption

* the bcrypt commandline needs the password to be interactively entered (i.e.
   typed in) and cannot be passed on the commandline

I wanted to write some scripts would periodically encrypt and email files, so
obviously there was a gap. Thus I wrote this package to allow bcrypt to be
called from within a script.

Obviously, there's a security angle here (in terms of embedding passwords in a
script ) but I'd like to encrypt things within scripts.
""",
   classifiers=[
      'Development Status :: 4 - Beta',
      'License :: OSI Approved :: MIT License',
      'Operating System :: Unix',
      'Programming Language :: Python',
      'Topic :: Security :: Cryptography',
      'Topic :: Software Development :: Libraries :: Python Modules',
   ],
   keywords='bcrypt encryption',
   author='Paul Agapow',
   author_email='paul@agapow.net',
   url='http://www.agapow.nnet/software/bcryptwrapper/',
   license='MIT',
   packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
   include_package_data=True,
   zip_safe=False,
   install_requires=[
      'pexpect',
   ],
   entry_points="""
      # -*- Entry points: -*-
   """,
)
