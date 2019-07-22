import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

from programms.utils.utils import get_project_root
project_root = get_project_root()

from configparser import ConfigParser
import os


 rank():
    # Load the configuration file
    config = ConfigParser()
    config.read(os.path.join(project_root, "config.ini"))
    user = config["general"]["user"]

    from os.path import join as path_join

    data_path = path_join(project_root, "data",  user)
    scraper_data_path = path_join(data_path, "output", "scraper")

    #get the newest dataset
    import os
    # dates_list = os.listdir(scraper_data_path)
    # dates_list.sort()
    # date = dates_list[-1]
    #user_lastdata_path = path_join(user_data_path, date)

    crawls_list = os.listdir(scraper_data_path)
    print(f"Number of crawls : {len(crawls_list)}")

    df = pd.DataFrame()
    for crawl in crawls_list:
        crawl_path = os.path.join(scraper_data_path, crawl)
        crawl_size = os.path.getsize(crawl_path)
        if crawl_size > 0:
            read = pd.read_csv(crawl_path)
            df = df.append(read)
    df.reset_index(inplace=True)

    from humanize import naturalsize
    print(f"Size : {naturalsize(df.size)}")

    df.drop_duplicates(["title", "company"], inplace = True)
    print(f"Size without duplicates : {naturalsize(df.size)}")

    #keywords_list = [crawl.replace(".csv", "").replace("-", " ") for crawl in crawls_list]

    ranking_keywords_file = config["ranking"]["ranking_keywords_file"]
    ranking_keywords_file_path = os.path.join(data_path, ranking_keywords_file)
    ranking_anti_keywords_file = config["ranking"]["ranking_anti_keywords_file"]
    ranking_anti_keywords_file_path = os.path.join(data_path, ranking_anti_keywords_file)

    with open(ranking_keywords_file_path) as f:
        keywords_list_str = f.read()
    keywords_list =  [keyword for keyword in keywords_list_str.split("\n") if keyword != ""]

    with open(ranking_anti_keywords_file_path) as f:
        anti_keywords_list_str = f.read()
    anti_keywords_list =  [keyword for keyword in anti_keywords_list_str.split("\n") if keyword != ""]

    number_of_results = int(config["ranking"]["number_of_results"])

    df["match"] = [[] for i in range(len(df))]
    df["anti_match"] = [[] for i in range(len(df))]

    import re
    for index, desc in df.to_dict()["desc"].items():
        for keyword in keywords_list:
            if  re.search(f"{keyword}", desc, flags=re.I):
                df.loc[index,"match"].append(keyword)
        for anti_keyword in anti_keywords_list:
            if  re.search(f"{anti_keyword}", desc, flags=re.I):
                df.loc[index,"anti_match"].append(anti_keyword)

    df["score"] = df.match.apply(len) - df.anti_match.apply(len)

    high_rank_offers = df.sort_values(by="score", ascending = False).iloc[:number_of_results]

    import time
    localtime   = time.localtime()
    now = time.strftime("%y%m%d-%H%M", localtime)
    csv_file = path_join(project_root, "products", "keywords_ranking", f"ranking.csv")
    high_rank_offers.to_csv(csv_file)
    print(f"Exported : {csv_file}")
