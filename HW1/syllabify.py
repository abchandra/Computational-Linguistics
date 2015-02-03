#!/usr/bin/env python

# Syllabify.py (python 2.7.6)
# Author: Abhishek Chandra
# email: abhishek.chandra@yale.edu
# Desc: HW1 for LING 227 at Yale

import sys
import re
import syllabify_base
#Write errmsg to stderr and exit

def die(errmsg):
	exit(sys.stderr.write("Error:"+errmsg+"\n"))

# this dictionary encodes the sonority level of each phoneme
son = { 'AA': 4, 'AE' : 4, 'AH' : 4, 'AO' : 4, 'AW' : 4, 'AY' : 4,
             'B'  : 0, 'CH' : 0, 'D' : 0, 'DH' : 0, 'EH' : 4, 'ER' : 4,
             'EY' : 4, 'F': 0, 'G': 0, 'HH': 0, 'IH': 4, 'IY': 4, 'JH': 0,
             'K': 0, 'L': 2, 'M': 1, 'N': 1, 'NG': 1, 'OW': 4, 'OY': 4,
             'P': 0, 'R': 2, 'S': 0, 'SH': 0, 'T': 0, 'TH': 0, 'UH': 4,
             'UW': 4, 'V': 0, 'W': 3, 'Y': 3, 'Z': 0, 'ZH': 0}

freq = { 'CCV': 0, 'CCVC': 0,'CV': 0, 'CVC': 0, 'CVCC': 0, 'CVCCC': 0, 'V': 0, 
'VC': 0,  'VCC': 0} 
#A pseudo-enum for states
coda = 0
onset = 1
initial_onset = 10

#updates the freq dictionary based on what type of syllables
#the pronounciation of the word contains
def update_frequency(line):
	lst = re.split(r'\s',line)
	c = 'C'
	v = 'V'
	syll_type=''
	for ph in lst:
		#+
		if ph == '+' and syll_type in freq:
				freq[syll_type] += 1
				syll_type = ''
		#ignore other non-phonemes
		elif not ph in son:
			continue
		#V
		elif son[ph] == 4:
			syll_type += v
		#C
		else:
			syll_type += c

	#update last syllable, if any		
	if syll_type in freq:
		freq[syll_type] += 1

def show_frequency():
	count = 0
	for key,val in freq.items():
		count+=val

	for key,val in freq.items():
		print "Frequency of %s :\t %.2f" % (key, 100 * val/float(count))
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
			#set onset, mode to initial
			lastonset = initial_onset
			mode = coda
			#initialize output list
			output_lst = []
			for ph in lst:
				#ignore non-phonemes
				if not ph in son:
					continue
				#always add S to current onset
				if ph == 'S' and mode == onset:
					lastonset = son[ph]
				#nuclei 
				elif son[ph] == 4:
					#if onset state, finish syllable
					if mode == onset:
						output_lst.append('+')
						lastonset = initial_onset
					#else, enter onset state
					else:
						mode = onset
				#onset
				elif mode == onset:
					#onset maximization 
					if lastonset - son[ph] < 2:
						output_lst.append('+')
						lastonset = initial_onset
						mode = coda
					else:
						lastonset = son[ph]
				#Append current phoneme to output list
				output_lst.append(ph)
			#create output string from list
			output_lst.append(lst[-1])
			output_lst=output_lst[::-1]
			syllabified_line = ' '.join(output_lst)
			#part2
			# pdate
			#print output
			print syllabified_line
			update_frequency(syllabified_line)
		show_frequency()
except IOError:
	die("unable to open file "+sys.argv[1])

