#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import datetime
import argparse
import os
import re

today = datetime.date.today().strftime("%b %e")

parser = argparse.ArgumentParser(description="Process the log.")
parser.add_argument('-d', '--date', default=today, help="the date (eg: May 31)")
parser.add_argument("toon", nargs="?", default="Karpan", help="the toon name")
args = parser.parse_args()

db = {}
i = 0
path = os.path.expanduser("~/Library/Application Support/EverQuest/PlayerLogs/eqlog_" + args.toon + "_52.txt")
with open(path, 'r') as f:
    dt = r"\[(Mon|Tue|Wed|Thu|Fri|Sat|Sun) ((Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) [ 1-3]\d) [0-2]\d:[0-5]\d:[0-5]\d [1-2]\d{3}\] "
    nm = r"( AFK )?\[(ANONYMOUS|[1-6]?\d [ A-Za-z]+)\] ([A-Z][a-z]*) (\([ A-Za-z]+\))?( <[ A-Za-z]+>)?( LFG)?"
    ct = r"There are \d+ players in [ A-Za-z,-]+\."
    fl = "T123456789abcdefghijklmnopqrstuvwxyz"
    for line in f:
        m = re.match(dt, line)
        if m is None or m.group(2) != args.date: continue
        line = line[27:]
        m = re.match(nm, line)
        if m is not None:
            name = m.group(3)
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
names = sorted(db.keys())
for name in names:
    print name, db[name]
print
print "Full attendance:", i + 1
print
print "(L = looted, T = on time, E = entire)"
