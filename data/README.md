# Data

## Source

U.S. EPA Air Quality System (AQS), daily summary files for PM2.5 FRM/FEM mass (parameter 88101), `daily_88101_YYYY.zip` from the [EPA AirData pre-generated files](https://aqs.epa.gov/aqsweb/airdata/download_files.html), 2015 through 2024. AQS data are produced by a federal agency and are in the public domain, so the processed file is republished on this repository's `data` release.

## File

`dc_pm25_daily.csv`, on the `data` release. One row per calendar day.

| Column | Meaning |
|---|---|
| `date` | Local calendar date, `YYYY-MM-DD` |
| `pm25` | Mean of the District of Columbia monitors' 24-hour mean PM2.5, µg/m³ |
| `n_sites` | Number of DC monitoring sites that reported that day |

SHA-256 of `dc_pm25_daily.csv`:

```
SHA256: dc43845209b3b8fa9c8c951e5e73595b9c786c17999473655184e7af6f3f1c4a
```

The notebook reads this line and refuses to run if the file does not match.

## Unit of observation, sample size, and time span

The unit is one calendar day in the District of Columbia, 1 January 2015 to 31 December 2024, about 3,650 days. Each day averages every DC monitor (state code 11) that reported at least 75% of the day. Days flagged as exceptional events (wildfire smoke, fireworks) keep the readings with the event included, because the athletes breathe that air.

## Rebuild from the source

From the project root:

```bash
python build_data.py
```

The script downloads the ten yearly zips to `data/raw/` (not committed), writes `data/dc_pm25_daily.csv`, and prints its SHA-256. Paste that hash above in the same commit.

## Release

`OWNER/REPO` is `khushisankar-dot/aii600-final-project`.

```bash
gh repo set-default khushisankar-dot/aii600-final-project
gh release create data data/dc_pm25_daily.csv --title "Data" --notes "See data/README.md"
```

When the file changes:

```bash
gh release upload data data/dc_pm25_daily.csv --clobber
```

On another machine:

```bash
gh release download data --dir data
```
