"""top level run script"""

import argparse
import datetime
import logging
import shutil
from pathlib import Path
from typing import Union

import pynwb
from hdmf_zarr import NWBZarrIO
from pynwb import NWBHDF5IO
import tempfile
import os
import atexit

# From multiple input NWB files, in the future, I need to figure out a wayu to detrermine which nwb is which. For now, only the ophys nwb has the processing file so if it exists, I will assume that it is the primary nwb
# # append ancillary data to the acquisition nwb
# Export appended nwb to the results folder


def create_temp_nwb(save_strategy=Union[NWBHDF5IO, NWBZarrIO]) -> str:
    """Create a temporary file and return the path

    Parameters
    ----------
    save_strategy : Union[NWBHDF5IO, NWBZarrIO]
        to determine if a temp file or directory should be created
    Returns
    -------
    str
        the path to the temporary file
    """
    if isinstance(save_strategy, NWBZarrIO):
        temp = tempfile.TemporaryDirectory(delete=False)
        temp_path = temp.name
    else:
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".nwb")
        temp_path = temp.name
    temp.close()

    # Register cleanup function to run at program exit
    atexit.register(os.unlink, temp_path)

    return temp_path


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
    for field_name in sub_io.fields.keys():
        attribute = getattr(sub_io, field_name)
        print(attribute)
        if (
            isinstance(attribute, str)
            or isinstance(attribute, datetime.datetime)
            or isinstance(attribute, list)
            or isinstance(attribute, pynwb.file.Subject)
        ):
            continue
        for name, data in getattr(sub_io, field_name).items():
            data.reset_parent()
            if name not in getattr(main_io, field_name):
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


def combine_nwb_file(main_nwb_fp: Path, sub_nwb_fp: Path, save_io) -> Path:
    """Combine two NWB files and save to scratch directory

    Parameters
    ----------
    main_nwb_fp : Path
        path to the main NWB file
    sub_nwb_fp : Path
        path to the sub NWB file
    save_io : Union[NWBHDF5IO, NWBZarrIO]
        how to save the nwb
    Returns
    -------
    Path
        the path to the saved nwb
    """
    main_io = determine_io(main_nwb_fp)
    sub_io = determine_io(sub_nwb_fp)
    scratch_fp = create_temp_nwb(save_io)
    with main_io(main_nwb_fp, "r") as main_io:
        main_nwb = main_io.read()
        with sub_io(sub_nwb_fp, "r") as read_io:
            sub_nwb = read_io.read()
            main_nwb = add_nwb_attribute(main_nwb, sub_nwb)
            with save_io(scratch_fp, "w") as io:
                io.export(src_io=main_io, write_args=dict(link_data=False))
    return scratch_fp


def determine_io(nwb_path: Path) -> Union[NWBHDF5IO, NWBZarrIO]:
    """determine the io type

    Returns
    -------
    Union[NWBHDF5IO, NWBZarrIO]
        the appropriate io object
    """
    if nwb_path.is_dir():
        return NWBZarrIO
    return NWBHDF5IO


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
        "--output-format",
        type=str,
        help="Output format hdf5 or zarr, default = zarr",
        default="zarr",
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
    save_io = NWBZarrIO
    if args.output_format.lower() == "hdf5":
        save_io = NWBHDF5IO

    logging.info(
        "Combining NWB files, {}, {} and {}".format(ophys_fp, behavior_fp, eye_fp)
    )
    for idx, nwb_fp in enumerate([behavior_fp, eye_fp]):
        if idx == 0:
            output_fp = combine_nwb_file(ophys_fp, nwb_fp, save_io)
        else:
            output_fp = combine_nwb_file(output_fp, nwb_fp, save_io)

    shutil.move(output_fp, output_dir / "session.nwb")
    logging.info("Done")


if __name__ == "__main__":
    run()
