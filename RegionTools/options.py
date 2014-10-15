from __future__ import absolute_import

import argparse, h5py, os, sys
from RegionTools._version import __version__

__author__ = "Brett Bowman"

options = argparse.Namespace()

def parseOptions():
    """
    Parse the options and perform some due diligence on them
    """
    desc = "Compute the likelihood of sequences coming from a list of barcodes."
    parser = argparse.ArgumentParser(description=desc, add_help=False)

    def canonicalizedFilePath(path):
        return os.path.abspath(os.path.expanduser(path))

    def checkInputFile(path):
        if not os.path.isfile(path):
            parser.error("Input file %s not found." % (path,))

    def checkOutputFile(path):
        try:
            f = open(path, "a")
            f.close()
        except:
            parser.error("Output file %s cannot be written." % (path,))

    basics = parser.add_argument_group("Basic required options")
    basics.add_argument(
        "cmpH5Filename",
        type=canonicalizedFilePath,
        metavar="CMP.H5",
        help="The filename of the input Bas.H5 file")
    basics.add_argument(
        "referenceFasta",
        type=canonicalizedFilePath,
        metavar="REFERENCE_FASTA",
        help="The reference sequences of interest in FASTA format")
    basics.add_argument(
        "basH5Fofn",
        type=canonicalizedFilePath,
        metavar="BARCODE_FASTA",
        help="The filename of the barcode FASTA")
    basics.add_argument(
        "-o", "--outputFilename",
        type=str,
        default=os.path.join(os.getcwd(), "output.csv"),
        metavar="CSV",
        help="The filename of the CSV to output barcode scoring data to.")
    basics.add_argument(
        "-m", "--minSize",
        type=int,
        default=3,
        metavar="INT",
        help="The minimum size of a homopolymer context to record")

    debugging = parser.add_argument_group("Verbosity and debugging/profiling")
    debugging.add_argument("--help", "-h",
                           action="help")
    debugging.add_argument(
        "--nZmws",
        default=-1,
        type=int,
        help="Label only the first N ZMWs for testing purposes.")
    debugging.add_argument(
        "--verbose", "-v",
        dest="verbosity",
        action="count",
        help="Set the verbosity level.")
    debugging.add_argument(
        "--quiet",
        dest="quiet",
        action="store_true",
        help="Turn off all logging, including warnings")
    class PrintVersionAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            print "  RegionTools version: %s" % __version__
            print "  h5py version: %s" % h5py.version.version
            print "  hdf5 version: %s" % h5py.version.hdf5_version
            sys.exit(0)
    debugging.add_argument("--version",
                           nargs=0,
                           action=PrintVersionAction)

    parser.parse_args(namespace=options)

    for path in (options.cmpH5Filename, options.referenceFasta, options.basH5Fofn):
        if path is not None:
            checkInputFile(path)

    for path in (options.outputFilename,):
        if path is not None:
            checkOutputFile(path)

    options.shellCommand = " ".join(sys.argv)
