#!/usr/bin/env python
# <bitbar.title>RescueTime Productive Time</bitbar.title>
# <bitbar.version>v2.0</bitbar.version>
# <bitbar.author>Jason Benn</bitbar.author>
# <bitbar.author.github>JasonBenn</bitbar.author.github>
# <bitbar.desc>Show your RescueTime very productive time & pulse in the status bar</bitbar.desc>
# <bitbar.dependencies>python</bitbar.dependencies>
#
# To install, you will want to generate an API key for rescue time and then store the
# key in ~/Library/RescueTime.com/api.key
# https://www.rescuetime.com/anapi/manage
import datetime
import os
import json
import urllib
import urllib2


def get(url, params):
    '''Simple function to mimic the signature of requests.get'''
    params = urllib.urlencode(params)
    result = urllib2.urlopen(url + '?' + params).read()
    return json.loads(result)


def mins_to_time(minutes):
    return "{}:{:02}".format(minutes // 60, minutes % 60)


MAPPING = {
    2: 'Very Productive',
    1: 'Productive',
    0: 'Neutral',
    -1: 'Distracting',
    -2: 'Very Distracting'
}

API_KEY = os.path.expanduser('~/Library/RescueTime.com/api.key')
if not os.path.exists(API_KEY):
    print('X')
    print('---')
    print('Missing API Key')
    exit()


key = open(API_KEY).read().strip()
date = datetime.date.today().strftime('%Y-%m-%d')
data = get('https://www.rescuetime.com/anapi/data', params={
    'format': 'json',
    'key': key,
    'resolution_time': 'day',
    'restrict_begin': date,
    'restrict_end': date,
    'restrict_kind': 'productivity',
})
pulse = get('https://www.rescuetime.com/anapi/current_productivity_pulse.json', params={'key': key})
# summary = get('https://www.rescuetime.com/anapi/daily_summary_feed.json', params={'key': key})

activities = data['rows']
total_mins = sum([x[1] for x in activities]) // 60
total_very_prod_mins = sum([x[1] for x in activities if x[3] == 2]) // 60
pulse_color = pulse['color']
print("{} (of {}) | color={}".format(mins_to_time(total_very_prod_mins), mins_to_time(total_mins), pulse_color))
