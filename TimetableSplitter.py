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

parser = argparse.ArgumentParser(description='Split a combined HTML exported Student Timetable from a common Management Information System (MIS) product that shall remain nameless into individual per-student files.')
parser.add_argument('--input', dest='inputfile', help='The input HTML file.')
parser.add_argument('--output',dest='outputdir', help='The directory for the output files')

args = parser.parse_args()

print(args.inputfile)
