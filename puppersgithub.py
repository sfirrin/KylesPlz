#!/usr/bin/env python
import sys
import random, os
import time
from twython import Twython, TwythonError
import string
import random

tweetStr = "Hello World2"

# your twitter consumer and access information goes here
# note: these are garbage strings and won't work
apiKey = ''
apiSecret = ''
accessToken = ''
accessTokenSecret = ''

twitter = Twython(apiKey,apiSecret,accessToken,accessTokenSecret)

#GET FOLLOWERS
followers = (twitter.get_followers_ids(screen_name = "@puppersplz")['ids'])

print followers

#pick a random ID from all followers
luckyid = random.choice(followers)

#lookup the handle of the lucky ID
output = twitter.lookup_user(user_id=luckyid)


# Loop through the results (Twitter screen names)
for user in output:
    print user['screen_name']
    username_list= (user['screen_name'])
    
print username_list

luckyfollower=username_list

#luckyfollower = (twitter.lookup_user(user_id=luckyid))
#print luckyfollower['screen_name']

#GET RANDOM COMPLIMENT AND TWEET AT PERSON

lines = open('/home/pi/Desktop/compliments.txt').read().splitlines()
myline =random.choice(lines)
#print(myline)


print(myline.format(luckyfollower))

path = r"/home/pi/Desktop/pups"

random_pic = random.choice([
    x for x in os.listdir(path)
    if os.path.isfile(os.path.join(path,x))
])

picfind = path+'/'+random_pic  

message = (myline.format(luckyfollower))
with open(picfind, 'rb') as photo:
    twitter.update_status_with_media(status=message, media=photo)


print "tweet complete"
