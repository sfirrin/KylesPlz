import sys
import random
import os
import time
from twython import Twython, TwythonError
from logzero import logger as log
import string
import random


def tweet():
    # Reading secret info from environment variables
    apiKey = os.environ.get('API_KEY')
    apiSecret = os.environ.get('API_SECRET')
    accessToken = os.environ.get('ACCESS_TOKEN')
    accessTokenSecret = os.environ.get('ACCESS_TOKEN_SECRET')

    if not all([apiKey, apiSecret, accessToken, accessTokenSecret]):
        print('You need to set up your environment variables before you can run this')
        return

    twitter = Twython(apiKey, apiSecret, accessToken, accessTokenSecret)

    # GET FOLLOWERS
    followers = (twitter.get_followers_ids(screen_name="@kylesplz")['ids'])

    log.info('Found these followers, {}'.format(followers))

    # pick a random ID from all followers
    winner_id = random.choice(followers)
    # lookup the handle of the lucky ID
    winner_user = twitter.lookup_user(user_id=winner_id)[0]

    log.info('Lucky follower was {}'.format(winner_user))

    winner_handle = winner_user['screen_name']

    lines = open('tweet_options.txt').read().splitlines()
    random_line = random.choice(lines)

    images_path = r'kyles/'

    random_pic = random.choice([x for x in os.listdir(images_path)
                                if os.path.isfile(os.path.join(images_path, x))])

    picfind = images_path + random_pic

    message = 'Hey @{}, {}'.format(winner_handle, random_line)

    log.info('Attempting tweet: {}'.format(message))
    with open(picfind, 'rb') as photo:
        twitter.update_status_with_media(status=message, media=photo)

    log.info('Tweet successfully made')


def lambda_handler(event, context):
    print event, context
    tweet()


if __name__ == '__main__':
    tweet()
