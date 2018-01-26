import sys
import random
from datetime import datetime
import os
import time
from twython import Twython, TwythonError
from logzero import logger as log
import string
import random

GREETINGS = [
    'Hello',
    'Hi',
    'Hey',
    'What\'s up'
]


IMAGES_PATH = r'kyles/'

# Same order as twython constructor
TWITTER_CRED_ENV_VARIABLE_NAMES = [
    'API_KEY', 'API_SECRET', 'ACCESS_TOKEN', 'ACCESS_TOKEN_SECRET'
]


def get_api_client():
    """ Makes client with creds from 
    """
    # Reading secret info from environment variables
    api_key = os.environ.get('API_KEY')
    api_secret = os.environ.get('API_SECRET')
    access_token = os.environ.get('ACCESS_TOKEN')
    access_token_secret = os.environ.get('ACCESS_TOKEN_SECRET')
    twitter_creds = map(
        lambda cred_name: os.environ.get(cred_name),
        TWITTER_CRED_ENV_VARIABLE_NAMES
    )

    if not all(twitter_creds):
        raise EnvironmentError(
            'You need to set up your Twitter secrets in environment' 
            'variables before you can run this'
        )

    twitter_api_client = Twython(*twitter_creds)
    return twitter_api_client


def tweet_kyle():
    """ Chooses a random Kyle image file from the IMAGES_PATH dir
        Connects to twitter with creds in env variables
        Chooses a random line from the text file with wise Kyle sayings
        Tweets the random line with the 
    """
    twitter_api_client = get_api_client()
    # Get followers
    followers = (twitter_api_client.get_followers_ids(screen_name="@kylesplz")['ids'])
    # Pick a random ID from all followers
    winner_id = random.choice(followers)
    winner_user = twitter_api_client.lookup_user(user_id=winner_id)[0]
    winner_handle = winner_user['screen_name']

    lines = open('tweet_options.txt').read().splitlines()
    random_line = random.choice(lines)

    image_options = sorted(
        filter(lambda f: os.path.isfile(os.path.join(IMAGES_PATH, f))),
        os.listdir(IMAGES_PATH)
    )
    chosen_kyle = random.choice(image_options)
    image_path = IMAGES_PATH + chosen_key

    message = '{greeting} @{handle}, {tweet_content}'.format(
        greeting=random.choice(GREETINGS),
        handle=winner_handle,
        tweet_content=random_line
    )
    log.info('Attempting to tweet the following message: %s', message)
    with open(image_path, 'rb') as photo:
        tweet = twitter_api_client.update_status_with_media(
            status=message, media=photo
        )

    log.info('API response to tweet attempt: %s', tweet)


def lambda_handler(event, context):
    tweet_kyle()

# For testing
if __name__ == '__main__':
    tweet()
