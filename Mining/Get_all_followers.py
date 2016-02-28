import tweepy
import time

# Takes care of the necessary login information

consumer_key = XXXXXXXXXXXXXXX
consumer_secret = XXXXXXXXXXXXXXX
access_token = XXXXXXXXXXXXXXX
access_token_secret = XXXXXXXXXXXXXXX

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)  

# Checks if app was able to successfully authorise
if(api.verify_credentials):
    print 'We sucessfully logged in'  

user_id = api.get_user('Enter the user handle of the twitter account here').id
followers_log = 'Enter the address where you want the file to be stored here' + 'followers.txt'

# Opens the newly created followers.txt file
outfile = open(followers_log, 'w')

# Gets all the followers of a twitter account as a cursor object. 
user = tweepy.Cursor(api.followers, id=user_id).items()
counter = 0

# Iterates through user object and incase of rate limit being reached, waits for 15 mins   
while True:
    try:
        u = next(user)
        outfile.write(u.screen_name + '-' + str(u.id) + '\n')
        counter += 1
    except tweepy.TweepError:
        localtime = time.asctime( time.localtime(time.time()) )       # The time when rate limit was reached
        print 'Local current time :', localtime
        print 'Followers written :', counter 
        print 'Sleeping for 15 minutes'
        print ''   # for an empty line
        time.sleep(15*60)
        continue
    except StopIteration:                                             # No more objects left to iterate over
        print 'All the followers were recorded'
        break

# Closes the file
outfile.close()
