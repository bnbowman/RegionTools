#!/usr/bin/env python
from __future__ import absolute_import

__author__ = "Brett Bowman"

import re, logging
from itertools import groupby
from collections import defaultdict

import h5py
import numpy as np

from pbcore.io import FastaReader, CmpH5Reader

from RegionTools._version import __version__
from RegionTools.options import options, parseOptions

class RegionAnalyzer(object):
    """
    A tool for analyzing barcode sequences with Quiver
    """
    def __init__(self):
        self._inputReader = None
        self._reader = None
        self._referenceSeqs = None
        self._referenceNames = None
        self._referenceLookup = None
        self._regionDict = None

    def _setupLogging(self):
        if options.quiet:
            logLevel = logging.ERROR
        elif options.verbosity >= 2:
            logLevel = logging.DEBUG
        elif options.verbosity == 1:
            logLevel = logging.INFO
        else:
            logLevel = logging.WARNING
        logFormat = '[%(levelname)s] %(message)s'
        logging.basicConfig(level=logLevel, format=logFormat)

    def _loadAlignments(self):
        logging.info("Loading alignment data")
        self._reader = CmpH5Reader( options.cmpH5Filename )
        self._reader.attach( options.basH5Fofn )

    def _readAlignmentRefs(self):
        referenceNames = {}
        referenceLookup = {}
        for row in self._reader.referenceInfoTable:
            referenceNames[row[0]] = row[3]
            referenceLookup[row[3]] = row[0]
        self._referenceNames = referenceNames
        self._referenceLookup = referenceLookup

    def _loadReferences(self):
        logging.info("Loading reference sequences")
        referenceSeqs = {}
        nameSet = set()      # Temporary storage to prevent duplicates
        for record in FastaReader( options.referenceFasta ):
            name = record.name.split()[0]
            # Catch duplicate names
            if name in nameSet:
                msg = "Duplicate reference name - {0}".format(name)
                logging.error( msg )
                raise ValueError( msg )
            nameSet.add( name )
            # Skip unused sequences
            if name not in self._referenceLookup.keys():
                logging.debug("Unused reference sequence '{0}' -- skipping".format(name))
                continue
            idx = self._referenceLookup[name]
            referenceSeqs[idx] = record.sequence
        self._referenceSeqs = referenceSeqs

    def _createRegionDict(self):
        logging.info("Creating region dictionary")
        regions = defaultdict(list)
        for idx, seq in self._referenceSeqs.iteritems():
            hps = [''.join(list(g)) for k, g in groupby(seq)]
            start = len(hps[0])       # Skip the first position
            for hp in hps[1:]:
                end = start + len(hp)
                if len(hp) >= options.minSize:
                    region = (idx, start, end)
                    regions[hp].append( region )
                start = end
        self._regionDict = regions

    @property
    def referenceNames(self):
        return self._referenceDict.keys()

    def main(self):
        parseOptions()
        self._setupLogging()
        self._loadAlignments()
        self._readAlignmentRefs()
        self._loadReferences()
        self._createRegionDict()

        logging.info("h5py version: %s" % h5py.version.version)
        logging.info("hdf5 version: %s" % h5py.version.hdf5_version)
        logging.info("RegionTools version: %s" % __version__)

        logging.info("Starting.")
        logging.info(options.cmpH5Filename)
        logging.info(options.referenceFasta)
        logging.info(options.basH5Fofn)

        for idx, start, end in self._regionDict['CCCCCCC']:
            reads = self._reader.readsInRange(idx, start, end)
            filtered = [r for r in reads if r.spansReferenceRange(start-1, end+1)]
            clipped = [r.clippedTo(start-1, end+1) for r in filtered]
            for read in clipped:
                print read.read(aligned=False, orientation='genomic')

        return 0

def main():
    return RegionAnalyzer().main()
