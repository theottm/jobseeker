#! /bin/bash
emacs --batch\
	  -l /home/teddd/.emacs.d/elpa/htmlize-1.53/htmlize.el \
	  -l /home/teddd/.emacs.d/elpa/htmlize-1.53/htmlize.el \
	  /home/teddd/data/projects/jobseeker/notebooks/jobseeker.org \
	  --eval "(org-html-export-to-html)" \
