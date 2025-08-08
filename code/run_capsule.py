"""top level run script"""

import logging
import shutil
from pathlib import Path

from aind_nwb_utils.utils import combine_nwb_file
from hdmf_zarr import NWBZarrIO
from pynwb import NWBHDF5IO
from hdmf_zarr import NWBZarrIO
from pathlib import Path
import numpy as np
import argparse


data_folder = Path("../data/")
scratch_folder = Path("../scratch/")
results_folder = Path("../results/")



def run():
    """basic run function"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", type=str, default=f'.')
    parser.add_argument("--output_dir", type=str, default=f'.')
    parser.add_argument("--output_format", type=str, default=f'hdf5')

    args = parser.parse_args()

    save_io = NWBZarrIO
    if args.output_format.lower() == "hdf5":
        save_io = NWBHDF5IO

    input_dir = data_folder / args.input_dir
    output_dir = results_folder / args.output_dir

    combine_nwbs = [f for f in input_dir.rglob("*.nwb*") if f.name.endswith(".nwb") or f.name.endswith(".nwb.zarr")]

    primary_nwb = None
    for nwb_path in combine_nwbs:
        if 'nwb_primary' in str(nwb_path):
            combine_nwbs.remove(nwb_path)
            primary_nwb = nwb_path
            break
    assert primary_nwb is not None, "Didn't find a primary NWB to combine with"
    logging.info(f"Using primary NWB: {primary_nwb}")

    assert len(combine_nwbs) >= 1, "Didn't find any non-primary NWBs to combine"
    logging.info(f"Using combine NWBs: {combine_nwbs}")

    output_nwb = primary_nwb
    for combine_nwb in combine_nwbs:
        logging.info("Combining NWB files; {output_nwb}, and {combine_nwb}")
        output_nwb = combine_nwb_file(output_nwb, combine_nwb, "/scratch", save_io)

    shutil.move(output_nwb, output_dir / primary_nwb.name)
    logging.info("Done")


if __name__ == "__main__":
    run()
