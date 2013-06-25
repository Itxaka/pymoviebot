# -*- coding: utf-8 -*-

"""
database.py
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

This code will crawl around /r/fullmoviesonvimeo and /r/fullmoviesonyoutube and extract the info to a sqlite database
This code works in conjuntion with pymoviebot.py
"""

Version = 1.1

# get the proxy data and save it if necessary
import urllib
if urllib.getproxies()['http'] == "":
    print "No proxies"
else:
    with open("praw.ini", "w") as f:
        f.write("[reddit]\n")
        f.write("http_proxy = " + urllib.getproxies()['http'])
    
import praw
import sqlite3
import logging
import config


# logging parameters below
logging.basicConfig(filename=config.path + 'database.log',level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
logging.info("Program Start")

user_agent = ("pymoviebot 1.1 by /u/itxaka")  # API guidelines enforce this

r = praw.Reddit(user_agent=user_agent)

try:
    r.login(config.user, config.password)  # login so we can enter vimeo subreddit
except (praw.errors.InvalidUser, praw.errors.InvalidUserPass):
    logging.error("User or password is incorrect, exiting...")
    exit(0)

db = sqlite3.connect("data.sql")
c = db.cursor()
try:
    c.execute("DROP TABLE movie")
except sqlite3.OperationalError:
    pass

c.execute("Create table if not exists movie(id text UNIQUE, name text, url text, author text, reddit_url text, subreddit text)")

def updateDb(reddit):
    subreddit = r.get_subreddit(reddit)
    for submission in subreddit.get_new(limit=1000):
        c.execute('INSERT INTO movie VALUES(?,?,?,?,?,?)', (submission.id,submission.title, submission.url, str(submission.author), submission.permalink, reddit))
        print "record inserted"
        db.commit()

#updateDb("fullmoviesonvimeo") # commented as the subreddit is private
updateDb("fullmoviesonyoutube")

c.close()
db.close()
logging.info("Program End")
