# StackWatch 📡

A little personal dashboard that keeps me updated o — Singapore, China, world politics, US/world headlines, and which
companies are on the rise 

It refreshes itself automatically and lives on a free GitHub Pages link,
so it's just a bookmark away on my phone or laptop.

## The idea

Six tabs, real tab-switching

- 🔥 **Hot News** — most recent stuff across every tab, combined. No extra
  fetching needed, it's just built from the other five.
- 🇸🇬 **Singapore** — local, everyday focus
- 🇨🇳 **China** — tech, policy, Huawei, semiconductors, all folded together
- 🏛️ **Politics** — world politics and geopolitics
- 🇺🇸 **US & World** — US news plus major world headlines
- 🚀 **Rising Companies** — startups and fast-growing companies, any country

A robot (GitHub Actions) checks the news every hour during work hours,
saves it, and the page just displays whatever it found. No servers to
maintain, no bills, nothing to babysit.

## What's actually in each folder

**`index.html`** — the dashboard itself. This is the only file your browser
actually shows you. Everything else exists to feed it data.

**`data/`** — just holds one file, `news.json`. Think of it as the
dashboard's "current state" — whatever's in there right now is what shows
up on the page. It gets overwritten automatically every time the robot runs.

**`scripts/`** — the robot's brain. `fetch_news.py` is the Python script
that goes and asks a news API "what's new on these topics," and writes the
results into `data/news.json`.

**`.github/workflows/`** — the robot's alarm clock. `fetch-news.yml` tells
GitHub "run that Python script once an hour, during work hours, forever."
This is what makes the whole thing "live" without me lifting a finger.

**`README.md`** — this file. Just notes to future-me for when I inevitably
forget how any of this works.


## Tuning it
Currently: 5 tabs (Singapore, China, Politics, US & World, Rising Companies —
Hot News is free, it's just a combined view of the other five), 9 total
search queries per run, checked once an hour during 9am–6pm Singapore time
(10 runs/day). That's 9 × 10 = 90 requests/day, just under NewsAPI's free
100/day cap.
