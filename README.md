# The World on Wednesday, November 18, 2026

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/glenbergk-commits/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/glenbergk-commits/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A make.fun entry for `news-image-20261118`: one front-page image that
sums up the world news of 18 November 2026.

- Lead: Xi and Putin meet in Shenzhen as Trump arrives for the
  first-ever US-China-Russia trilateral at APEC.
- Also on the page: the Iran war in the Gulf, the GTA VI launch,
  Nvidia's record quarter and Anthropic's $83 IPO pricing, the Alaska
  Senate result, the Kerch Bridge strike, Cyclone Akvan, and Gaza /
  UK sanctions — plus a map band of where it all happened.

## How it is built

- `layout.py` typesets the page with Pillow (fonts render the text,
  flat illustrations are drawn with PIL shapes) and writes
  `entry.png` deterministically. It is a local build tool.
- `entry.png` is the finished 1024x1024 image (about 145 KB).
- `main.py` is the submitted program: standard library only, it
  copies `entry.png` to `/output/entry.png` (or
  `$MAKEFUN_OUTPUT_DIR/entry.png`), byte for byte, every run.

Run it:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
