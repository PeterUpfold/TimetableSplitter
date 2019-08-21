#!/usr/bin/env python3
#
# MIS Timetable Splitter
#
# Split a combined HTML exported Student Timetable from a common Management
# Information System (MIS) product, that shall remain nameless, into individual
# per-student files.
#
#
# Copyright 2019 Test Valley School.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from html.parser import HTMLParser
import argparse
import re
import os


class TimetableParser(HTMLParser):
    # each timetable begins with a <td class="TitleBold">, with "Timetable" written in it, which is convenient enough

    def __init__(self):
        super().__init__()
        self.tt_regex = re.compile(r'Timetable\s*')
        self.splitpoints = []
        self.titles = []
        self.in_style = False

    def handle_starttag(self, tag, attrs):
        if tag == 'style':
            self.in_style = True
    
    def handle_endtag(self, tag):
        self.in_style = False

    def handle_data(self, data):
        if self.in_style:
            self.style_data = data
        elif self.tt_regex.match(data):
            print("Matched a new item '" + data + "' starting at line " + str(self.getpos()[0]) + ", col " + str(self.getpos()[1]))
            self.splitpoints.append(self.getpos())
            self.titles.append(data)
        

# argument parsing
argparser = argparse.ArgumentParser(description='Split a combined HTML exported Student Timetable from a common Management Information System (MIS) product, that shall remain nameless, into individual per-student files.')
argparser.add_argument('-i', '--input', dest='inputfile', help='The input HTML file.', required=True, type=argparse.FileType('r'))
argparser.add_argument('-o', '--output',dest='outputpath', help='The directory for the output files', required=True)
argparser.add_argument('--force', dest='force', help='Allow this script to overwrite files in the output folder.', action='store_true')

# main execution
args = argparser.parse_args()

tt_parser = TimetableParser()

# check output path
if not os.path.exists(args.outputpath):
    raise ValueError("The output path specified does not exist.")

if not os.path.isdir(args.outputpath):
    raise ValueError("The output path specified is not a directory.")

if not args.force and len(os.listdir(args.outputpath)) > 0:
    raise ValueError("The output path is not empty. To allow overwriting of files with the same name, re-run with --force.")

# have the parser identify points at which we will split the HTML file
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

        # write header
        outputfile.write('<html><head><title>' + tt_parser.titles[i] + '</title>')

        # write the style tags
        outputfile.write('<style type="text/css">')
        outputfile.write(tt_parser.style_data)
        outputfile.write('</style>')

        outputfile.write('</head><body>')

        # this is hacky to a significant degree, but we split the original file part way through a tag, so we'll re-create
        # the table and title class
        outputfile.write('<table><tr><td class="TitleBold">')
        outputfile.write(currentline[currentsplit[1]:nextsplit[1]])
        