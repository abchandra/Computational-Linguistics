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
	return 1
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
	distance = [[0 for x in range(m+1)] for x in range(n+1)]
	for i in range(1,n+1):
		distance[i][0] = distance[i-1][0] + ins_cost(target[i-1])
	for j in range(1,m+1):
		distance[0][j] = distance[0][j-1] + del_cost(source[j-1])
	for i in range(1,n+1):
		for j in range(1,m+1):
			sub_cost = subst_cost(source[j-1],target[i-1])
			distance[i][j] = min(distance[i-1][j]+ins_cost(target[i-1]),
				distance[i-1][j-1] + sub_cost,
				distance[i][j-1] + del_cost(source[j-1]))
			#Damerau-Levenshtein Distance
			if i > 1 and j > 1 and target[i-1]==source[j-2] and target[i-2]==source[j-1]:
				distance[i][j] = min (distance[i][j],distance[i-2][j-2] + 1)
	# print_matrix(distance)
	return distance [n][m]

###MAIN###
# min_edit_dist("intention","execution")
#Check input length
if len(sys.argv) != 3:
	die("invalid command. Expected: spelling_correction.py dictfile misspeltfile")

try:
	with open(sys.argv[2]) as f:
		for source in f:
			dist = 2*len(source)
			correct = source
			try:
				with open(sys.argv[1]) as dic:
					for target in dic:
						x = min_edit_dist(target.rstrip('\n'),source.rstrip('\n'))
						if dist >= x:
							dist = x
							correct = target.rstrip('\n')
			except IOError:
				die("unable to open file "+sys.argv[1])
			print correct
except IOError:
	die("unable to open file "+sys.argv[2])