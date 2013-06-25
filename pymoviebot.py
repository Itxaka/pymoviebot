# -*- coding: utf-8 -*-

"""
pymoviebot.py
Copyrigth 2013 Itxaka Serrano <itxakaserrano@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


This code works in conjuntion with database.py
"""
import urllib
if urllib.getproxies()['http'] == "":
    print "No proxies"
else:
    with open("praw.ini", "w") as f:
        f.write("[reddit]\n")
        f.write("http_proxy = " + urllib.getproxies()['http'])

import praw
import time
import sqlite3
import logging
import requests
import config

# logging parameters below
logging.basicConfig(filename=config.path + 'pymoviebot.log',level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
logging.info("Program Start")

user_agent = ("pymoviebot 1.1 by /u/itxaka") # API guidelines suggest this
already_done = []  # the ones we have submitted the comment to go here

def getMovieData(movie):
    db = sqlite3.connect("data.sql")
    c = db.cursor()

    c.close()
    db.close()
while True:

    r = praw.Reddit(user_agent=user_agent)
    try:
        r.login(config.user,config.password)  # login so we can post comments!
    except (praw.errors.InvalidUser, praw.errors.InvalidUserPass):
        logging.error("User or password is incorrect, exiting...")
        exit(0)
    except requests.HTTPError as e:
        logging.error("We got an http error: " + str(e))
        exit(0)

    subreddit = r.get_subreddit('fullmovierequest')

    for submission in subreddit.get_new(limit=1):
        print submission.title
        for comment in praw.helpers.flatten_tree(submission.comments):
            if str(comment.author) == "pymoviebot":
                print "Author is the bot"
                print "Author:", comment.author
                print "Text:", comment.body
            else:
                pass




logging.info("Program End")