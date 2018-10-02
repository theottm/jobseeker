#! /bin/bash
emacs --batch \
	  -l ~/.emacs
	  /home/teddd/data/projects/jobseeker/notebooks/jobseeker.org \
	  --eval "(ox-ipynb-export-to-buffer)(save-file)"
