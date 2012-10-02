#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import datetime
import argparse
import dateutil.parser
import os
import re

iso = "%Y-%m-%d"
today = datetime.date.today().strftime(iso)
parser = argparse.ArgumentParser(description="Process the log.")
parser.add_argument('-d', '--date', default=today, help="the date")
parser.add_argument("toon", nargs="?", default="Karpan", help="the toon name")
args = parser.parse_args()
date = dateutil.parser.parse(args.date).date()
path = os.path.expanduser("~/Library/Application Support/EverQuest/PlayerLogs/eqlog_" + args.toon + "_52.txt")

db = {}
i = 0
with open(path, 'r') as f:
    dt = r"\[(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [ 1-3]\d) [0-2]\d:[0-5]\d:[0-5]\d ([1-2]\d{3})\] "
    nm = r"( TRADER)?( AFK )?( <LINKDEAD>)?\[(ANONYMOUS|[1-6]?\d [ A-Za-z]+)\] ([A-Z][a-z]*) (\([ A-Za-z]+\))?( <[ A-Z`a-z]+>)?( LFG)?"
    ct = r"There (is|are) \d+ players? in .+\."
    fl = "T123456789abcdefghijklmnopqrstuvwxyz"
    yr = date.strftime("%Y")
    md = date.strftime("%b %e")
    for line in f:
        m = re.match(dt, line)
        if m is None or m.group(4) != yr or m.group(2) != md: continue
        line = line[27:]
        m = re.match(nm, line)
        if m is not None:
            name = m.group(5)
            if name in db:
                db[name] = db[name] + fl[i]
            else:
                db[name] = fl[i]
            continue
        m = re.match(ct, line)
        if m is not None:
            i = i + 1
            continue
        #print line,
print date.strftime(iso)
print
names = sorted(db.keys())
for name in names:
    print name, db[name]
print
print "Full attendance:", i + 1
print
print "(L = looted, T = on time, E = entire)"
