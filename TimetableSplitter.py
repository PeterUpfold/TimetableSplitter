#!/usr/bin/env python3
#
# MIS Timetable Splitter
#
# Split a combined HTML exported Student Timetable from a common Management
# Information System (MIS) product that shall remain nameless into individual
# per-student files.
#
#

from html.parser import HTMLParser
import argparse
import re


class TimetableParser(HTMLParser):
    # each timetable begins with a <td class="TitleBold">, which is convenient enough

    def __init__(self):
        super().__init__()
        self.tt_regex = re.compile(r'Timetable\s*')
        self.splitpoints = []

    def handle_starttag(self, tag, attrs):
        #print("Start tag", tag)
        pass
        # if tag == 'td' and ('class', 'TableBorder') in attrs:
        #     # a new timetable begins -- dump any previous one to disk
        #     print(self.get_starttag_text())
                        
    
    def handle_endtag(self, tag):
        #print("End tag", tag)
        pass

    def handle_data(self, data):
        if self.tt_regex.match(data):
            print("MATCH at " + str(self.getpos()[0]) + "," + str(self.getpos()[1]))
        

# argument parsing
argparser = argparse.ArgumentParser(description='Split a combined HTML exported Student Timetable from a common Management Information System (MIS) product that shall remain nameless into individual per-student files.')
argparser.add_argument('-i', '--input', dest='inputfile', help='The input HTML file.', required=True, type=argparse.FileType('r'))
argparser.add_argument('-o', '--output',dest='outputpath', help='The directory for the output files', required=True)

# main execution
args = argparser.parse_args()

tt_parser = TimetableParser()

tt_parser.feed(args.inputfile.read())

for splitpoint in tt_parser.splitpoints:
    print(splitpoint)