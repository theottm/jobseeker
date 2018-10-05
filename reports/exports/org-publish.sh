#! /bin/bash
emacs --batch\
	  -l /home/teddd/.emacs.d/elpa/htmlize-1.53/htmlize.el \
	  -l /home/teddd/.emacs.d/elpa/htmlize-1.53/htmlize.el \
	  -l /home/teddd/data/projects/jobseeker/reports/exports/org-publish.el \
	  --eval '(org-publish-project "jobsseker-publish-batch-emacs")'
