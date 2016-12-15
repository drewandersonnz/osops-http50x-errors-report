#!/usr/bin/env python
from __future__ import print_function

import datetime

timezone = -5
times = []

# setup for this and last hour only
for x in range (-1, 1):
    times.append(datetime.datetime.utcnow() + datetime.timedelta(hours=(timezone + x), ))

datesGrep = '|'.join([x.strftime("%d/%b/%Y:%H") for x in times])

# remove these lines from investigation
excludesGrep = '|'.join([
    '.jpg', '.png', '.css', '.js', '.svg', 'favicon.ico', 'robots.txt', # images and resources
    '"WatchMouse/', '"NodePing"', '; UptimeRobot/', # uptime robots
])

# build command
command = ' | '.join([
    "egrep '\" 50[0-9]' /var/log/httpd/openshift/openshift_log",
    "grep -Ev '({excludesGrep})'".format(excludesGrep=excludesGrep),
    "grep -E '({datesGrep})'".format(datesGrep=datesGrep),
    "awk '{ print $1 }'",
    "sort",
    "uniq -c",
    "sort -n",
    "tail",
])

print(command)
