#!/usr/bin/env python3
#
# MIS Timetable Splitter
#
# Split a combined HTML exported Student Timetable from a common Management
# Information System (MIS) product, that shall remain nameless, into individual
# per-student files.
#
#

from html.parser import HTMLParser
import argparse
import re
import os


class TimetableParser(HTMLParser):
    # each timetable begins with a <td class="TitleBold">, which is convenient enough

    def __init__(self):
        super().__init__()
        self.tt_regex = re.compile(r'Timetable\s*')
        self.splitpoints = []
        self.titles = []

    def handle_starttag(self, tag, attrs):
        pass
    
    def handle_endtag(self, tag):
        #print("End tag", tag)
        pass

    def handle_data(self, data):
        if self.tt_regex.match(data):
            print("MATCH at " + str(self.getpos()[0]) + "," + str(self.getpos()[1]))
            self.splitpoints.append(self.getpos())
            self.titles.append(data)
        

# argument parsing
argparser = argparse.ArgumentParser(description='Split a combined HTML exported Student Timetable from a common Management Information System (MIS) product, that shall remain nameless, into individual per-student files.')
argparser.add_argument('-i', '--input', dest='inputfile', help='The input HTML file.', required=True, type=argparse.FileType('r'))
argparser.add_argument('-o', '--output',dest='outputpath', help='The directory for the output files', required=True)

# main execution
args = argparser.parse_args()

tt_parser = TimetableParser()

tt_parser.feed(args.inputfile.read())

# with identified split points, split file into individual items??
args.inputfile.seek(0)
lines = args.inputfile.readlines()

for i in range(0, len(tt_parser.splitpoints)):
    currentsplit = tt_parser.splitpoints[i]
    currentline = lines[currentsplit[0]-1]
    
    try:
        nextsplit = tt_parser.splitpoints[i+1]
    except IndexError:
        # at the end of the loop, simply split from the current split point to the end of the line
        nextsplit = (currentsplit[0]-1, len(currentline))
    
    individual_tt_filename = os.path.join(args.outputpath, tt_parser.titles[i] + '.html')
    with open(individual_tt_filename, 'w') as outputfile:
        print("Writing " + individual_tt_filename)
        outputfile.write(currentline[currentsplit[1]:nextsplit[1]])
        # now we need to clean up that HTML... :(