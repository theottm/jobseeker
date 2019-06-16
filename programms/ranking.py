import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from utils.utils import get_project_root
project_root = get_project_root()

from configparser import ConfigParser
import os

# Load the configuration file
config = ConfigParser()
config.read(os.path.join(project_root, "config.ini"))
user = config["general"]["user"]

from os.path import join as path_join

scraper_data_path = path_join(project_root, "data",  user, "output", "scraper")
print("scraper_data_path")
print(scraper_data_path)

#get the newest dataset
import os
# dates_list = os.listdir(scraper_data_path)
# dates_list.sort()
# date = dates_list[-1]
#user_lastdata_path = path_join(user_data_path, date)

crawls_list = os.listdir(scraper_data_path)

df = pd.DataFrame()
for crawl in crawls_list:
    crawl_path = os.path.join(scraper_data_path, crawl)
    crawl_size = os.path.getsize(crawl_path)
    if crawl_size > 0:
        read = pd.read_csv(crawl_path)
        df = df.append(read)
df.reset_index(inplace=True)

df.drop_duplicates(["title", "company"], inplace = True)

keywords_list = [crawl.replace(".csv", "").replace("-", " ") for crawl in crawls_list]
NUMBER_OF_RESULTS = 200

df["match"] = [[] for i in range(len(df))]

import re
for keyword in keywords_list:
    for index, desc in df.to_dict()["desc"].items():
        if  re.search(keyword, desc, flags=re.I):
            df.loc[index,"match"].append(keyword)

df["score"] = df.match.apply(len)

high_rank_offers = df.sort_values(by="score", ascending = False).iloc[:NUMBER_OF_RESULTS]

import time
localtime   = time.localtime()
now = time.strftime("%y%m%d-%H%M", localtime)
csv_file = path_join(project_root, "products", "keywords_ranking", f"ranking.csv")
high_rank_offers.to_csv(csv_file)
print(csv_file)
