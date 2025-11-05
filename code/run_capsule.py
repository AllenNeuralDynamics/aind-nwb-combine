"""top level run script"""

from datetime import datetime as dt
import json
import logging
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
    """
    Runs NWB combine process
    1. Locate primary NWB file in nwb_primary directory
    2. Locate secondary NWB files in nwb_secondary, etc.
    3. Combine primary with each secondary in order
    4. Save combined NWB file in output directory
    5. Output format can be zarr or hdf5
    """
    combine_settings = NWBCombineSettings()
    input_dir = Path(combine_settings.input_dir)
    output_dir = Path(combine_settings.output_dir)

    # Locate primary NWB file
    nwb_primary = next((input_dir / "nwb_primary").rglob("*.nwb"))
    save_io = NWBZarrIO
    if combine_settings.output_format.lower() == "hdf5":
        save_io = NWBHDF5IO

    secondary_dirs = sorted(input_dir.glob("nwb_secondary*"))
    nwb_secondaries = []
    for sec_dir in secondary_dirs:
        try:
            nwb_fp = next(sec_dir.rglob("*.nwb"))
            nwb_secondaries.append(nwb_fp)
        except StopIteration:
            logging.warning("No NWB file found in %s", sec_dir)

    logging.info("Primary NWB: %s", nwb_primary)
    logging.info("Secondary NWB files: %s", nwb_secondaries)

    output_fp = nwb_primary
    for idx, secondary_fp in enumerate(nwb_secondaries, start=1):
        logging.info(
            "Combining primary with %s (%d/%d)",
            secondary_fp,
            idx,
            len(nwb_secondaries)
        )
        combine_nwb_file(
            output_fp,
            secondary_fp,
            output_dir / "combined.nwb",
            save_io
        )


if __name__ == "__main__":
    run()
