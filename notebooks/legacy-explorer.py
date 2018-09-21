import pandas as pd
from html2text import html2text
from bs4 import BeautifulSoup
import math
import numpy as np
import os
import re
# from functions import write_text

# jobs = pd.read_csv("/home/teddd/code/web/scraping/udemy-class/indeed/software engineer.csv")
# jobs.desc = jobs.desc.map(html2text)
pd.options.display.max_colwidth = 5000

csv_files = []
dir_files = os.listdir()
for fl in dir_files:
    if re.search('[.]csv', fl, re.I) is not None:
        csv_files.append(fl)

jobs = pd.DataFrame()

for fl in csv_files:
    print(fl+(30-len(fl)//2)*" *")
    jobs_set = pd.read_csv(fl)
    jobs_set.dropna(axis=0, how='any', subset=["desc"], inplace=True)
    jobs_set.drop_duplicates(subset="desc", inplace=True)
    try:
        jobs.iloc[0,0]
        jobs = jobs.append(jobs_set)
    except IndexError:
        jobs = jobs_set

jobs.drop_duplicates(subset="desc", inplace=True)

# german entries :
# jobs[jobs.desc.str.contains("ä") | jobs.desc.str.contains("ü") | jobs.desc.str.contains(",und ") | jobs.desc.str.contains("ö")].count()

# junior_no_degrees_recent = jobs[(jobs.desc.str.contains("degree", case=False).map(lambda x: not x) & jobs.desc.str.contains("junior", case=False) & jobs.days_ago.str.contains("30+").map(lambda x: not x))]
# junior = jobs.loc[jobs.desc.str.contains("junior", case=False) | jobs.title.str.contains("junior", case=False)]


def souper(html):
    soup = BeautifulSoup(html, 'html.parser')
    print(soup.get_text())


def soupprint(df, begin, end):
    for i in range(begin, end):
        print(i, df.title.iloc[i])
        print("\n")
        print(df.company.iloc[i])
        print("\n")
        souper(df.desc.iloc[i])
        print("\n"*3)
        print("-"*100)
        print("\n"*3)


"""
sorter tryout

read : pandas.core.sorting.py (get_group_index) [[file:~/code/web/scraping/udemy-class/pyenv/lib/python3.5/site-packages/pandas/core/sorting.py::def%20get_group_index(labels,%20shape,%20sort,%20xnull):][get group index]]

read : pandas.core.frame.py (duplicated) [[file:~/code/web/scraping/udemy-class/pyenv/lib/python3.5/site-packages/pandas/core/frame.py::def%20duplicated(self,%20subset=None,%20keep='first'):][duplicated]]

i = 0
j = 0
while i < len(jobs):
    print(i, 20*"-")
    while j < len(jobs)-(i+1):
        if jobs.title.iloc[i] == jobs.title.iloc[i+1+j]:
            if jobs.company.iloc[i] == jobs.company.iloc[i+1+j]:
                jobs = jobs.drop(index=i+j+1)
                print(i+j+1)
        else:
            j += 1
    i += 1

for i in range(100):
    for j in range(100-i-1):
        print(i,i+j+1)
"""

"""
predictive model to determine job titles words more likely to hide a junior position

variables : list of all words in all titles. (bool : presence or not)

create a subset based on the word criterium

evaluate the entropy of this subset

evaluate probability of this subset

give an IG (info gain) for the word

todo:
-data cleansing on title parenthisis, case
- data cleansing on doubles
"""

def multi_replace(string, *args, replace=""):
    for target in args:
        string = string.replace(target, replace)
    return string

trash_car = (",", "\'", "\"", "&", "#", "{", "}",
             "(", ")", "[", "]", "_", "\\", "~", "-",
             ",", ";", ":", ".", "?", "!", "+", "|",
             "@", "/", "–", "*", "“", "„", "%", " ",
             "€")



# one way of calculating entrpy and info gain


# def lol(*args, fun="lol"):
#     for laugh in args:
#         print(laugh, fun)

# title_words = ["berlin"]
# words_occurences = {}
# for ttl in jobs.title:
#     ttl = multi_replace(ttl, *trash_car, replace=" ")
#     ttl = ttl.lower()
#     for word in ttl.split(" "):
#         if len(word) > 2:
#             if word in words_occurences:
#                 words_occurences[word] += 1
#             else:
#                 words_occurences[word] = 1
#             if word not in title_words:
#                 title_words.append(word)

# def entropy(p):
#     if p == 0:
#         entropy = 0
#     else:
#         entropy = - p * math.log2(p)
#     return entropy


# root_target_probability = jobs.loc[jobs.desc.str.contains("junior", case=False) |
#              jobs.title.str.contains("junior", case=False)].desc.count() /jobs.desc.count()
# root_entropy = entropy(root_target_probability)


# words_target_probability = {}
# words_subsets_entropies = {}
# words_anti_subsets_entropies = {}
# words_subsets_probabilities = {}
# words_anti_subsets_probabilities = {}
# words_info_gain = {}

"""
for word in title_words:
    print(word+(30-len(word)//2)*" *")
    subset = jobs.loc[jobs.title.str.contains(word, case=False)]
    anti_subset = jobs.loc[jobs.title.str.contains(word, case=False).map(lambda x: not x)]
    target_occurences = subset.loc[subset.desc.str.contains("junior", case=False) |
                                   subset.title.str.contains("junior", case=False)].desc.count()
    anti_target_occurences = anti_subset.loc[anti_subset.desc.str.contains("junior", case=False) |
                                   anti_subset.title.str.contains("junior", case=False)].desc.count()
    subset_lenght = subset.desc.count()
    anti_subset_lenght = anti_subset.desc.count()
    target_probability = target_occurences/subset_lenght
    words_target_probability[word] = target_probability
    anti_target_probability = anti_target_occurences/anti_subset_lenght
    words_subsets_entropies[word] = entropy(target_probability)
    words_anti_subsets_entropies[word] = entropy(anti_target_probability)
    words_subsets_probabilities[word] = words_occurences[word] / jobs.desc.count()
    words_anti_subsets_probabilities[word] = 1 - words_occurences[word] / jobs.desc.count()
    words_info_gain[word] = root_entropy - (words_subsets_probabilities[word] * words_subsets_entropies[word] + words_anti_subsets_probabilities[word] * words_anti_subsets_entropies[word])


# word = pd.DataFrame(title_words)
# word = word.rename(columns={0:"word"})
# word = word.set_index(["word"])
# word_occ = pd.DataFrame.from_dict(words_occurences, orient='index')
# word_occ.rename(columns={0:"occurences"}, inplace=True)
# word = word.join(word_occ)
# word_ig = pd.DataFrame.from_dict(words_info_gain, orient='index')
# word_ig.rename(columns={0:"info gain"}, inplace=True)
# word = word.join(word_ig)
# word_tar_prob = pd.DataFrame.from_dict(words_target_probability, orient='index')
# word_tar_prob.rename(columns={0:"target probability"}, inplace=True)
# word = word.join(word_tar_prob)
# word.sort_values("info gain", ascending=False)
# word.sort_values(["target probability", "info gain"], ascending=False)
"""
"""
TEST :
subset = jobs.loc[jobs.title.str.contains(word)]
target_occurences = subset.loc[jobs.desc.str.contains("junior", case=False) | jobs.title.str.contains("junior", case=False)].desc.count()
subset_lenght = subset.desc.count()
target_probability= target_occurences/subset_lenght
entropy = - target_probability* math.log2(p)
word_entropies[word] = entropy
"""


"""
Words relationships with other jobs and other words :

TODO

apply filters :
- low number of occurences
- numbers
- current english/german words

print most used words and their relatives
print 2 generations of relatives for one word
implement for descriptions (oop?)
print node and its relatives in a star rep (org mode )
"""

# For titles :

words_jobs = {}
for i in range(len(jobs)):
    job = jobs.iloc[i]
    print(job.title+(30-len(job.title)//2)*" *")
    # for word in jobs.iloc[i].desc.str.split
    ttl = multi_replace(job.title, *trash_car, replace=" ")
    ttl = ttl.lower()
    for word in ttl.split(" "):
        if len(word) > 2:
            if word in words_jobs.keys():
                if i in words_jobs[word].keys():
                    words_jobs[word][i] += 1
                else:
                    words_jobs[word][i] = 1
            else:
                words_jobs[word] = {i:1}

"""
# For descriptions :

words_jobs = {}
for i in range(len(jobs)):
    job = jobs.iloc[i]
    print(job.title+(30-len(job.title)//2)*" *")
    # for word in jobs.iloc[i].desc.str.split
    ttl = multi_replace(job.desc, *trash_car, replace=" ")
    ttl = ttl.lower()
    for word in ttl.split(" "):
        if len(word) > 2:
            if word in words_jobs.keys():
                if i in words_jobs[word].keys():
                    words_jobs[word][i] += 1
                else:
                    words_jobs[word][i] = 1
            else:
                words_jobs[word] = {i:1}
"""

words_jobs_df = pd.DataFrame(words_jobs, dtype=int)
words_jobs_df.fillna(0, inplace=True)

def booleanize(threshold ,int):
    if int > threshold:
        return True
    else:
        return False

words_jobs_df_bool = words_jobs_df.applymap(lambda x: booleanize(0, x))


def related(word_list):
    for word in word_list:
        yield words_jobs_df[words_jobs_df_bool.loc[:,word]].sum().sort_values()

words_words = pd.DataFrame(related(list(words_jobs_df.keys())))
words_words = words_words.set_index(words_words.keys())

for i in range(len(words_words)):
    for j in range(len(words_words)):
        if i == j :
            words_words.iloc[i,j] = 0

words_words.loc[(words_words.sum() > 10)]
wwb = words_words.applymap(lambda x: booleanize(0, x))

def close_relatives(word, number):
    return list(words_words.loc[word].sort_values().keys()[-number:])


def n_relatives(word, number, degree):
    lst = close_relatives(word, number)
    final_lst = {}
    final_lst[0] = {word: lst}
    for i in range(1, degree+1):
        new_lst = {}
        for word in lst:
            new_lst[word] = close_relatives(word, number)
        final_lst[i] = new_lst
        lst = []
        for val in new_lst.values():
            lst += val
    return final_lst

# clustering
"""
1. TFIDF (Term Frequency times Invert Document Frequency)
2. Cosine similarity x*y / ||x||2 . ||y||2
"""

words_jobs_tfidf = words_jobs_df
for i in range(words_jobs_df.shape[1]):
    print(words_jobs_tfidf.keys()[i])
    summ = words_jobs_tfidf.iloc[:,i].sum()
    if summ != 1 :
        words_jobs_tfidf.iloc[:,i] = words_jobs_df.iloc[:,i]/summ

distance_to_orig = {}
words_jobs_tfidf_squared = words_jobs_tfidf.applymap(lambda x: x**2)
for i in range(words_jobs_tfidf.shape[0]):
    distance_to_orig[i] = math.sqrt(words_jobs_tfidf_squared.iloc[i].sum())

jobs_jobs_similarity = {}
for i in range(words_jobs_tfidf.shape[0]):
    jobs_jobs_similarity[i] = {}
    for j in range(i+1, words_jobs_tfidf.shape[0]):
        scalar_product = (words_jobs_tfidf.iloc[i] * words_jobs_tfidf.iloc[j]).sum()
        similarity = scalar_product / distance_to_orig[i] * distance_to_orig[j]
        jobs_jobs_similarity[i][j] = similarity
        print("job #{0} and job #{1} have {2} similarity rate".format(i, j, similarity))


"""
TODO

* write a whole program
* use unit testing
* input : kaggle datasets ?
* use jupyter for communication
* data cleansing
* add init arguments : open all queries if none
* class for jobs : Job
* store in a relational database : postgresql
* show each A/B job on one side of the screen
*

REMINDER :

Sebastian Gutierrez Method for producing a data analysis :
1. input
2. store
3. extract
4. organize
5. tidy
6. transform
7. vizualise
8. model
9. code
10. understand
11. communicate
12.
13. document
"""
