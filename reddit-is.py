import praw
import re
import time
from requests.exceptions import ConnectionError, ReadTimeout

CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = ""
REFRESH_TOKEN = ""
USERNAME = ""

def authenticate():
    print "Authenticating"
    r = praw.Reddit('Reddit is by /u/{}'.format(USERNAME))
    r.set_oauth_app_info(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)
    access_information = r.refresh_access_information(REFRESH_TOKEN)
    r.set_access_credentials(**access_information)
    # authenticated_user = r.get_me()
    # print "Authenticated as {}".format(authenticated_user.name)
    return r
    
# TODO: Check authenticated_user.link_karma > 1
r = authenticate()
try:
    while True:
        try:
            comments = praw.helpers.comment_stream(r, 'all', limit=None,verbosity=3)
        except (ConnectionError, 
                ReadTimeout, 
                praw.errors.OAuthInvalidToken, 
                IOError) as e:
            print "{}, waiting...".format(e.strerror)
            time.wait(6)
            r = authenticate()
            continue

        for comment in comments:
            p = re.compile(ur"""(reddit\s+(is|isnt|isn\'t|
                                    was|wasnt|wasn\'t|werent|weren\'t|
                                    does|didnt|didn\'t|goes|makes|gets|
                                    will|wont|won\'t|
                                    says|said|pontificates|
                                    has|hasnt|hasn\'t|
                                    can|cannot|cant|can\'t|
                                    likes|dislikes|hates|loves|
                                    thinks|hopes|acts|wishes|wants|needs|
                                    fears|freaks|worships|finds|pretends|compares|
                                    spazzes|denies|sings)\b)""", re.IGNORECASE)
            tis = re.match(p, comment.body)
            if tis is not None:
                body = comment.body.rstrip('\n')
                with open('reddit-is.csv','a') as f:
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
                    f.write(score+ "," +controversiality+ "," + created_utc + "," 
                        +link+ ",reddit-is-comment:" +body)
                    f.write('\n')
                f.closed
                print comment.body
            else:
                continue
except KeyboardInterrupt:
    pass

