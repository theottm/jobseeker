import subprocess as sp 
import shlex
import numpy as np
import asyncio
import time
import os
import argparse
import shutil
from configparser import ConfigParser
from os.path import join as path_join


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

# read keywords file
user_data_path = path_join(project_root, "data", user)
keywords_file = path_join(user_data_path, "scraper_keywords.txt")


# define parser with command line arguments
parser = argparse.ArgumentParser(description='Launches many scrapers.')
parser.add_argument("-f", "--file", nargs="?", type=str, default=keywords_file,
                    help="A plain text file with a keyword per line", metavar="txt")
parser.add_argument("-l", '--limit', nargs="?", default=20, type=int,
                    help="Maximum number of scrapers that can run at the same time.", metavar="N")
args = parser.parse_args()


# read the keywords list
with open(args.file) as f:
    keywords_text = f.read()
# remove stackedit tag
keywords_text = keywords_text.split("<")[0]
keywords_list = keywords_text.split("\n")
# remove empty lines
keywords_list = [keyword for keyword in keywords_list if keyword != "" and "stackedit" not in keyword]
# remove trailing whitespaces
keywords_list = [keyword if keyword[-1] != " " else keyword[:-1] for keyword in keywords_list]
print(f"{keywords_list}")
print(f"Number of keywords: {len(keywords_list)}")


# prepare data output folders
ongoing_dir = path_join(user_data_path, "output", "scrapers", "ongoing")
done_dir = path_join(user_data_path, "output", "scrapers", "done")
try:
    os.makedirs(done_dir)
except FileExistsError:
    pass
try:
    shutil.rmtree(ongoing_dir)
    os.mkdir(ongoing_dir)
except FileNotFoundError:
    os.makedirs(ongoing_dir)


# define a crawl function that will be launched by asyncio
async def crawl(keyword, semaphore):
    async with semaphore:
        file_name = f"{keyword.replace(' ','-')}.csv"
        output_ongoing = path_join(ongoing_dir, file_name)
        output_done = path_join(done_dir, file_name)
        print(f"Starting: {keyword}")
        if not os.path.isfile(output_done):
            cmd = ['scrapy', "crawl", "france", "-a", f'query="{keyword}"', "-a", 'location="Paris"', "-a", 'country="fr"', "-o", output_ongoing]
            #cmd = ["touch", 'output/"{}".csv'.format(keyword)]
            cmd = " ".join(cmd)
            print(f"Running : {cmd}")
            proc = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await proc.communicate()
            # move file to a specific folder when done
            try:
                print(f"Done: {keyword}")
                os.rename(output_ongoing, output_done)
            except FileNotFoundError:
                print("{} stderr: length {}".format(cmd, stderr.decode()))
                raise 
            if stdout:
                print("stdout: length: {}".format(len(stdout.decode())))
            if stderr:
                print("stderr: length {}".format(len(stderr.decode())))
        else:
            print(f"{file_name} already exists, skipping.")


max_parallel = int(args.limit)
print(f"Maximum  number of simultaneously active spiders: {max_parallel}")

async def main():
    tasks = []
    # instantiate a semaphore before calling our coroutines
    semaphore = asyncio.BoundedSemaphore(max_parallel)
    for keyword in keywords_list:
        # pass the semaphore to the coroutine that will limit itself
        tasks.append(asyncio.ensure_future(crawl(keyword, semaphore)))
    await asyncio.gather(*tasks)

if sys.platform == "win32":
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()
loop.set_debug(True)
ids = loop.run_until_complete(main())
