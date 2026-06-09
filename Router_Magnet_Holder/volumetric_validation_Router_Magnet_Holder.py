"""
volumetric_validation.py

Download this script from a part folder on GitHub and run it:
    python volumetric_validation.py

Requires:
    pip install numpy-stl requests

Setup (one time only):
    Mac/Linux: export GITHUB_TOKEN="your_token_here"
    Windows:   setx GITHUB_TOKEN "your_token_here"
"""

import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path

import numpy as np
import requests
from stl import mesh


# Log file named after the script: volumetric_validation_PartName.log

# URLs injected automatically by distribute_validation_script.py
OUTPUT_URL = "https://raw.githubusercontent.com/sft-01/CNC-MACHINE-V5/main/Router_Magnet_Holder/Router_Magnet_Holder.stl"
SOURCE_URL = "https://raw.githubusercontent.com/sft-01/CNC-MACHINE-V5/main/Router_Magnet_Holder/source_Router_Magnet_Holder.stl"


# ── Logging setup ─────────────────────────────────────────────────────────────

def setup_logging(folder: Path, log_file: str):
    log = logging.getLogger("vol_validation")
    log.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")
    fh = logging.FileHandler(folder / log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(fmt)
    log.addHandler(fh)
    log.addHandler(ch)
    return log


# ── Volume calculation ────────────────────────────────────────────────────────

def signed_volume_of_triangle(v0, v1, v2):
    return np.dot(v0, np.cross(v1, v2)) / 6.0


def compute_volume_from_file(stl_path: str) -> float:
    m = mesh.Mesh.from_file(stl_path)
    total = 0.0
    for triangle in m.vectors:
        total += signed_volume_of_triangle(triangle[0], triangle[1], triangle[2])
    return abs(total)


# ── GitHub download ───────────────────────────────────────────────────────────

def download_stl(url: str, token: str, log, save_to: Path = None) -> str | None:
    log.debug(f"Downloading: {url}")
    headers = {"Authorization": f"token {token}"}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            save_path = save_to if save_to else Path(tempfile.mktemp(suffix=".stl"))
            save_path.write_bytes(response.content)
            log.debug(f"Downloaded OK — {len(response.content)} bytes → {save_path.name}")
            return str(save_path)
        else:
            log.error(f"HTTP {response.status_code} — {url}")
            return None
    except Exception as e:
        log.error(f"Download failed: {e}")
        return None


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    folder = Path(__file__).parent.resolve()
    log_file = Path(__file__).stem + ".log"
    log    = setup_logging(folder, log_file)

    log.info("=" * 60)
    log.info(f"volumetric_validation.py started — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # PAT check
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        log.error("GITHUB_TOKEN environment variable not set.")
        log.error("  Mac/Linux: export GITHUB_TOKEN='your_token_here'")
        log.error("  Windows:   setx GITHUB_TOKEN 'your_token_here'")
        return

    log.info(f"Output URL : {OUTPUT_URL}")
    log.info(f"Source URL : {SOURCE_URL}")

    # Save STLs to same folder as the script
    output_filename = OUTPUT_URL.split("/")[-1].replace("%20", " ")
    source_filename = SOURCE_URL.split("/")[-1].replace("%20", " ")
    output_local    = folder / output_filename
    source_local    = folder / source_filename

    output_tmp = download_stl(OUTPUT_URL, token, log, save_to=output_local)
    source_tmp = download_stl(SOURCE_URL, token, log, save_to=source_local)

    if not output_tmp or not source_tmp:
        log.error("Could not download one or both STL files. Aborting.")
        return

    try:
        vol_output = compute_volume_from_file(str(output_local))
        vol_source = compute_volume_from_file(str(source_local))

        abs_diff = abs(vol_output - vol_source)
        pct_diff = (abs_diff / vol_source * 100) if vol_source != 0 else float("inf")

        log.info(f"Source volume : {vol_source:.2f} mm³")
        log.info(f"Output volume : {vol_output:.2f} mm³")
        log.info(f"Difference    : {abs_diff:.2f} mm³  ({pct_diff:.2f}%)")

    except Exception as e:
        log.error(f"Failed to compute volume: {e}")

    log.info("=" * 60)
    log.info(f"Log saved to: {folder / log_file}")


if __name__ == "__main__":
    main()
