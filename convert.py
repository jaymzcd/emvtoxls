#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import os
import sys
import xlwt
import time

from optparse import OptionParser
from lxml import etree

#
# .,::::::  .        : :::      .::..:::.    .,::      .: :::     .::::::.
# ;;;;''''  ;;,.    ;;;';;,   ,;;;',;'``;.   `;;;,  .,;;  ;;;    ;;;`    `
#  [[cccc   [[[[, ,[[[[,\[[  .[[/  ''  ,[['    '[[,,[['   [[[    '[==/[[[[,
#  $$""""   $$$$$$$$"$$$ Y$c.$$"   .c$$P'       Y$$$P     $$'      '''    $
#  888oo,__ 888 Y88" 888o Y88P    d88 _,oo,   oP"``"Yo,  o88oo,.__88b    dP
#  """"YUMMMMMM  M'  "MMM  MP     MMMUP*"^^,m"       "Mm,""""YUMMM "YMmMY"
#


class EMVXMLFile(object):
    """
        We can't rely on them to supply good well formed XML, so lets replace anything
        bad as we see it on demand for iterparse to avoid it throwing exceptions
    """
    def __init__(self, filename):
        self.f = open(filename)

    def read(self, size=None):
        # For one they seem to pass through ampresands no problem despite
        # being invalid unless encoded as entities.
        return self.f.read(size).replace('&', '&amp;')


def create_xls(name='Sheet 1'):
    """
        Generate the XLS instance to write to
    """
    wb = xlwt.Workbook()
    ws = wb.add_sheet(name)
    return wb, ws

def get_header_style():
    """
        Return a XLS style for headers
    """
    font = xlwt.Font()
    font.bold = True
    style = xlwt.XFStyle()
    style.font = font
    return style

def parse(filename, outfile, nodata='', maxcount=None):
    """
        Read the given XML file and use the options given to create an XLS
        file as we go
    """
    start = time.clock()

    context = etree.iterparse(EMVXMLFile(filename), events=("start",))
    header_style = get_header_style()
    wb, ws = create_xls()

    ws.set_panes_frozen(True)
    ws.set_horz_split_pos(1)

    row_pointer = 0

    event, current_member = context.next()

    for event, current_member in context:

        col_pointer = 0

        # The xml is structured so that we have 2 nested levels
        # if that changes this logic will need to as well otherwise
        # further nesting would output as new rows
        children = current_member.getchildren()
        for tag in children:

            fieldname = tag.tag.replace('_', ' ').capitalize()
            offset = 0

            if row_pointer == 0:
                ws.write(row_pointer, col_pointer, fieldname, header_style)
                offset = 1  # shift down now for the data row

            if tag.text:
                content = tag.text
            else:
                content = nodata

            ws.write(row_pointer + offset, col_pointer, content)

            # Now move to the next column
            col_pointer += 1

        if len(children) > 0:
            # And onto the next row, need to go up by 2 though for the first row
            # to account for the header
            if row_pointer == 0:
                row_pointer += 2
            else:
                row_pointer += 1

            if row_pointer % 100 == 0:
                print "On row {}".format(row_pointer)

        # Now remove the current root element from memory - this is how to
        # avoid a huge memory error when dealing with 100Mb XML files :)
        current_member.clear()

        if maxcount is not None and row_pointer > maxcount:
            # Note we write out the count - 1 as we don't include the header
            # in this count! So 101 rows is 100 rows of actual data
            print "Exiting after {} entries".format(row_pointer - 1)
            break

    # Finally save and close the XLS sheet that's been made
    wb.save(outfile)

    end = time.clock()
    msg = "Processed {0} entries in {1:.2f}s".format(row_pointer - 1, end - start)
    print msg
    return msg

def check_filesize(filename):
    """
        Check the size of a given file
    """
    size = os.stat(filename).st_size
    filesize_meg = float(size) / 1024**2
    if filesize_meg > 30:
        print "Not yet suitable for large XML files"
        sys.exit(3)

def run():
    """
        Setup the command line tool and generate arguments
    """
    parser = OptionParser()
    parser.add_option("-f", "--file", default='out.xls', dest="filename", help="write output to file.xls", metavar="FILE")
    parser.add_option("-n", "--nodata", default='', dest="nodata", help="What to write for missing data", metavar="string")
    parser.add_option("-c", "--max", dest="maxcount", help="Stop after this many entries", metavar="int", type=int)
    options, args = parser.parse_args()

    if len(args) != 1:
        print "You must provide the input XML file"
        sys.exit(2)

    parse(args[0], options.filename, nodata=options.nodata, maxcount=options.maxcount)


if __name__ == '__main__':
    run()  # Start CLI
