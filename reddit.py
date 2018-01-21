import praw
import re
import argparse

#to manage the argument from terminal
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-r","--subreddit",action="store_true")
group.add_argument("-u","--url",action="store_true")
parser.add_argument("n",help="Name of subreddit or url")
args = parser.parse_args()

# obtaining a reddit instance
reddit = praw.Reddit(client_id='reVWPERa_RrRFg',
client_secret='dMHgiJF2LlvvnkV4CLjXqQRzfTs',
username='reddit_data',
password='reddit_data',user_agent='anything')


# taking subreddit according to the argument
if args.subreddit:
    name = args.n
elif args.url:
    try:
        name = re.search('reddit.com/r/(.+?)/', args.n).group(1)
    except AttributeError:
    # subbreddit not found so searching for bitcoin
        name = 'bitcoin'

#import for database

import pymysql
pymysql.install_as_MySQLdb()

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","password","reddit" )


# prepare a cursor object using cursor() method
cursor = db.cursor()
cursor2 = db.cursor()

# #function to write into database
def write_submission(i,t,a,k,u,d,s,idd,parent,text,subid,flag):


    # Open database connection
    db = MySQLdb.connect("localhost","root","password","reddit" )
    print("function call")

    # prepare a cursor object using cursor() method
    cursor = db.cursor()


    if (flag == 1):
        # Prepare SQL query to INSERT a record into the database.
        sql = "INSERT INTO submission(ID, \
            TITLE, AUTHOR, KARMA, UPS, DOWNS, SCORE) \
            VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s' )" % \
            (i,t, a, k, u, d, s)
    else:

        sql = "INSERT INTO comments(id, \
        parent_id, text, submission_id) \
        VALUES ('%s', '%s', '%s', '%s')" % \
        (idd,parent,text,subid)

    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
        print("WRITTEN")
    except:
        # Rollback in case there is any error
        db.rollback()
        print("WRITING ERROR")

    # disconnect from server
    finally:
        db.close()


subreddit = reddit.subreddit(name)
hot_python = subreddit.hot(limit=5)




# looking at the individual post
for submission in hot_python:
    if not submission.stickied:
        idNum = format(submission.id)
        title = format(submission.title)
        author = format(submission.author)
        karma = format(submission.author.link_karma)
        ups = format(submission.ups)
        downs = format(submission.downs)
        score = format(submission.score)
        print(title)
        write_submission(idNum,title,author,karma,ups,downs,score,'idd','parent','text','subid',1)


# now looking at the comments
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            selfID = comment.id
            parent = comment.parent()
            body = comment.body
            sub_id = submission.id
            write_submission('idNum','title','author','karma','ups','downs','score',selfID,parent,body,sub_id,0)
