#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Description Script for reformatting xml to suite Blast2Go. Because 
b2g4pipe cannotcope with current style large Blast XML files, so we 
reformat these to avoid it crashing with a Java heap space OutOfMemoryError.

Blast2GO can't cope with 1000s of <Iteration> tags within a single
<BlastOutput_iterations> tag, so instead split this into one full
XML record per interation (i.e. per query). This gives a concatenated XML
file mimicing old versions of BLAST.
@Input multiple Blast XML files.
@Output formatted XML files.
"""

import sys
import os

if sys.argv[1] == '-h':
	print "Usage:\n\tpython %s output_file inputfiles" % os.path.basename(__file__)
	sys.exit(0)

op = open("%s.b2g" % sys.argv[1], "w")

for f in sys.argv[2:]:
	
	with open(f) as xml:
		header = ''
		
		for line in xml:
			header += line
			if line.strip() == '<BlastOutput_iterations>': break

		footer = '</BlastOutput_iterations>\n</BlastOutput>\n\n'

		element = ''

		query_count = 0

		for line in xml:
			if line.strip() == '</BlastOutput_iterations>': break

			element += line
			
			if line.strip() == '</Iteration>':
				op.write(header)
				op.write(element)
				op.write(footer)
				element = ''
				query_count += 1
				sys.stdout.write("\rFormatting %s, Querys %s" % (f, query_count))
				sys.stdout.flush()
	print "\n"