#!/usr/bin/env python
import sys
import re
import syllabify_base
#Write errmsg to stderr and exit

def die(errmsg) :
	exit(sys.stderr.write("Error:"+errmsg+"\n"))


# this dictionary encodes the sonority level of each phoneme
son = { 'AA': 4, 'AE' : 4, 'AH' : 4, 'AO' : 4, 'AW' : 4, 'AY' : 4,
             'B'  : 0, 'CH' : 0, 'D' : 0, 'DH' : 0, 'EH' : 4, 'ER' : 4,
             'EY' : 4, 'F': 0, 'G': 0, 'HH': 0, 'IH': 4, 'IY': 4, 'JH': 0,
             'K': 0, 'L': 2, 'M': 1, 'N': 1, 'NG': 1, 'OW': 4, 'OY': 4,
             'P': 0, 'R': 2, 'S': 0, 'SH': 0, 'T': 0, 'TH': 0, 'UH': 4,
             'UW': 4, 'V': 0, 'W': 3, 'Y': 3, 'Z': 0, 'ZH': 0}

#A pseudo-enum for states
coda = 0
onset = 1
initial_onset = 10

###MAIN###

#Check input length
if len(sys.argv) != 2:
	die("invalid command. Expected: syllabify.py filename")

try:
	with open(sys.argv[1]) as f:
		for line in f:
			#split line by spaces
			lst = re.split(r'\s',line)
			lst = lst[::-1]
			# print lst
			lastonset = initial_onset
			mode = coda
			output_lst = []
			for ph in lst:
				if not ph in son:
					continue
				if not ph == 'S':
					if son[ph] == 4:
						if mode == onset:
							# print "appending plus"
							output_lst.append('+')
							lastonset = initial_onset
						else:
							# print "begin building onset"
							mode = onset
					elif mode == onset:
						if lastonset - son[ph] < 2:
							# print ph + str(son[ph] - lastonset) + " is the end of onset, append plus"
							output_lst.append('+')
							lastonset = initial_onset
							mode = coda
						else:
							lastonset = son[ph]
				elif mode == onset:
					lastonset = son[ph]
				output_lst.append(ph)
			output_lst.append(lst[-1])
			output_lst=output_lst[::-1]
			syllabified_line = ' '.join(output_lst)
			print syllabified_line
			#implement principles
			#write to file
except IOError:
	die("unable to open file "+sys.argv[1])

