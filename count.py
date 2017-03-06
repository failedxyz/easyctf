#!/usr/bin/env python

import os
import yaml
import traceback
from collections import Counter

problem_names = os.listdir(os.path.dirname(os.path.abspath(__file__)))
problems = []

for problem_name in problem_names:
	try:
		metadata_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + problem_name + os.sep + "problem.yml"
		with open(metadata_file, "r") as f:
			metadata_raw = f.read()
			metadata = yaml.load(metadata_raw)
			if "category" in metadata:
				problems.append(metadata)
	except:
		pass
		# print traceback.format_exc()

problems.sort(key=lambda p: p.get("value"), reverse=True)
print "Grand Total: %d" % len(problems)
print "Category Breakdown:"

c = Counter(map(lambda p: p.get("category", ""), problems))
categories = sorted(c.items(), key=lambda c: c[1], reverse=True)
for category, count in categories:
	print "  %s: %s" % (category, count)
	for problem in problems:
		if problem.get("category") != category: continue
		print "    %s [%s]" % (problem.get("title"), problem.get("value"))
