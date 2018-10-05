#! /bin/bash
file=$1

emacs --batch \
	  $file \
	  --eval "(org-latex-export-to-pdf)"
