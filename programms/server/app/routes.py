from app import app
from flask import render_template, request

from urllib.parse import urlparse, parse_qs
import subprocess as sp 
import shlex
import re

from jobseeker_server import *
from os.path import join as path_join
import os
from configparser import ConfigParser
import pandas as pd
import ast

# find the configuration file of the project
def find_config(dir):
    files = os.listdir(dir)
    if "config.ini" in files:
        dir = os.path.abspath(dir)
        print(f"Found config file at {dir}.")
        return os.path.join(dir, "config.ini")
    else:
        return find_config(os.path.join(dir, ".."))
config_path = find_config(".")

# read the config file
config = ConfigParser()
config.read(config_path)
project_root = config["general"]["project_root"]
user = config["general"]["user"]


@app.route("/jobs", methods=["GET"])
def index():
    # get the ranking
    ranking_dir = path_join(project_root, "products", "keywords_ranking")
    rankings = os.listdir(ranking_dir)
    rankings = [r for r in rankings if "rank" in r]
    rankings.sort()
    ranking = rankings[-1]
    ranking_path = path_join(ranking_dir, ranking)
    df = pd.read_csv(ranking_path)
    index = df.to_dict("records")
    return render_template("index_template.html",jobs=index)

@app.route("/jobs/<int:job_index>", methods=["GET"])
def job(job_index):
    ranking_dir = path_join(project_root, "products", "keywords_ranking")
    rankings = os.listdir(ranking_dir)
    rankings = [r for r in rankings if "rank" in r]
    rankings.sort()
    ranking = rankings[-1]
    ranking_path = path_join(ranking_dir, ranking)
    df = pd.read_csv(ranking_path)
    row = df.to_dict("records")[job_index]
    match=ast.literal_eval(row["match"])
    return render_template("job_template.html",
                           job=row, index=job_index, limit=len(df), matches=match)

@app.route("/", methods=["GET", "POST"])
def front():
    query_string = urlparse(request.url).query

    # Define default parameters to send the html.
    # If there is a query, parameters change accordingly. 
    html_param = {"keywords" : "TODO",
                 "case" : "",}

    results = {}
    
    if query_string:
        query_dict = parse_qs(query_string)

        # get case sensitivity option from the query
        case = "-s" if "case" in query_dict else "-i" 
        html_param["case"] = "checked" if "case" in query_dict else ""

        if "keywords" in query_dict:

            # get keywords from the query
            keywords_string = query_dict["keywords"][0]
            html_param["keywords"] = keywords_string
            print("Keywords string: \"{}\"".format(keywords_string))

            # Parse keywords.
            keywords_list = keywords_string.split()
            # Add whitespaces with with help of "+"
            keywords_list = [k.replace("+", " ") for k in keywords_list]
            # Parse negative and positive keywords
            keywords_positive = [k for k in keywords_list if "-" != k[0]]
            keywords_negative = [k[1:] for k in keywords_list if "-" == k[0]]

            print("Parsed keywords: {}".format(keywords_list))
            print("Positiv search: {}".format(keywords_positive))
            print("Negative search: {}".format(keywords_negative))

            # check if a positive keyword is present
            if not keywords_positive:
                error = "You must give at least one positive search keyword."
                return render_template("base.html",
                                       param=html_param,
                                       msg=error)

            # run ag search for the first positive keyword        
            print("Search for: \"{}\"".format(keywords_positive[0]))
            cwd="/home/teddd/Dropbox/org-mode"
            cmd = ['ag', '-r', case, '-F', '{}'.format(keywords_positive[0]), cwd]
            proc = sp.Popen(cmd, shell=False, stdout=sp.PIPE, stderr=sp.PIPE)
            print("Command arguments: {}".format(proc.args))

            # Filter results.
            # With remaining positive keywords, run grep commands on previous stdout through a pipe.
            if len(keywords_positive) > 1:
                for k in keywords_positive[1:]:
                    print("Positive filter for: \"{}\"".format(k))
                    cmd = ['grep', "-F", case, k]
                    proc = sp.Popen(cmd, shell=False, stdin=proc.stdout, stdout=sp.PIPE, stderr=sp.PIPE)
                    print("Command arguments: {}".format(proc.args))

            # Filter results.
            # With remaining negative keywords, run inverted grep commands on previous stdout through a pipe.
            if keywords_negative:
                for k in keywords_negative:
                    print("Negative filter for: \"{}\"".format(k))
                    cmd = ['grep', "-F", "-v", case, k]
                    proc = sp.Popen(cmd, shell=False, stdin=proc.stdout, stdout=sp.PIPE, stderr=sp.PIPE)
                    print("Command arguments: {}".format(proc.args))

            # get relevant outputs of the commands pipeline
            process_output = proc.communicate()
            print(type(process_output[0]))
            process_output_dict = {"returncode": proc.returncode,
                                   "results": process_output[0].decode('utf-8', errors="ignore"),
                 "stderr": process_output[1]}
            print("Return code: {}".format(process_output_dict["returncode"]))

            # parse and format result output
            results = process_output_dict["results"].split("\n")[:-1]
            results = [{"file": r.split(":")[0].replace(cwd, ""),
                  "line": r.split(":")[1],
                  "excerpt": ":".join(r.split(":")[2:])} for r in results if len(r.split(":")) > 1]

    # send variables to the jinja html render
    return render_template("base.html",
                           title="Documentation Search Engine",
                           param=html_param,
                           results=results,
                           len=len(results))
