#!/usr/bin/env python
import sys
import random, os
import time
from twython import Twython, TwythonError
import string
import random


def main():
    # your twitter consumer and access information goes here

    credentials = open('credentials.txt', 'rb')
    apiKey = credentials.next().strip()
    apiSecret = credentials.next().strip()
    accessToken = credentials.next().strip()
    accessTokenSecret = credentials.next().strip()

    twitter = Twython(apiKey, apiSecret, accessToken, accessTokenSecret)

    # GET FOLLOWERS
    followers = (twitter.get_followers_ids(screen_name="@kylesplz")['ids'])

    print followers

    # pick a random ID from all followers
    luckyid = random.choice(followers)

    # lookup the handle of the lucky ID
    output = twitter.lookup_user(user_id=luckyid)

    # Loop through the results (Twitter screen names)
    for user in output:
        print user['screen_name']
        username_list = (user['screen_name'])

    print username_list

    luckyfollower = username_list

    # luckyfollower = (twitter.lookup_user(user_id=luckyid))
    # print luckyfollower['screen_name']

    # GET RANDOM COMPLIMENT AND TWEET AT PERSON

    lines = open('tweet_options.txt').read().splitlines()
    random_line = random.choice(lines)
    # print(myline)

    path = r'kyles/'

    random_pic = random.choice([x for x in os.listdir(path)
                                if os.path.isfile(os.path.join(path, x))])

    picfind = path + random_pic

    message = 'Hey @' + luckyfollower + ', ' + random_line

    with open(picfind, 'rb') as photo:
        twitter.update_status_with_media(status=message, media=photo)

    print 'tweet complete'


if __name__ == '__main__':
    main()
