#!usr/bin/env python3
#-*- coding:utf-8 -*-
'fileCopy.py'
__autor__ = 'myth'

from distutils.dir_util import *
from shutil import * #copy2()
import os #path and dir operator
import filecmp #cmp() func
import config

def my_copy_tree(src,dst,symlinks = False):
	errors = []
	if not os.path.exists(dst):
		os.makedirs(dst)
	for name in os.listdir(src):
		srcname = os.path.join(src, name)
		dstname = os.path.join(dst, name)
		try:
			if symlinks and os.path.islink(srcname):
				linkto = os.readlink(srcname)
				if os.path.exists(dstname) and filecmp.cmp(srcname,dstname):
					pass
				else:
					os.symlinks(linkto,dstname)
			elif os.path.isdir(srcname):
				if not os.path.exists(dstname):
					os.mkdir(dstname)
				my_copy_tree(srcname,dstname)
			else:
				if os.path.exists(dstname) and filecmp.cmp(srcname,dstname):
					pass
				else:
					copy2(srcname,dstname)
		except OSError as why:
			errors.append(srcname,dstname,str(why))
		# catch the Error from the recursive copytree so that we can
        # continue with other file
		except Error as err:
			errors.extend(err.args[0])
	try:
		copystat(src,dst)
	except OSError as why:
		#can't copy file access times on Windows
		if why.winerror is None:
			errors.extend((src,dst,str(why)))
	if errors:
		raise Error(errors)

for i in range(min(len(config.fromDir),len(config.toDir))):
	my_copy_tree(config.fromDir[i],config.toDir[i])
	
# #python build-in module implement
# for i in range(min(len(fromDir),len(toDir))):
	# print(fromDir[i],toDir[i])
	# copy_tree(fromDir[i],toDir[i]) 

