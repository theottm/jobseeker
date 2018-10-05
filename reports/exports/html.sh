#! /bin/bash
file=$1

emacs --batch\
	  -l /home/teddd/.emacs.d/elpa/htmlize-1.53/htmlize.el \
	  -l /home/teddd/.emacs.d/elpa/htmlize-1.53/htmlize.el \
	  $file \
	  --eval "(org-html-export-to-html)" \
