import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PROJECT_ROOT = "/home/teddd/data/projects/jobseeker2019"
usr = "cyborgab"

project_data_path = PROJECT_ROOT + "/data/" 
usr_data_path = project_data_path + usr + "/"

#get the newest dataset
import os
dates_list = os.listdir(usr_data_path)
dates_list.sort()
date = dates_list[-1]
usr_lastdata_path = usr_data_path + date + "/"

crawls_list = os.listdir(usr_lastdata_path)

df = pd.DataFrame()
for crawl in crawls_list:
    crawl_path = usr_lastdata_path + crawl
    crawl_size = os.path.getsize(crawl_path)
    if crawl_size > 0:
        read = pd.read_csv(crawl_path)
        df = df.append(read)
df.reset_index(inplace=True)

df.drop_duplicates(["title", "company"], inplace = True)

keywords_list = [crawl.replace(".csv", "").replace("-", " ") for crawl in crawls_list]
NUMBER_OF_RESULTS = 200

df["match"] = [[] for i in range(len(df))]

for keyword in keywords_list:
    for index, desc in df.to_dict()["desc"].items():
        if keyword in desc:
            df.loc[index,"match"].append(keyword)

df["score"] = df.match.apply(len)

high_rank_offers = df.sort_values(by="score", ascending = False).iloc[:NUMBER_OF_RESULTS]

import time
localtime   = time.localtime()
now = time.strftime("%y%m%d-%H%M", localtime)
csv_file = PROJECT_ROOT + f"/products/keywords_ranking/{now}-rank.csv"
high_rank_offers.to_csv(csv_file)
print(csv_file)
