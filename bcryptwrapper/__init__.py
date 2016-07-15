"""
A programmatic wrapper for the bcrypt commandline utility.

Replicates the full
"""

__version__ = '0.1'


### IMPORTS

import os
import pexpect


### CONSTANTS & DEFINES

# XXX: how good is this? should I use '/usr/local/bin/bcrypt'?
BCRYPT_EXE_PATH = 'bcrypt'



### CODE ###

def _build_cline (paths, exe_path=None, write_to_stdout=False,
		remove_input_files=True, compress_input_files=True, overwrite_times=None):
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
	try:
		child = pexpect.spawnu (cline)
		child.expect ('Encryption key:')
		child.sendline (passwd)
		child.expect ('Again:')
		child.sendline (passwd)
	except Exception as err:
		# TODO: like to get more info from exception
		if 'No valid files found' in err.value:
			raise ValueError ('no valid files found')
		elif 'command not found' in err.value:
			raise OSError ('bcrypt executable not found')
		else:
			raise OSError ('bcrypt call failed')


def encrypt (paths, passwd, rexe_path=exe_path, remove_input_files=True,
		compress_input_files=True, overwrite_times=None):
	## Preparation:
	# check password length
	assert (8 <= len (passwd)), "encryption key must be at least 8 characters"

	# XXX: cehcl file endings?
	
	# do we have a single path or list of paths?
	if isinstance (paths, ''.__class__):
		paths_is_str = True
		paths = [paths]
	else:
		paths_is_str = False

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
	# XXX: try-except in here?
	try:
		child = pexpect.spawnu (cline)
		child.expect ('Encryption key:')
		child.sendline (passwd)
		child.expect ('Again:')
		child.sendline (passwd)
	except Exception as err:
		# TODO: like to get more info from exception
		if 'No valid files found' in err.value:
			raise ValueError ('no valid files found')
		elif 'command not found' in err.value:
			raise OSError ('bcrypt executable not found')
		else:
			raise OSError ('bcrypt call failed')

		# XXX: makes sense to return paths of created files?
		ret_paths = ['%s.bfe' for x in paths]

		## Return:
		# XXX:
		if paths_is_str:
			return ret_paths[0]
		else:
			return ret_paths


def _call_decrypt (cline):
	try:
		child = pexpect.spawnu (cline)
		child.expect ('Encryption key:')
		child.sendline (passwd)
	except Exception as err:
		# TODO: like to get more info from exception
		if 'No valid files found' in err.value:
			raise ValueError ('no valid files found')
		elif 'command not found' in err.value:
			raise OSError ('bcrypt executable not found')
		else:
			raise OSError ('bcrypt call failed')


def decrypt (paths, passwd, rexe_path=exe_path, remove_input_files=True,
		compress_input_files=True, overwrite_times=None):
	## Preparation:
	# check password length
	assert (8 <= len (passwd)), "encryption key must be at least 8 characters"

	# do we have a single path or list of paths?
	if isinstance (paths, ''.__class__):
		paths_is_str = True
		paths = [paths]
	else:
		paths_is_str = False

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
	# XXX: try-except in here?
	try:
		child = pexpect.spawnu (cline)
		child.expect ('Encryption key:')
		child.sendline (passwd)
		child.expect ('Again:')
		child.sendline (passwd)
	except Exception as err:
		# TODO: like to get more info from exception
		if 'No valid files found' in err.value:
			raise ValueError ('no valid files found')
		elif 'command not found' in err.value:
			raise OSError ('bcrypt executable not found')
		else:
			raise OSError ('bcrypt call failed')

		# XXX: makes sense to return paths of created files?
		ret_paths = ['%s.bfe' for x in paths]

		## Return:
		# XXX:
		if paths_is_str:
			return ret_paths[0]
		else:
			return ret_paths





### END ###
