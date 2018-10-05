import os

org_files = []
for dirpath, dirs, files in os.walk("/home/teddd/data/projects/jobseeker/"): 
  for filename in files:
    fname = os.path.join(dirpath,filename)
    if fname.endswith('.org'):
      if "#" not in fname:
        if "reports" not in fname:
          org_files.append(fname)

from subprocess import Popen, PIPE

def publish_html(org):
    bash_script = ['/home/teddd/data/projects/jobseeker/reports/exports/html.sh']
    command = bash_script + [org]
    session = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    
def publish_pdf(org):
    bash_script = ['/home/teddd/data/projects/jobseeker/reports/exports/pdf.sh']
    command = bash_script + [org]
    session = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()

for org in org_files:
    publish_html(org)
    publish_pdf(org)
