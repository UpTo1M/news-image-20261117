# World News — Tuesday, 17 November 2026

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/UpTo1M/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/UpTo1M/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

A newspaper front page summing up the world's news of Tuesday, 17 November 2026 in one image.

## What it is

`entry.png` is a 1024x1024 front page — masthead "WORLD NEWS" with the date
"TUESDAY, 17 NOVEMBER 2026", and six story blocks covering the day's news:
Iran's drone strike on a U.S. radar site in Bahrain, Ukraine hitting the
Kerch Bridge, Trump's Asia trip, Estonia closing its Russia border, Japan
scrambling jets, and the Houthi advance in Yemen.

## How it works

- `draw.py` draws the front page with Pillow and saves it as `entry.png`.
- `main.py` (standard library only, no network) copies `entry.png` to the
  output directory (`MAKEFUN_OUTPUT_DIR`, default `/output`).

Run it:

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Both runs write the same bytes.
