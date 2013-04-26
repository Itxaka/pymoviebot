# -*- coding: utf-8 -*-

"""
pymoviebot-2.py
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


New features:
- Does not need to be running all the time, has to be scheduled by cron
- Does not rely on a list to check the submissions, now it checks the comments.
- It fills the new flair "Not filled"
- Distinguishes posts

"""


import praw
import time
import sqlite3
import logging
import requests
import config

# logging parameters below
logging.basicConfig(filename=config.path + 'pymoviebot.log', level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
logging.info("Program Start")

user_agent = "pymoviebot 2.0 by /u/itxaka" # API guidelines suggest this
r = praw.Reddit(user_agent=user_agent)

try:
    r.login(config.user, config.password)  # login so we can post comments!
except (praw.errors.InvalidUser, praw.errors.InvalidUserPass):
    logging.error("User or password is incorrect, exiting...")
    exit(0)
except requests.HTTPError as e:
    logging.error("We got an http error: " + str(e))

db = sqlite3.connect(config.path + "data.sql")
c = db.cursor()

subreddit = r.get_subreddit('fullmovierequest')

try:
    for submission in subreddit.get_new(limit=500):  # we get all we can
        try:
            flat_comments = praw.helpers.flatten_tree(submission.comments)  # flat everything
            for comment in flat_comments:
                if "pymoviebot" in str(comment.author):
                    if "moderator" in str(comment.distinguished):
                        pass
                    else:
                        logging.info("Comment distinguished")
                        comment.distinguish()
        except:
            pass
        else:
            c.execute("SELECT * FROM movie WHERE name LIKE ?", ("%" + submission.title + "%",))
            for row in c.fetchall():  # I still don't know what happens when I get 2 results back...
                a = True  # set this so we can keep retrying the comment and not stop until we post it
                commentAuthors = []  # set this so we check live if we have a comment on the submission
                flat_comments = praw.helpers.flatten_tree(submission.comments)  # flat everything
                for comment in flat_comments:
                    commentAuthors.append(comment.author)  # generate a list of usernames that posted
                if "pymoviebot" in str(commentAuthors):  # check if we are in that list
                        pass
                else:
                    while a:
                        try:
                            z = submission.add_comment("The movie ***" + submission.title + "*** can be found in: [here]("+ row[4] + ") thanks to /u/" + row[3] + "\n\n   *I am a bot. for comments or suggestions write [me](http://www.reddit.com/message/compose/?to=Itxaka)*")
                            # Set up the flair
                            submission_to_flair = r.get_submission(submission_id=submission.id)
                            if row[5] == "fullmoviesonvimeo":
                                subreddit.set_flair(submission_to_flair,"View on Vimeo", "vimeo")
                                logging.info("Flair Vimeo set for: " + str(unicode(submission.title)))
                            elif row[5] == "fullmoviesonyoutube":
                                subreddit.set_flair(submission_to_flair,"View on YouTube", "youtube")
                                logging.info("Flair Youtube set for: " + str(submission.title))
                            else:
                                subreddit.set_flair(submission_to_flair,"Request not fullfilled", "notfilled")
                                logging.info("Flair not filled set for: " + str(submission.title))
                            logging.info("Comment posted for " + str(submission.title))
                            a = False  # as soon as we post a comment we get out of the while
                        except praw.errors.RateLimitExceeded:
                            logging.warning("Rate limit exceeded, trying in a few seconds...")
                            time.sleep(60)  # I believe that the rate is around 8 minutes and decreases with the karma.
except requests.HTTPError as e:
    logging.error("We got an http error: " + str(e))
c.close()  # close cursor
db.close()  # close db
logging.info("Program End")