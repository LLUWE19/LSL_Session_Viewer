"""
A general purpose reader for LSL recording sessions using the Lab Recorder. Open an XDF file and print out the data
that was recorded for each stream.

Must specify an XDF file to use on the command line (or edit the script to include here)
"""
import argparse
import os
import logging
import pyxdf


try:
    # Pull and prepare arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Specify an XDF file containing a recording session.")
    args = parser.parse_args()

    """Load a specific recording session"""
    if args.file:
        # Specify the xdf file and session to load
        # To reach this, try the command below:
        # >> python load_lsl_recording.py --file recording_1.xdf
        print('Opening recording session in', args.file)
        fname = os.path.abspath(os.path.join(os.path.dirname(__file__), args.file))
        with open(fname, "r") as rs:
            streams, fileheader = pyxdf.load_xdf(fname)

        # logging.basicConfig(level=logging.DEBUG)  # Use logging.INFO to reduce output.

        print("Found {} streams:".format(len(streams)))

        # Print out the stream descriptions
        for ix, stream in enumerate(streams):
            print("Stream {}: {} - type {} - uid {} - shape {} at {} Hz (effective {} Hz)".format(
                ix + 1, stream['info']['name'][0],
                stream['info']['type'][0],
                stream['info']['uid'][0],
                (int(stream['info']['channel_count'][0]), len(stream['time_stamps'])),
                stream['info']['nominal_srate'][0],
                stream['info']['effective_srate'])
            )
            if any(stream['time_stamps']):
                print("\tDuration: {} s".format(stream['time_stamps'][-1] - stream['time_stamps'][0]))

        # Print each streams records
        for r, stream in enumerate(streams):
            print(streams[r]['info']['name'][0])
            print("Record       Stamp           Data")
            for p, stamp in enumerate(stream['time_stamps']):
                print("{}       {}      {}".format(p, streams[r]['time_stamps'][p], streams[r]['time_series'][p]))
            print()
    else:
        print("No xdf specified")

finally:
    print("done.")
