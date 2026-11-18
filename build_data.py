"""Build data/dc_pm25_daily.csv from the EPA AQS daily PM2.5 files.

Downloads daily_88101_YYYY.zip for 2015-2024 from the EPA AirData site,
keeps the District of Columbia monitors (state code 11), and writes one
row per day: the mean of the DC monitors' 24-hour mean PM2.5 (µg/m³).

    python build_data.py

The zips go to data/raw/ (about 10 MB each, not committed) and are reused
if they are already there. The script prints the SHA-256 of the output,
which goes in data/README.md.
"""

import hashlib
import io
import subprocess
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

YEARS = range(2015, 2025)
URL = "https://aqs.epa.gov/aqsweb/airdata/daily_88101_{year}.zip"
STATE_CODE = "11"  # District of Columbia
MIN_OBS_PERCENT = 75  # drop monitor-days with less than 18 of 24 hours

DATA = Path("data")
RAW = DATA / "raw"
OUT = DATA / "dc_pm25_daily.csv"


def fetch(year):
    """Return the bytes of one year's zip, downloading it once."""
    RAW.mkdir(parents=True, exist_ok=True)
    path = RAW / f"daily_88101_{year}.zip"
    if not path.exists():
        print(f"Downloading {year} ...", flush=True)
        try:
            urllib.request.urlretrieve(URL.format(year=year), path)
        except urllib.error.URLError:
            # Python from python.org on a Mac can lack SSL certificates; curl has them.
            subprocess.run(["curl", "-fsSL", "-o", str(path), URL.format(year=year)], check=True)
    return path.read_bytes()


def read_year(year):
    """Rows for the DC monitors from one year's file."""
    with zipfile.ZipFile(io.BytesIO(fetch(year))) as z:
        name = z.namelist()[0]
        df = pd.read_csv(z.open(name), dtype={"State Code": str}, low_memory=False)
    df = df[df["State Code"].str.zfill(2) == STATE_CODE]
    return df


def build():
    raw = pd.concat([read_year(y) for y in YEARS], ignore_index=True)

    # Wildfire smoke and fireworks are flagged as exceptional events. AQS
    # repeats those days once with the event and once without it. Keep the
    # air people actually breathed: drop the "Excluded" copies.
    raw = raw[raw["Event Type"] != "Excluded"]
    raw = raw[raw["Observation Percent"] >= MIN_OBS_PERCENT]

    # One reading per monitor (site and POC) per day. The same reading is
    # repeated once per pollutant standard, so drop those repeats.
    raw["site"] = (raw["State Code"].str.zfill(2) + "-"
                   + raw["County Code"].astype(str).str.zfill(3) + "-"
                   + raw["Site Num"].astype(str).str.zfill(4))
    raw = raw.drop_duplicates(["site", "POC", "Date Local", "Sample Duration"])
    monitor_day = (raw.groupby(["Date Local", "site", "POC"])["Arithmetic Mean"]
                   .mean().reset_index())

    # Average the instruments at a site, then the sites, for one DC value per day.
    site_day = (monitor_day.groupby(["Date Local", "site"])["Arithmetic Mean"]
                .mean().reset_index())
    daily = (site_day.groupby("Date Local")
             .agg(pm25=("Arithmetic Mean", "mean"), n_sites=("site", "nunique"))
             .reset_index()
             .rename(columns={"Date Local": "date"}))
    daily["pm25"] = daily["pm25"].round(2)
    daily = daily.sort_values("date")

    DATA.mkdir(exist_ok=True)
    daily.to_csv(OUT, index=False, lineterminator="\n")
    sha = hashlib.sha256(OUT.read_bytes()).hexdigest()
    print(f"Wrote {OUT}: {len(daily)} days, {daily['date'].min()} to {daily['date'].max()}")
    print(f"SHA-256 {sha}")


if __name__ == "__main__":
    build()
