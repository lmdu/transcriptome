#!/usr/bin/env python
import sys
import pyfaidx

inFasta, clustMap, outFasta = sys.argv[1:]

transcriptome = pyfaidx.Fasta(inFasta)

clustDict = {}
with open(clustMap) as fh:
	for line in fh:
		transId, clustId = line.strip().split()
		try:
			clustDict[clustId].append(transId)
		except KeyError:
			clustDict[clustId] = [transId]

with open(outFasta, "w") as out:
	for cluster in clustDict:
		names = clustDict[cluster]
		out.write(">%s\n" % cluster)
		if len(names) == 1:
			out.write("%s\n" % transcriptome[names[0]][:].seq)
		else:
			max_len = 0
			max_name = None
			for name in names:
				if len(transcriptome[name]) > max_len:
					max_len = len(transcriptome[name])
					max_name = name
			out.write("%s\n" % transcriptome[max_name][:].seq)