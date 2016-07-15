bcryptwrapper
=============

A quick and dirty library for encrypting files using bcrypt.

Background
----------

This was prompted by the facts that:

* despite there being several bcrypt libraries for Python, all of them are for
   password generation and validation, none for encryption

* the bcrypt commandline needs the password to be interactively entered (i.e.
   typed in) and cannot be passed on the commandline

I wanted to write some scripts would periodically encrypt and email files, so
obviously there was a gap. Thus I wrote this package to allow bcrypt to be
called from within a script.

Obviously, there's a security angle here (in terms of embedding passwords in a
script ) but I'd like to encrypt things within scripts.

Examples
--------

Encrypt files from the commandline::

	> import bcryptwrapper as bcw
	> in_files = ['foo.txt', 'bar.txt']
	> encrypt (in_files, password="foobarbaz")
	['foo.txt.bfe', 'bar.txt.bfe']

Decrypt files::

	> import bcryptwrapper as bcw
	> in_files = ['foo.txt.bfe', 'bar.txt.bfe']
	> encrypt (in_files, password="foobarbaz")
	['foo.txt.bfe', 'bar.txt.bfe']
