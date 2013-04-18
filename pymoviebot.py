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

Version = 0.2

# TODO: Add logging so it can provide feedback
# DONE! Put it in a loop so it runs indefinitly? Not sure if we want that and a time.sleep() or we rather launch it every X minutes like with cron
# TODO: Try/except in case reddit is down
# TODO: Check what happens if I get back 2 results when searching for a movie. Maybe I get a normal and HD version and all hell breaks loose?


import praw
import time
import sqlite3


user_agent = ("pymoviebot 0.1 by /u/itxaka") # API guidelines suggest this
already_done = []  # the ones we have submitted the comment to go here

r = praw.Reddit(user_agent=user_agent)
try:
    r.login(,)  # login so we can post comments!
except (praw.errors.InvalidUser, praw.errors.InvalidUserPass):
    print "User or password is incorrect, exiting..."
    exit(0)


while True:
    db = sqlite3.connect("data.sql")
    c = db.cursor()
    subreddit = r.get_subreddit('fullmovierequest')
    for submission in subreddit.get_new(limit=10):  # we get 10 at a time. It would be strange to have mora than 10 new submissions every 5 minutes
        if submission.id in already_done:  # first check to see if we added it to the done list
            print "ID is already fullfilled"
            print "Already done list:", already_done, "Submission ID:", submission.id
            pass
        else:
            c.execute("SELECT * FROM movie WHERE name LIKE ?", ("%" + submission.title + "%",))
            for row in c.fetchall():  # I still don't know what happens when I get 2 results back...
                print "----------------------------------------------"
                print "Possible result found:"
                print "Reddit text:", submission.title
                print "Database find:", row[1]
                print "----------------------------------------------"
                print
                already_done.append(submission.id)  # we found it so we add it to the list of dones.
                a = True  # set this so we can keep retying the comment and not stop until we post it
                commentAuthors = []  # set this so we check live if we have a comment on the submission
                flat_comments = praw.helpers.flatten_tree(submission.comments)  # flat everything
                for comment in flat_comments:
                    commentAuthors.append(comment.author)  # generate a list of usernames that posted
                if "pymoviebot" in str(commentAuthors):  # check if we are in that list
                        print "Seems that we already submitted content"
                else:
                    while a:
                        try:
                            z = submission.add_comment("The movie ***" + submission.title + "*** can be found in: [here]("+ row[4] + ") thanks to /u/" + row[3] + "\n\n   pymoviebot by /u/Itxaka. This is just a test, data could be wrong.")
                            print "Comment posted"
                            a = False  # as soon as we post a comment we get out of the while
                        except praw.errors.RateLimitExceeded:
                            print "Rate limit exceeded, trying in a few seconds..."
                            time.sleep(60)  # I believe that the rate is around 8 minutes and decreases with the karma.
    print "Run done"
    c.close()  # close cursoi
    db.close()  # close db
    time.sleep(300)  # We sleep for 5 minutes before checking again, I believe new submissions arent provided until 30 seconds after being posted