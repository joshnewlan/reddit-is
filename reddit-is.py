import praw
import re

r = praw.Reddit('Reddit is /u/USER')
r.login('USERNAME', 'PASSWORD')

comments = praw.helpers.comment_stream(r, 'all', limit=None)

for comment in comments:
    p = re.compile(ur'(reddit\s+(is|isnt|isn\'t|was|wasnt|wasn\'t|does|didnt|didn\'t|says|said|has|hasnt|hasn\'t|can|cannot|cant|can\'t|will|wont|won\'t|likes|dislikes|hates|loves|thinks|hopes|acts|wishes|gets|wants|needs|fears|worships|finds|pretends|compares)\b)', re.IGNORECASE)
    #tis = re.findall(p, comment.body)
    tis = re.match(p, comment.body)
    if tis is not None:
        body = comment.body.rstrip('\n')
        with open('test.txt','a') as f:
            comment_id = str(comment.id)
            subreddit = str(comment.subreddit)
            author = str(comment.author)
            link = str(comment.permalink)
            score = str(comment.score)
            created_utc = str(comment.created_utc)
            controversiality = str(comment.controversiality)
            f.write(comment_id + ",")
            f.write(subreddit + ",")
            f.write(author + ",")
            f.write(score+ "," +controversiality+ "," +created_utc+ "," +link+ ",reddit-is-comment:" +body)
            f.write('\n')
        f.closed
        print comment.body
    else:
        continue
