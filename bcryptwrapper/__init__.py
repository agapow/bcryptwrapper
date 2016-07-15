"""
A programmatic wrapper for the bcrypt commandline utility.

Replicates the full bcrypt commandline behaviour.

Along the way, I've discovered a few interesting behaviours:

* bcrypt recognises encrypted files by the extension '.bfe'

* This extension is case-sensitive. '.BFE' won't work.

* When a file is decrypted, the name of the output is just the input with the '.bfe' extension stripped off. That is, if you encrypt 'a.txt', you'll get 'a.txt.bfe'. If you rename this to 'b.txt.bfe' and decrypt it, you'll end up with 'b.txt'. Put another way, the encryption does not preserve the input filename.

* If you use bcrypts send to stdout ability

"""

__version__ = '0.1'


### IMPORTS

import os
import pexpect


### CONSTANTS & DEFINES

# XXX: how good is this? should I use '/usr/local/bin/bcrypt'?
BCRYPT_EXE_PATH = 'bcrypt'



### CODE ###

### Internals

def _build_cline (paths, exe_path=None, write_to_stdout=False,
		remove_input_files=True, compress_input_files=True, overwrite_times=None,
	):
	"""
	Build the commandline for bcrypt.

	Since both encryption and decryption use the same commandline, it's best to
	do it in one place and get it right.
	"""
	## Preparation:
	# prep exe_path
	exe_path = exe_path or BCRYPT_EXE_PATH

	# check password length
	assert (8 <= len (passwd)), "encryption key:Key must be at least 8 characters"

	# overwrite only makes sense if you're removing the input files
	if overwrite_times:
		assert remove_input_files, "overwrite only logical if removing input files"

	# if you direct to stdout, input is never deleted?
	if write_to_stdout:
		assert not remove_input_files, \
			"if writing to stdout, input files cannot be removed"

	# do we have a single path or list of paths?
	if isinstance (paths, ''.__class__):
		paths_is_str = True
		paths = [paths]
	else:
		paths_is_str = False

	## Main:
	# build commandline
	if remove_input_files and compress_input_files and (not write_to_stdout):
		first_arg = ''
	else:
		first_arg_parts = [
			'-',
			'o' if write_to_stdout else '',
			'' if remove_input_files else 'r',
			'' if compress_input_files else 'c',
		]
		first_arg = ''.join (first_arg_parts)

	cline_parts = [
		exe_path,
		first_arg,
		'-s%s' % overwrite_times if overwrite_times else '',
	]
	cline_parts.extend (paths)

	cline = ' '.join (cline_parts)

	## Return:
	print (cline)
	return cline


def _call_encrypt (cline):
	"""
	An internal utility for common calling encryption behaviour.
	"""
	try:
		child = pexpect.spawnu (cline)
		child.expect ('Encryption key:')
		child.sendline (passwd)
		child.expect ('Again:')
		child.sendline (passwd)
	except Exception as err:
		# TODO: like to get more info from exception
		if 'No valid files found' in err.value:
			raise ValueError ('no valid input files found')
		elif 'command not found' in err.value:
			raise OSError ('bcrypt executable not found')
		else:
			raise OSError ('bcrypt call failed')


def _call_decrypt (cline):
	"""
	An internal utility for common calling decryption behaviour.
	"""
	try:
		child = pexpect.spawnu (cline)
		child.expect ('Encryption key:')
		child.sendline (passwd)
	except Exception as err:
		# TODO: like to get more info from exception
		if 'No valid files found' in err.value:
			raise ValueError ('no valid input files found')
		elif 'command not found' in err.value:
			raise OSError ('bcrypt executable not found')
		else:
			raise OSError ('bcrypt call failed')



### Public

def encrypt (paths, passwd, exe_path=exe_path, remove_input_files=True,
		compress_input_files=True, overwrite_times=None,
	):
	"""
	Encrypt a file or files.

	Args:
		paths (str or seq): path or paths of files to be encrypted
		passwd (str): password to use for encryption
		exe_path (str): path to the bcrypt executable
		remove_input_files (bool): should the inputs be deleted after a
			successful encryption
		compress_input_files (bool): should the inputs be comprerssed before
			encryption
		overwrite_times (int): how many times should a to-be-deleted input be
			overwriten

	Returns:
		a list of the paths of the encrypted files

	Raises:
		ValueError: if the input files cannot be found
		OSError: if the executable cannot be found or encryption otherwise fails

	"""
	## Preparation:
	# check password length
	assert (8 <= len (passwd)), "encryption key must be at least 8 characters"

	# do we have a single path or list of paths?
	if isinstance (paths, ''.__class__):
		paths_is_str = True
		paths = [paths]
	else:
		paths_is_str = False

	# check files are named correctly
	for p in paths:
		assert not p.endswith ('.bfe'), "cannot encrypt already encrypted file ends with '.bfe'"

	## Main:
	# build commandline
	cline = _build_cline (paths,
		exe_path=None,
		write_to_stdout=False,
		remove_input_files=remove_input_files,
		compress_input_files=compress_input_files,
		overwrite_times=overwrite_times,
	)

	# run comandline
	_call_encrypt (cline)

	## Return:
	# XXX:
	if paths_is_str:
		return ret_paths[0]
	else:
		return ret_paths

