#!python

"""
    Python program to make copies of a file
     but dropping a few random lines during copying.

    Given multiple output files, will make multiple copies of the single
     source file - each copy having different random lines omitted.

    Intended to process .CSV files, treats file content as text lines.
    
    Anticipated to be run from the command line:
     python line_drop.py -l <losses> [ in-file [ out-file ... ]]
       -l = the number of lines dropped (defaults to 5)

    Created 01 Feb 2016  by Martin Savidge  for Mark Briers
     for use in customising .CSV format datasets for course exercises
"""

import sys
import string
import getopt
import random

from sets import Set

def main(argv):
    """ Process files - everything is done in main() """

    losses = 5 # Number of lines to lose - initialised to default

    # Process command line arguments: -h -l in-file out-file ...
    try:
        opts, args = getopt.getopt(argv,"hl:")
    except getopt.GetoptError:
        print('line_drop.py -l <losses> [ in-file [ out-file ... ]]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('line_drop.py -l <losses> [ in-file [ out-file ... ]]')
            print('             -l number of lines to lose [default {}]'.format(losses))
            print('  Make copies of in-file with a few random lines omitted from the copies.') 
            sys.exit()
        elif opt in ("-l"):
            losses = int(arg)

    # Source file path - string
    if len(args) > 0:
        inputfile = args[0]
    else:     
        inputfile = raw_input("Input filename: ")

    # Copies - list of strings
    if len(args) > 1:
        outputfiles = args[1:]
    else:     
        outputfiles = raw_input("Output filename(s): ").split()

    # Discover the number of lines in the source file
    try:
        print('Reading file "{}"...'.format(inputfile))
        lines = 0
        with open(inputfile, "r") as inf:
            for line in inf:
                lines += 1
    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
        sys.exit(2)
    print("Entries found: {}".format(lines))

    # Sequence through the output files
    for outputfile in outputfiles:
        
        # Select the line numbers of the lines to be dropped
        drops = Set()
        while len(drops) < losses:
            drops.add(random.randint(0, lines))

        try:
            # Open the source file
            with open(inputfile, "r") as inf:
                # Create the new file
                print('Creating file "{}" - dropping lines {}'.\
                               format(outputfile, sorted(drops)))
                with open(outputfile, "w") as outf:
                    # Copy non-dropped lines to the new file
                    lineNo = 0
                    for line in inf:
                        lineNo += 1
                        if lineNo not in drops:
                            outf.write(line)
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
    # end for outputfile in outputfiles:
# end main()


# Ensure starting point is main()
if __name__ == "__main__":
    main(sys.argv[1:])

