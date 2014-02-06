#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import xlwt
import time

from optparse import OptionParser
from xml.dom import minidom

def create_xls(name='Sheet 1'):
    wb = xlwt.Workbook()
    ws = wb.add_sheet(name)
    return wb, ws

def parse(filename, outfile, nodata=''):
    start = time.clock()

    xmlf = minidom.parse(filename)
    members = xmlf.getElementsByTagName('MEMBER')
    wb, ws = create_xls()

    row_pointer = 0

    for member in members:

        col_pointer = 0

        for tag in member.childNodes:
            # Skip the empty whitespace in the file
            if tag.nodeType == minidom.Node.TEXT_NODE:
                continue

            fieldname = tag.nodeName.replace('_', ' ').capitalize()
            offset = 0

            if row_pointer == 0:
                ws.write(row_pointer, col_pointer, fieldname)
                offset = 1  # shift down now for the data row

            if tag.firstChild:
                content = tag.firstChild.nodeValue
            else:
                content = nodata

            ws.write(row_pointer + offset, col_pointer, content)

            # Now move to the next column
            col_pointer += 1

        # And onto the next row, need to go up by 2 though for the first row
        if row_pointer == 0:
            row_pointer += 2
        else:
            row_pointer += 1

        if row_pointer % 100 == 0:
            print "On row {}".format(row_pointer)

    wb.save(outfile)

    end = time.clock()
    print "Processed {0} entries in {1:.2f}s".format(row_pointer, end - start)

def run():
    parser = OptionParser()
    parser.add_option("-f", "--file", default='out.xls', dest="filename", help="write output to file.xls", metavar="FILE")
    parser.add_option("-n", "--nodata", default='', dest="nodata", help="What to write for missing data", metavar="string")
    options, args = parser.parse_args()

    if len(args) != 1:
        print "You must provide the input XML file"
        sys.exit(2)

    parse(args[0], options.filename, nodata=options.nodata)


if __name__ == '__main__':
    run()
