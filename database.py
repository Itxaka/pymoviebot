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

Version = 0.2

# TODO: Try/catch if reddit is down or there is no connection
# TODO: logging so we don't print anything to the screen
# TODO: Catch database UNIQUE violation in case an id is duplicated
# TODO: Fix the count at the end. Even if it doesn't insert anything, the numbers don't match. Dont know why.

import praw
import sqlite3
import logging


# logging parameters below
logFormat='%(asctime)s - %(message)s'
logging.basicConfig(filename='database.log',level=logging.INFO, format=format, datefmt='%d/%m/%Y %I:%M:%S %p')
logging.info("Program Start")

user_agent = ("pymoviebot 0.1 by /u/itxaka")  # API guidelines enforce this
count = 0

r = praw.Reddit(user_agent=user_agent)

db = sqlite3.connect("data.sql")
c = db.cursor()
c.execute("Create table if not exists movie(id text UNIQUE, name text, url text, author text, reddit_url text, subreddit text)")

subreddit = r.get_subreddit('fullmoviesonvimeo')
for submission in subreddit.get_new(limit=1000):
    c.execute('SELECT * FROM movie where id=?', (submission.id,))
    if c.fetchone():  # check if the id is already in the database
        count += 1  # if it was, add one so we can check the db at the end
    else:
        # use str() for the author as it won't work any other way
        c.execute('INSERT INTO movie VALUES(?,?,?,?,?,?)', (submission.id,submission.title, submission.url, str(submission.author), submission.permalink, "fullmoviesonvimeo"))
        db.commit()

subreddit = r.get_subreddit('fullmoviesonyoutube')
for submission in subreddit.get_new(limit=1000):
    c.execute('SELECT * FROM movie where id=?', (submission.id,))
    if c.fetchone(): # check if the id is already in the database
        count += 1  # if it was, add one so we can check the db at the end
    else:
        # use str() for the author as it won't work any other way
        c.execute('INSERT INTO movie VALUES(?,?,?,?,?,?)', (submission.id,submission.title, submission.url, str(submission.author), submission.permalink, "fullmoviesonyoutube"))
        db.commit()

# we will execute a little check in order to see if we found new items
c.execute("SELECT COUNT(*) FROM movie")
controlCheck = c.fetchone()[0]

if controlCheck == count:
    logging.info("Database is up to date")
else:
    logging.info("Database was updated")
    logging.info("There was " + str(count) + " items before. There is " + str(controlCheck) + " items now.")

# Don't forget to close the database (¬_¬)
c.close()
db.close()
logging.info("Program End")
