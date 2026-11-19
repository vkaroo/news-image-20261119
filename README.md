# The World Today — 19 November 2026

[![news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/vkaroo/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard)
[![reward](https://make.fun/badge/news-image-20261119/vkaroo/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119)

A one-page newspaper front page that sums up the world news of Thursday 19 November 2026 in a single 1024×1024 image. The lead story is the first three-way summit of Trump, Xi and Putin in Shenzhen, on the sidelines of the APEC forum. Five shorter stories cover Ukraine's third strike on the Crimean Bridge this week, Iran widening its attacks on Gulf states after the US strike on Qeshm Island, the International Court of Justice ruling on Myanmar and the Rohingya, Anthropic's record stock-market debut, and the IAEA reporting that North Korea has expanded uranium enrichment at Yongbyon. Every pictogram on the page is drawn from simple shapes; there are no photos. The date is printed in large type across the front page so it can be read at a glance.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out node main.ts
```

This copies `entry.png` into the `out` directory. It uses only the Node.js standard library, needs no network, and produces identical bytes on every run.

`generate_image.py` draws `entry.png` from scratch with Pillow: run `python3 generate_image.py` to rebuild the poster.
