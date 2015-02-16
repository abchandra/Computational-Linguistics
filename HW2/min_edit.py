#!/usr/bin/env python

# min_edit.py (python 2.7.6)
# Author: Abhishek Chandra
# email: abhishek.chandra@yale.edu
# Desc: HW2 for LING 227 at Yale

import sys
def die(errmsg):
	exit(sys.stderr.write("Error:"+errmsg+"\n"))

def ins_cost(s):
	return 1
def del_cost(s):
	return 1.1
def subst_cost(s,t):
	return 2*(s!=t)

#Credit to unutbu for this elegant pretty print function 
#http://stackoverflow.com/questions/17870612/printing-a-two-dimensional-array-in-python
def print_matrix(dist):
	print('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
      for row in dist]))

def min_edit_dist(target, source):
	n = len(target)
	m = len(source)
	distance = [[0.0 for x in range(m+1)] for x in range(n+1)]
	for i in range(1,n+1):
		distance[i][0] = distance[i-1][0] + ins_cost(target[i-1])
	for j in range(1,m+1):
		distance[0][j] = distance[0][j-1] + del_cost(source[j-1])
	for i in range(1,n+1):
		for j in range(1,m+1):
			sub_cost = subst_cost(source[j-1],target[i-1])								
			distance[i][j] = min(distance[i-1][j]+ins_cost(target[i-1]), #insertion
				distance[i-1][j-1] + sub_cost,														 #substitution
				distance[i][j-1] + del_cost(source[j-1]))									 #deletion
			#Damerau-Levenshtein Distance : 															transposition
			#pseudo code from http://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance
			if i > 1 and j > 1 and target[i-1]==source[j-2] and target[i-2]==source[j-1]:
				distance[i][j] = min (distance[i][j],distance[i-2][j-2] + 1)
	return distance [n][m]

#Soundex: heuristics implemented from instructions at
#http://en.wikipedia.org/wiki/Soundex
def soundex(s):
	if len(s) < 1:
		return "000"
	code = ['0','1','2','3','0','1','2','0','0','2','2','4','5',
	'5','0','1','2','6','2','3','0','1','0','2','0','2']
	vow = ['a','e','i','o','u','y','h','w']
	def getcode(i):
		code[s[i]-'a']
	i=0	
	#First letter of result is a consonant (but not y,h,w)
	while i < len(s) - 1 and s[i] in vow:
		i+=1
	res = s[i]
	while len(code) < 4 and i < len(s):
		#ignore vow
		if s[i] in vow:
			continue
		#If two or more letters with the same number are adjacent in the 
		#original name (before step 1), only retain the first letter
		if getcode[i] == getcode[i-1]:
			continue
		# two letters with the same number separated by 'h' or 'w' 
		# are coded as a single number
		if i> 1 and getcode[i] == getcode[i-2] and s[i] in ['h','w']:
			continue
		#Append code to result
		res = res + getcode(i)
	#Pad result with 0s if needed
	while len(res) < 4:
		res = res + '0'
	return res

def vow_count(s):
	x = 0
	for c in s:
		if c in ['a','e','i','o','u']:
			x+=1
	return x
###MAIN###
#Check input length
if len(sys.argv) != 3:
	die("invalid command. Expected: spelling_correction.py dictfile misspeltfile")

try:
	with open(sys.argv[2]) as f:
		for line in f:
			source = line.rstrip('\n')
			dist = 4*len(source)
			correct = source
			source_soundex = soundex(source)
			try:
				with open(sys.argv[1]) as dic:
					for val in dic:
						target = val.rstrip('\n')
						x = min_edit_dist(target,source)
						if dist > x or dist == x and soundex(target) == source_soundex:
							dist = x
							correct = target
			except IOError:
				die("unable to open file "+sys.argv[1])
			print correct
except IOError:
	die("unable to open file "+sys.argv[2])