#!/usr/bin/env python
# <bitbar.title>RescueTime Productive Time</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Jason Benn & Paul Traylor</bitbar.author>
# <bitbar.author.github>kfdm</bitbar.author.github>
# <bitbar.desc>Show your RescueTime productivity time & pulse in the status bar</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>
#
# To install, you will want to generate an API key for rescue time and then store the
# key in ~/Library/RescueTime.com/api.key
# https://www.rescuetime.com/anapi/manage
import datetime
import json
import os
import urllib
import urllib2

API_KEY = os.path.expanduser('~/Library/RescueTime.com/api.key')

MAPPING = {
    2: 'Very Productive',
    1: 'Productive',
    0: 'Neutral',
    -1: 'Distracting',
    -2: 'Very Distracting'
}


def get(url, params):
    '''Simple function to mimic the signature of requests.get'''
    params = urllib.urlencode(params)
    result = urllib2.urlopen(url + '?' + params).read()
    return json.loads(result)

if not os.path.exists(API_KEY):
    print('X')
    print('---')
    print('Missing API Key')
    exit()

with open(API_KEY) as fp:
    key = fp.read().strip()
    date = datetime.date.today().strftime('%Y-%m-%d')
    result = get('https://www.rescuetime.com/anapi/data', params={
        'format': 'json',
        'key': key,
        'resolution_time': 'day',
        'restrict_begin': date,
        'restrict_end': date,
        'restrict_kind': 'productivity',
    })
    pulse = get('https://www.rescuetime.com/anapi/current_productivity_pulse.json', params={
        'key': key,
    })
    data = get('https://www.rescuetime.com/anapi/data.json', params={
        'key': key,
    })
    prod_total = sum([row[1] for row in data['rows'] if row[5] == 2])
    pulse_colored = '{} | color={}'.format(pulse['pulse'], pulse['color'])

def mins_to_time(seconds):
    minutes = seconds / 60
    return "{}:{:02}".format(minutes / 60, minutes % 60)

print("{} - {}".format(mins_to_time(prod_total), pulse_colored))
print('---')
print('Rescue Time | href=https://www.rescuetime.com/dashboard?src=bitbar')
for rank, seconds, people, productivity in result['rows']:
    print('%s \t %s' % (mins_to_time(seconds), MAPPING[productivity]))