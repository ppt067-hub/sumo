#!/usr/bin/env python
# Eclipse SUMO, Simulation of Urban MObility; see https://eclipse.org/sumo
# Copyright (C) 2012-2020 German Aerospace Center (DLR) and others.
# This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v2.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v20.html
# SPDX-License-Identifier: EPL-2.0

# @file    turnCount2EdgeCount.py
# @author  Jakob Erdmann
# @date    2020-02-09

"""
Converts turn-count data into edgeData
"""
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import random
from argparse import ArgumentParser
from collections import defaultdict
import subprocess

if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import sumolib  # noqa


def get_options(args=None):
    parser = ArgumentParser(description="Sample routes to match counts")
    parser.add_argument("-t", "--turn-file", dest="turnFile",
            help="Input turn-count file")
    parser.add_argument("-o", "--output-file", dest="out",
            help="Output edgeData file")
    parser.add_argument("--edgedata-attribute", dest="edgeDataAttr", default="entered",
            help="Write edgeData counts with the given attribute")
    parser.add_argument("--turn-attribute", dest="turnAttr", default="probability",
            help="Read turning counts from the given attribute")

    options = parser.parse_args(args=args)
    if options.turnFile is None or options.out is None:
        parser.print_help()
        sys.exit()
    return options

def main(options):
    with open(options.out, 'w') as outf:
        sumolib.writeXMLHeader(outf, "$Id$", "meandata")  # noqa
        for interval in sumolib.xml.parse(options.turnFile, 'interval'):
            outf.write('    <interval begin="%s" end="%s">\n' % (
                interval.begin, interval.end))
            for fromEdge in interval.fromEdge:
                count = int(sum([float(getattr(toEdge, options.turnAttr)) for toEdge in fromEdge.toEdge]))
                outf.write('        <edge id="%s" %s="%s"/>\n' % (
                    fromEdge.id, options.edgeDataAttr, count))
            outf.write('    </interval>\n')
        outf.write('</meandata>\n')

if __name__ == "__main__":
    main(get_options())
