#!/usr/bin/evn python
import sys

family = {}
stat = {}

with open("rfam_families.txt") as fh:
	for line in fh:
		if line[0] == "#":
			continue
		cols = line.strip().split()
		stat[cols[0]] = len(cols[1:])
		for col in cols[1:]:
			family[col] = cols[0]

counts = {}
with open(sys.argv[1]) as fh:
	for line in fh:
		nc = line.strip().split("\t")[1].split(';')[0]
		rf = family[nc]
		try:
			counts[rf]
		except KeyError:
			counts[rf] = [0, set()]
		counts[rf][0] += 1
		counts[rf][1].add(nc)

for c in counts:
	print c, "\t", stat[c], "\t", len(counts[c][1]), "\t", counts[c][0]