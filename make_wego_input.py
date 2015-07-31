#!/usr/bin/env python
# -*- cdoing: utf-8 -*-

'''
@Description this script was used to make input file for WEGO
of BGI with the output files of blast2go annotation.
@input blast2go annotation file
@output wego native format
'''

import sys
import os

if sys.argv[1] == '-h':
	print "Usage:\n\t%s output_file input_files" % os.path.basename(__file__)
	sys.exit(0)

op = open(sys.argv[1], "w")

seqs = dict()
for annot in sys.argv[2:]:
	with open(annot) as fh:
		for line in fh:
			cols = line.strip().split()
			try:
				seqs[cols[0]].append(cols[1])
			except KeyError:
				seqs[cols[0]] = [cols[1]]

for query in seqs:
	op.write("%s\t%s" % (query, "\t".join(seqs[query])))
	op.write("\n")

op.close()