def encrypt_to (in_path, out_path, exe_path=exe_path, remove_input_files=True,
		compress_input_files=True, overwrite_times=None,
	):
	"""
	Encrypt a single file & specify the destination.

	Args:
		in_path (str): path of file to be encrypted
		out_path (str): path of resultant encrypted file
		passwd (str): password to use for encryption
		exe_path (str): see ``encrypt``
		remove_input_files (bool): see ``encrypt``
		compress_input_files (bool): see ``encrypt``
		overwrite_times (int): see ``encrypt``

	Raises:
		ValueError: see ``encrypt``
		OSError: see ``encrypt``

	This uses bcrypt's send to stdout facility. Note this allows you to create an
	encrypted file without the '.bfe' extension that bcrypt requires. Be it on
	your own head.

	"""
	## Preparation:
	# check password length
	assert (8 <= len (passwd)), "encryption key must be at least 8 characters"

	# check files are named correctly
	assert not p.endswith ('.bfe'), \
		"cannot encrypt already encrypted file (ends with '.bfe')"

	## Main:
	# build commandline
	cline = _build_cline (
		[in_path],
		exe_path=None,
		write_to_stdout=True,
		remove_input_files=remove_input_files,
		compress_input_files=compress_input_files,
		overwrite_times=overwrite_times,
	)
	cline = '%s > %s' % (cline, out_path)

	# run comandline
	_call_encrypt (cline)


def decrypt (paths, passwd, rexe_path=exe_path, remove_input_files=True,
		compress_input_files=True, overwrite_times=None):
	"""
	Decrypt a file or files.

	Args:
		paths (str or seq): path or paths of files to be decrypted
		passwd (str): password to use for decryption
		exe_path (str): see ``encrypt``
		remove_input_files (bool): should the inputs be deleted after a
			successful decryption
		compress_input_files (bool): see ``encrypt``
		overwrite_times (int): see ``encrypt``

	Returns:
		a list of the paths of the decrypted files

	Raises:
		ValueError: see ``encrypt``
		OSError: see ``encrypt``

	"""
	## Preparation:
	# check password length
	assert (8 <= len (passwd)), "encryption key must be at least 8 characters"

	# do we have a single path or list of paths?
	if isinstance (paths, ''.__class__):
		paths_is_str = True
		paths = [paths]
	else:
		paths_is_str = False

	# check files are named correctly
	# NOTE: is case-sensitive, '.BFE' doesn't work
	for p in paths:
		assert p.endswith ('.bfe'), "encrypted files must end with '.bfe'"

	## Main:
	# build commandline
	cline = _build_cline (paths,
		exe_path=None,
		write_to_stdout=False,
		remove_input_files=remove_input_files,
		compress_input_files=compress_input_files,
		overwrite_times=overwrite_times,
	)

	# run comandline
	_call_decrypt (cline)

	## Return:
	# XXX:
	if paths_is_str:
		return ret_paths[0]
	else:
		return ret_paths


def decrypt_to (in_path, out_path, passwd, rexe_path=exe_path,
		remove_input_files=True, compress_input_files=True, overwrite_times=None):
	"""
	Decrypt a single file & specify the destination.

	This uses bcrypt's send to stdout facility.

	"""
	## Preparation:
	# check password length
	assert (8 <= len (passwd)), "encryption key must be at least 8 characters"

	# check files are named correctly
	# NOTE: is case-sensitive, '.BFE' doesn't work
	assert in_path.endswith ('.bfe'), "encrypted files must end with '.bfe'"

	## Main:
	# build commandline
	cline = _build_cline (
		[in_path],
		exe_path=None,
		write_to_stdout=True,
		remove_input_files=remove_input_files,
		compress_input_files=compress_input_files,
		overwrite_times=overwrite_times,
	)
	cline = '%s > %s' % (cline, out_path)

	# run comandline
	_call_decrypt (cline)



### END ###
