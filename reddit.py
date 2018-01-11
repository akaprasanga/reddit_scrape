import praw
import re
import argparse

try:
    #to manage the argument from terminal
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-r","--subreddit",action="store_true")
    group.add_argument("-u","--url",action="store_true")
    parser.add_argument("n",help="Name of subressit or url")
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

    subreddit = reddit.subreddit(name)
    hot_python = subreddit.hot(limit=3)

    open('data.txt', 'w').close()
    f = open('data.txt','a')


    # looking at the individual post
    for submission in hot_python:
        if not submission.stickied:
            title = format(submission.title)
            ups = format(submission.ups)
            downs = format(submission.downs)
            idNum = format(submission.id)
            f.write('\n' + 90*'-')
            f.write('\n'+'TITLE :'+ title + '\tSubmissionID :'+ idNum + '\tUpvote :'+ ups +'\tDown Votes :'+ downs)
            f.write('\n' + 90*'-')
    # now looking at the comments
            submission.comments.replace_more(limit=0)
            for comment in submission.comments.list():
                f.write('\n\n' + 3*'#')
                parent = str(comment.parent())
                selfID = str(comment.id) 
                # print (parent,selfID)
                f.write('Parent ID:' + parent)
                f.write('\tComment ID:' + selfID)
                f.write('\n' + comment.body[:100])# limiting body of comment 

    f.close()

except:
    print('Might be internet connection or bad URL probem')