#!/usr/bin/env python
from __future__ import absolute_import

__author__ = "Brett Bowman"

import logging, string, math
from collections import defaultdict
from pkg_resources import Requirement, resource_filename
from pbcore.io import FastaReader

import h5py
import numpy as np

from RegionTools._version import __version__
from RegionTools.options import options, parseOptions

class RegionAnalyzer(object):
    """
    A tool for analyzing barcode sequences with Quiver
    """
    def __init__(self):
        self._inputReader = None
        self._sequenceZmws = None
        self._barcodeDict = None
        self._barcodeSequences = None
        self._barcodeNames = None
        self._barcodePairs = None
        self._barcodeLength = None
        self._configDict = None

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

    def _loadData(self):
        logging.info("Loading input data")

    def main(self):
        parseOptions()
        self._setupLogging()

        logging.info("h5py version: %s" % h5py.version.version)
        logging.info("hdf5 version: %s" % h5py.version.hdf5_version)
        logging.info("RegionTools version: %s" % __version__)

        logging.info("Starting.")
        logging.info(options.cmpH5Filename)
        logging.info(options.referenceFasta)
        logging.info(options.basH5Fofn)

        return 0

def main():
    return RegionAnalyzer().main()
