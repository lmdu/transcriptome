#!/usr/bin/env python

'''
@module assess_assembly_quality.py
@descrition Before running this script, you should run Trinity first, the
input file is Trinity.fasta, the output of Trinity contains all contigs
And then, get the length of each contig, calculate the N10, N50, N90, mean,
median and do statistics.
@input a FASTA file contains multiple contigs sequences
@output a statistical file
@author ming
@date 2013/9/25 12:09:26
'''

import sys
import os
import gzip

if sys.argv[1] == '-h':
	print "Usage:\n\t %s contigs.fasta > output.txt" % os.path.basename(__file__)
	sys.exit(0)

in_fasta = sys.argv[1]

transcript_lens = []
gc = 0

print "Calculating contig length"
contig_len = 0

if in_fasta.endswith(".gz"):
	fh = gzip.open(in_fasta, 'rb')
else:
	fh = open(in_fasta, 'r')

for line in fh:
	line = line.strip()
	if not line: continue
	if line[0] == '>':
		if contig_len:
			transcript_lens.append(contig_len)
		contig_len = 0
	else:
		contig_len += len(line)
		gc += line.upper().count('G')
		gc += line.upper().count('C')
else:
	transcript_lens.append(contig_len)

fh.close()

transcript_lens.sort(reverse=True)

transcript_counts = len(transcript_lens)

#calculating median value
idx = transcript_counts/2
if transcript_counts % 2 == 0:
	median_len = round((transcript_lens[idx] + transcript_lens[idx-1])/2.0, 1)
else:
	median_len = transcript_lens[idx]

max_len = max(transcript_lens)
min_len = min(transcript_lens)
total_len = sum(transcript_lens, 0.0)
mean_len = round(total_len/transcript_counts, 1)
N50_partial_len = total_len * 0.5
N10_partial_len = total_len * 0.1
N90_partial_len = total_len * 0.9

print "Calculating N50 length"
partial_len = 0
N10_len = None
N50_len = None
N90_len = None
for length in transcript_lens:
	partial_len += length

	if N10_len is None:
		if partial_len >= N10_partial_len:
			N10_len = length

	if N50_len is None:
		if partial_len >= N50_partial_len:
			N50_len = length

	if partial_len >= N90_partial_len:
		N90_len = length
		break

scales = range(200, 1000, 100) + range(1000, 11000, 1000)

statistics = {}.fromkeys(scales, 0)

print "Doing statistics for each scale"
for length in transcript_lens:
	for scale in scales:
		if length >= scale:
			statistics[scale] += 1

print "Total transcripts:\t%s" % transcript_counts
print "Max length:\t%s" % max_len
print "Min length:\t%s" % min_len
print "Total length:\t%s" % total_len
print "Mean length:\t%s" % mean_len
print "Median length:\t%s" % median_len
print "Contig N10:\t%s" % N10_len
print "Contig N50:\t%s" % N50_len
print "Contig N90:\t%s" % N90_len
print "GC content:\t%s" % round(gc/total_len*100, 2)
print "============================="
print "Length\tCounts"
for scale in scales:
	print ">=%s\t%s" % (scale, statistics[scale])

with open("%s.length_tracking" % sys.argv[1], "w") as op:
	op.write("\n".join(map(str,transcript_lens)))
