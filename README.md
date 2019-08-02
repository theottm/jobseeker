# Installation
## Install python
On Windows and Mac install anaconda. On Linux just install python.
## Which command line to use?
Use anaconda prompt if you are on Windows or mac.
## Navigate to the project's root folder with the command line
```shell
cd path/to/jobseeker
```
## Install the libraries
Open the command line an run :
```shell
cd path/to/jobseeker
pip install -r requirements.txt
```
## Initialize the program
First initialize the program for your computer by running this command in the project's root folder.
```shell
python ./jobseeker_launcher.py
```

# Usage
## Launch the scraper
Check if there is a file named "scraper\_keywords.txt" in data/[your-user-name].
Add keywords to the list. Separate each keyword by a new line.
```shell
cd programms/scraper/indeed_scraper 
python ./scraper_launcher.py
```
This will run a crawl on indeed for every keyword in "scraper\_keywords.txt".


## Rank the results
```shell
cd programms
python ./ranking.py
```

## View the ranking
```shell
cd programms/viewer
python ./html_generator.py
```
open products/html/index.html in a web browser.
