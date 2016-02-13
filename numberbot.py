from slackclient import SlackClient
import os

import math
from itertools import count, islice

import logging


logger = logging.getLogger(__name__)

outputs = []
crontable = []

client_token = os.environ['SLACK_TOKEN']
sc = SlackClient(client_token)

def is_fibonacci(n):
    phi = 0.5 + 0.5 * math.sqrt(5.0)
    a = phi * n
    return n == 0 or abs(round(a) - a) < 1.0 / n

def is_prime(n):
    if n < 2:
        return False
    return all(n % i for i in islice(count(2), int(math.sqrt(n) - 1)))

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def process_message(data):
    if data['type'] == 'message':
        ts = data['ts']
        text = data['text']
        channel = data['channel']
        tokens = text.split(' ')
        for token in tokens:
            if is_int(token):
                logger.info('int')
                number = int(token)
                if number < 100:
                    return
                if number <= 99194853094755497 and is_prime(number):
                    logger.info('prime')
                    result = sc.api_call('reactions.add', timestamp=ts, channel=channel, name='prime')
                    logger.info(str(result))

                if is_fibonacci(number):
                    logger.info('fib')
                    result = sc.api_call('reactions.add', timestamp=ts, channel=channel, name='shell')
                    logger.info(str(result))

    logger.info(data)
