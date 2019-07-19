from jinja2 import Template
import pandas as pd
import random
import ast
import os
import shutil
from os.path import join as path_join
from configparser import ConfigParser
import re

# find the configuration file of the project
def find_config(dir):
    files = os.listdir(dir)
    if "config.ini" in files:
        dir = os.path.abspath(dir)
        print(f"Found config file at {dir}.")
        return path_join(dir, "config.ini")
    else:
        return find_config(path_join(dir, ".."))
config_path = find_config(".")

# read the config file
config = ConfigParser()
config.read(config_path)
project_root = config["general"]["project_root"]
user = config["general"]["user"]

# get the ranking
ranking_dir = path_join(project_root, "products", "keywords_ranking")
rankings = os.listdir(ranking_dir)
rankings = [r for r in rankings if "rank" in r]
rankings.sort()
ranking = rankings[-1]
ranking_path = path_join(ranking_dir, ranking)
df = pd.read_csv(ranking_path)

# clean output dir
output_dir = path_join(ranking_dir, "html")
shutil.rmtree(output_dir)
os.mkdir(output_dir)

# render the index
with open("./index_template.html") as f:
    index_template = f.read()
    index_template = Template(index_template)

index = df.to_dict("records")
html = index_template.render(jobs=index)
with open(path_join(output_dir, "index.html"), "w", encoding="utf-8") as text_file:
    text_file.write(html) 
    
# render a html file per job
with open("./job_template.html") as f:
    job_template = f.read()
    job_template = Template(job_template)

for i, row in enumerate(df.to_dict("records")):
    i+=1
    desc=row["desc"]
    match=ast.literal_eval(row["match"])
    html = job_template.render(job=row, index=i, limit=len(df), matches=match)
    # color the html
    html_head, html_body = html.split("<body>")
    html_body = "<body>" + html_body
    html_colored = html_body
    for keyword in match:
        r = lambda: random.randint(1,255)
        base = [r(), r(), 255]
        random.shuffle(base)
        random_color_str = '{:02X}{:02X}{:02X}'.format(*base)
        keyword_colored = f'<b style="background-color:#{random_color_str}">{keyword}</b>'
        html_colored = re.sub(keyword, keyword_colored, html_colored, flags=re.I)
    with open(path_join(output_dir, f"job-{i}.html"), "w", encoding="utf-8") as text_file:
        text_file.write(html_head + html_colored)
