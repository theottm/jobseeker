# Initialize the program
First launch the program by running this command in the project root folder.
```shell
python ./jobseeker_launcher.py
```

# Launch the scraper
Check if there is a file named "scraper\_keywords.txt" in data/[your-user-name].
Add keywords to the list. Separate each keyword by a new line. 
Run the commands (in anaconda prompt if you are on Windows):
```shell
cd programms/scraper/indeed_scraper 
python ./scraper_launcher.py
```
This will run a crawl on indeed for every keyword in "scraper\_keywords.txt".


# Rank the results
```shell
cd programms
python ./ranking.py
```

# View the ranking
```shell
cd programms/viewer
python ./html_generator.py
```
open products/html/index.html in a web browser.
