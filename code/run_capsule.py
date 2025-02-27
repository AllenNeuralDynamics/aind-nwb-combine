"""top level run script"""

import argparse
import logging
import shutil
from pathlib import Path
from typing import Union

from hdmf_zarr import NWBZarrIO
from pynwb import NWBHDF5IO

# From multiple input NWB files, in the future, I need to figure out a wayu to detrermine which nwb is which. For now, only the ophys nwb has the processing file so if it exists, I will assume that it is the primary nwb
# # append ancillary data to the acquisition nwb
# Export appended nwb to the results folder


# Load the remote NWB file from DANDI
def add_nwb_attribute(
    main_io: Union[NWBHDF5IO, NWBZarrIO], sub_io: Union[NWBHDF5IO, NWBZarrIO]
) -> Union[NWBHDF5IO, NWBZarrIO]:
    """Get an attribute from the NWB file

    Parameters
    ----------
    main_io : Union[NWBHDF5IO, NWBZarrIO]
        the io object
    sub_io : Union[NWBHDF5IO, NWBZarrIO]
        the sub io object

    Returns
    -------
    Any
        the attribute
    """
    for field_name in sub_io.fields.keys()():
        for name, data in sub_io.get(field_name).items():
            data.reset_parent()
            if name not in main_io.get(field_name):
                if field_name == "acquisition":
                    main_io.add_acquisition(data)
                elif field_name == "processing":
                    main_io.add_processing_module(data)
                elif field_name == "analysis":
                    main_io.add_analysis(data)
                elif field_name == "intervals":
                    main_io.add_interval(data)
                else:
                    raise ValueError("Attribute not found")
    return main_io


def combine_nwb_file(main_nwb_fp: Path, sub_nwb_fp: Path, scratch_fp: Path) -> Path:
    """Combine two NWB files and save to scratch directory

    Parameters
    ----------
    main_nwb_fp : Path
        path to the main NWB file
    sub_nwb_fp : Path
        path to the sub NWB file
    scratch_fp : Path
        path to the scratch directory

    Returns
    -------
    Path
        path to the combined NWB file
    """
    main_io = determine_io(main_nwb_fp)
    sub_io = determine_io(sub_nwb_fp)
    with main_io(main_nwb_fp, "r") as io:
        main_nwb = io.read()
        with sub_io(sub_nwb_fp, "r") as read_io:
            sub_nwb = read_io.read()
            main_nwb = add_nwb_attribute(main_nwb, sub_nwb)
        with NWBZarrIO(scratch_fp, "w") as io:
            io.export(src_io=main_nwb, write_args=dict(link_data=False))
    return scratch_fp


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
        "--input-dir", type=str, help="Input directory, default = /data", default="/data/"
    )
    argparser.add_argument(
        "--output-dir",
        type=str,
        help="Output directory, default = /results",
        default="/results/",
    )
    argparser.add_argument(
        "--scratch-dir",
        type=str,
        help="Scratch directory, default = /scratch",
        default="/scratch/",
    )
    # Not doing anything with this yet but will in the future
    argparser.add_argument(
        "--output-format", type=str, help="Output format, default = Zarr", default="Zarr"
    )
    return argparser.parse_args()


def run():
    """basic run function"""
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    scratch_dir = Path(args.scratch_dir)
    ophys_fp = next(input_dir.glob("ophys/*.nwb"))
    behavior_fp = next(input_dir.glob("behavior/*.nwb"))
    eye_fp = next(input_dir.glob("eye_tracking/*.nwb"))
    scratch_fp = scratch_dir / "scratch"

    logging.info(
        "Combining NWB files, {}, {} and {}".format(ophys_fp, behavior_fp, eye_fp)
    )
    for idx, nwb_fp in enumerate([behavior_fp, eye_fp]):
        if idx == 0:
            output_fp = combine_nwb_file(ophys_fp, nwb_fp, scratch_fp)
        else:
            output_fp = combine_nwb_file(ophys_fp, nwb_fp, output_fp)
    shutil.move(scratch_fp, output_dir)
    logging.info("Done")


if __name__ == "__main__":
    run()
