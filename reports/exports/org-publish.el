(require 'ox-publish)
(setq org-publish-project-alist
      '(
        ("notebooks-html"
         :base-directory "/home/teddd/data/projects/jobseeker/notebooks"
         :base-extension "org"
         :publishing-directory "/home/teddd/data/projects/jobseeker/notebooks"
         :recursive nil
         :publishing-function org-html-export-to-html
         :headline-levels 8             ; Just the default for this project.
		 :toc t
		 :auto-preamble t
         )

		("notebooks-pdf"
         :base-directory "/home/teddd/data/projects/jobseeker/notebooks"
         :base-extension "org"
         :publishing-directory "/home/teddd/data/projects/jobseeker/notebooks"
         :recursive nil
         :publishing-function org-latex-export-to-pdf
         :headline-levels 8             ; Just the default for this project.
		 :toc t
		 :auto-preamble t
         )

        ("references-html"
         :base-directory "/home/teddd/data/projects/jobseeker/references"
         :base-extension "org"
         :publishing-directory "/home/teddd/data/projects/jobseeker/references"
         :recursive nil
         :publishing-function org-html-export-to-html
         :headline-levels 8             ; Just the default for this project.
		 :toc t
		 :auto-preamble t
         )

		("references-pdf"
         :base-directory "/home/teddd/data/projects/jobseeker/references"
         :base-extension "org"
         :publishing-directory "/home/teddd/data/projects/jobseeker/references"
         :recursive nil
         :publishing-function org-latex-export-to-pdf
         :headline-levels 8             ; Just the default for this project.
		 :toc t
		 :auto-preamble t
         )

		("notebooks-ipynb"
         :base-directory "/home/teddd/data/projects/jobseeker/notebooks"
         :base-extension "org"
         :publishing-directory "/home/teddd/data/projects/jobseeker/notebooks"
         :recursive nil
         :publishing-function org-latex-export-to-pdf
         :headline-levels 8             ; Just the default for this project.
		 :toc t
		 :auto-preamble t
         )

        ("jobsseker-publish-batch-emacs" :components ("notebooks-html" "notebooks-pdf" "references-html" "references-pdf"))
		("jobsseker-publish-standard-emacs" :components ("notebooks-ipynb"))
        ))
