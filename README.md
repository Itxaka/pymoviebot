Copyrigth 2013 - Itxaka Serrano Garcia <itxakaserrano@gmail.com>

  This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>




pymoviebot.py
--------------

pymoviebot is a bot for reddit. It will keep checking the subreddit /r/fullmovierequest for movie requests. 
On a new request it will check the sqlite databse created from /r/fullmoviesonyoutube and /r/fullmoviesonvimeo 
and if something is found it will post the correct link to the post.


How it works
-------------

database.py will crawl both subreddits and store into a sqlite database the whole thing. post ID, title, url,
reddit url and post author is stored. 
The sqlite database provides us with a quick and small response for any query we do, much better than searching
both subreddits everytime there is a new request.

pymoviebot.py will check the request subreddit every 5 minutes and get the 10 newests post. Then it will check if they 
are already fulfilled and commented by itself and if not, check and post if there is any coincidence in the database.


TODOs
------

Add logging so it can be run and get get some output of what is going on.
Use more try/Except to catch more exceptions, in case reddit is down for example.
Check what happens if the search answers 2 rows of data, like a movie and his HD counterpart. Im guessing nothing happens,
it tries to post the links again but the bot check that he has commented already so it ignores it.
