from jinja2 import Template
import pandas as pd
import random
import ast
import os
import shutil


# get the rankings (can be produced by the analys)
ranking_dir = "../../products/keywords_ranking/"
rankings = os.listdir(ranking_dir)
rankings = [r for r in rankings if "rank" in r]
rankings.sort()
print(rankings)
ranking = rankings[-1]
ranking_path = ranking_dir + ranking
df = pd.read_csv(ranking_path)

# clean output dir
output_dir = ranking_dir + "html/"
shutil.rmtree(output_dir)
os.mkdir(output_dir)

# render the index
with open("./index_template.html") as f:
    index_template = f.read()
    index_template = Template(index_template)

index = df.to_dict("records")
html = index_template.render(jobs=index)
with open(f"{output_dir}/index.html", "w") as text_file:
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
    html_colored = html
    for keyword in match:
        print(f"\"{keyword}\"")
        r = lambda: random.randint(1,255)
        base = [r(), r(), 255]
        random.shuffle(base)
        random_color_str = '{:02X}{:02X}{:02X}'.format(*base)
        print(random_color_str)
        keyword_colored = f'<b style="background-color:#{random_color_str}">{keyword}</b>'
        html_colored = html_colored.replace(keyword, keyword_colored)
    with open(f"{output_dir}/job-{i}.html", "w") as text_file:
        text_file.write(html_colored)
