"""top level run script"""

import argparse
import logging
from pathlib import Path
from typing import Union

from hdmf_zarr import NWBZarrIO
from pynwb import NWBHDF5IO

# From multiple input NWB files, in the future, I need to figure out a wayu to detrermine which nwb is which. For now, only the ophys nwb has the processing file so if it exists, I will assume that it is the primary nwb
# # append ancillary data to the acquisition nwb
# Export appended nwb to the results folder


# Load the remote NWB file from DANDI
def combine_nwb_files(
    ophys_nwb_fp: Path,
    eye_tracking_nwb_fp: Path,
    behavior_nwb_fp: Path,
    export_fp: Path,
):
    """Combine multiple NWB files into a single NWB file

    Parameters
    ----------
    ophys_nwb_fp : Path
        ophys movie
    eye_tracking_nwb_fp : Path
        eye tracking nwb
    behavior_nwb_fp : Path
        behavior nwb
    export_fp : Path
        export file path
    """
    ophys_io = determine_io(ophys_nwb_fp)
    behavior_io = determine_io(behavior_nwb_fp)
    eye_tracking_io = determine_io(eye_tracking_nwb_fp)

    with ophys_io(ophys_nwb_fp, "r") as io:
        ophys_nwb = io.read()
        with behavior_io(behavior_nwb_fp, "r") as read_io:
            behavior_nwb = read_io.read()
            for name, data in behavior_nwb.acquisition.items():
                if name not in ophys_nwb.acquisition:
                    data.reset_parent()
                    ophys_nwb.add_acquisition(data)
            for name, data in behavior_nwb.processing.items():
                if name not in ophys_nwb.processing:
                    data.reset_parent()
                    ophys_nwb.add_processing_module(data)
            for name, data in behavior_nwb.analysis.items():
                if name not in ophys_nwb.analysis:
                    data.reset_parent()
                    ophys_nwb.add_analysis(data)
            for name, interval in behavior_nwb.intervals.items():
                if name not in ophys_nwb.intervals:
                    data.reset_parent()
                    ophys_nwb.add_interval(interval)
        with eye_tracking_io(eye_tracking_nwb_fp, "r") as read_io:
            eye_tracking_nwb = read_io.read()
            for name, data in eye_tracking_nwb.acquisition.items():
                if name not in ophys_nwb.acquisition:
                    data.reset_parent()
                    ophys_nwb.add_acquisition(data)
            for name, data in eye_tracking_nwb.processing.items():
                if name not in ophys_nwb.processing:
                    data.reset_parent()
                    ophys_nwb.add_processing_module(data)
            for name, data in eye_tracking_nwb.analysis.items():
                if name not in ophys_nwb.analysis:
                    data.reset_parent()
                    ophys_nwb.add_analysis(data)
            for name, interval in eye_tracking_nwb.intervals.items():
                if name not in ophys_nwb.intervals:
                    data.reset_parent()
                    ophys_nwb.add_interval(interval)
            with NWBZarrIO(export_fp, mode="w") as export_io:
                export_io.export(src_io=io, write_args=dict(link_data=False))


def determine_io(nwb_path: Path) -> Union[NWBHDF5IO, NWBZarrIO]:
    """determine the io type

    Parameters
    ----------
    nwb_path : Path
        path to the nwb file

    Returns
    -------
    Union[NWBHDF5IO, NWBZarrIO]
        the appropriate io object
    """
    if nwb_path.is_dir():
        return NWBZarrIO(nwb_path, mode="r")
    return NWBHDF5IO(nwb_path, mode="r")


def parse_args():
    """parse command line arguments"""
    argparser = argparse.ArgumentParser(description="Run the capsule")
    argparser.add_argument(
        "--input-dir", type=str, help="Input directory", default="/data/"
    )
    argparser.add_argument(
        "--output-dir", type=str, help="Output directory", default="/results/"
    )

    return argparser.parse_args()


def run():
    """basic run function"""
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    ophys_nwb = next(input_dir.glob("ophys/*.nwb"))
    behavior_nwb = next(input_dir.glob("behavior/*.nwb"))
    eye_tracking_nwb = next(input_dir.glob("eye_tracking/*.nwb"))
    export_fp = output_dir / "session"
    logging.info(
        "Combining NWB files, {}, {}, {}, to {}".format(
            ophys_nwb, behavior_nwb, eye_tracking_nwb, export_fp
        )
    )
    combine_nwb_files(ophys_nwb, eye_tracking_nwb, behavior_nwb, export_fp)
    logging.info("Done")


if __name__ == "__main__":
    run()
