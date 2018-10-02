#! /bin/bash
emacs --batch \
	  /home/teddd/data/projects/jobseeker/notebooks/jobseeker.org \
	  --eval "(org-latex-export-to-pdf)"
