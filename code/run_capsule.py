"""top level run script"""

import logging
import shutil
from pathlib import Path

from aind_nwb_utils.utils import combine_nwb_file
from hdmf_zarr import NWBZarrIO
from pydantic_settings import BaseSettings
from pynwb import NWBHDF5IO



class NWBCombineSettings(
    BaseSettings, cli_parse_args=True, cli_ignore_unknown_args=True
):
    """Settings for NWBCombine"""

    input_dir: str = "/data"
    output_dir: str = "/results"
    output_format: str = "zarr"


def run():
    """basic run function"""
    combine_settings = NWBCombineSettings()
    input_dir = Path(combine_settings.input_dir)
    output_dir = Path(combine_settings.output_dir)
    ophys_fp = next(input_dir.glob("ophys/*.nwb"))
    behavior_fp = next(input_dir.glob("behavior/*.nwb"))
    eye_fp = next(input_dir.glob("eye_tracking/*.nwb"))
    save_io = NWBZarrIO
    if combine_settings.output_format.lower() == "hdf5":
        save_io = NWBHDF5IO

    logging.info(
        "Combining NWB files, %s, %s and %s", ophys_fp, behavior_fp, eye_fp)
    for idx, nwb_fp in enumerate([behavior_fp, eye_fp]):
        if idx == 0:
            output_fp = combine_nwb_file(ophys_fp, nwb_fp, save_io)
        else:
            output_fp = combine_nwb_file(output_fp, nwb_fp, save_io)

    shutil.move(output_fp, output_dir / "session.nwb")
    logging.info("Done")


if __name__ == "__main__":
    run()
