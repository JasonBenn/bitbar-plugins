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


def h_to_t(hours_float):
    hours = int(hours_float)
    mins = int(hours_float % 1 * 60)
    return "{}:{:02d}".format(hours, mins)


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

activities = data['rows']
time_today = sum([x[1] for x in activities]) // 60 / 60
vp_time_today = sum([x[1] for x in activities if x[3] == 2]) // 60 / 60
pulse_color = pulse['color']
print("{} (of {}) | color={}".format(h_to_t(vp_time_today), h_to_t(time_today), pulse_color))

print('---')

# Print summaries for last 7 days
summary = get('https://www.rescuetime.com/anapi/daily_summary_feed.json', params={'key': key})
last_7_days = summary[:7]
last_7_as_days_of_week = [datetime.datetime.strptime(x['date'], '%Y-%m-%d').weekday() for x in last_7_days]
monday_index = last_7_as_days_of_week.index(0)
this_week_daily_summaries = last_7_days[:monday_index+1]

week_vp_time = vp_time_today
week_time = time_today

for x in this_week_daily_summaries:
    day = datetime.datetime.strptime(x['date'], '%Y-%m-%d').strftime('%a')
    day_time = x['all_productive_hours'] + x['neutral_hours'] + x['all_distracting_hours']
    day_vp_time = x['very_productive_hours']
    print("{}: {} (of {})".format(day, h_to_t(day_vp_time), h_to_t(day_time)))
    week_vp_time += day_vp_time
    week_time += day_time

print("Total: {} (of {})".format(h_to_t(week_vp_time), h_to_t(week_time)))
