# Initialize the program
First launch the program by running this command in the project root folder.
```shell
python ./jobseeker_launcher.py
```

# Launch the scraper
Check if there is a file named "scraper_keywords.txt" in data/[your-user-name]
Navigate to programms/scraper/indeed_scraper and run the command (in anaconda prompt if you are on Windows):
```shell
python ./scraper_launcher.py
```
This will run a crawl on indeed for every keyword you gave in.


# Rank the results
```shell
cd programms
python ./ranking.py
```

# View the results
```shell
cd programms/viewer
python ./html_generator.py
```
open products/html/index.html in a web browser.
