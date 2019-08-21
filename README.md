# MIS Timetable Splitter

Split a combined HTML exported Student Timetable from a common Management Information System (MIS) product, that shall  remain nameless, into individual per-student files.

## Usage

 * Perform an HTML export from the Management Information System (perhaps through a menu structure not dissimilar to **Reports** > **Timetables** > **Student Timetables**) and have this available as the input file.
 * Have an empty folder ready for the individual student timetable files. This is your output path.
 * Then run this tool with `-i INPUTFILE -o OUTPUTPATH`.

### Arguments
    -h, --help                             show a help message and exit
    -i INPUTFILE, --input INPUTFILE        The input HTML file.
    -o OUTPUTPATH, --output OUTPUTPATH     The directory for the output files
    --force                                Allow this script to overwrite files in the output folder.

## Licence

Copyright 2019 Test Valley School.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.  You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0.

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS,  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.