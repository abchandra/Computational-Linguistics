import sys

of = open(sys.argv[1], 'r') # this is the output of the spellchecker
cf = open(sys.argv[2], 'r') # this is the target correction file

correct = 0.0

#reading both files as lists of lines
lineso = of.readlines()
linesc = cf.readlines()

#if the files are different lengths we exit
if len(lineso) != len(linesc):
    print "Your files are not the same length...exiting"
    exit(1)

for lineo in lineso: #go through each of our outputs
    linec = linesc.pop(0).strip() #grabbing next line from corrections file and stripping new lines off
    # the corrections file may have multiple words so we split
    cwords = linec.split(', ')
    for corr in cwords: #go through each possible correction and compare to our output
        # we increment 'correct' if our output matches any of the target words
        if corr == lineo.strip(): correct += 1 #compare correction to our output with newlines removed
    
print "Accuracy is", correct/len(lineso)
