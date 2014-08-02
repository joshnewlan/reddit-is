import praw
import re

r = praw.Reddit('Reddit is /u/user')
r.login('user', 'pwd')
textfile = "/Users/user/reddit-is.txt"

comments = praw.helpers.comment_stream(r, 'all', limit=None)

for comment in comments:
    p = re.compile(ur'(reddit\s+(is|isnt|isn\'t|was|wasnt|wasn\'t|does|didnt|didn\'t|says|said|has|hasnt|hasn\'t|can|cannot|cant|can\'t|will|wont|won\'t|likes|dislikes|hates|loves|thinks|hopes|acts|wishes|gets|wants|needs|fears|worships)\b)', re.IGNORECASE)
    tis = re.match(p, comment.body)
    if tis is not None:
        body = comment.body.rstrip('\n')
        with open(textfile,'a') as f:
            f.write(comment.id + ",")
            f.write(comment.link_id + ",")
            subreddit = str(comment.subreddit)
            author = str(comment.author)
            f.write(subreddit + ",")
            f.write(author + ",")
            score = str(comment.score)
            controversiality = str(comment.controversiality)
            created_utc = str(comment.created_utc)
            f.write(score+ "," +controversiality+ "," +created_utc+ "," +body)
            f.write('\n')
        f.closed
        print comment.body
    else:
        continue
