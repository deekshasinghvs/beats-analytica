# Analysis 04 · Time-Series Genre & Feature Trends

> **Status: Complete** — `timeseries.r`

## Objective

Use `track_album_release_date` to track how genre composition and audio feature profiles have changed from 1990 to 2024 — and whether genres are sonically converging or diverging over time.

## Script

`analysis/04_timeseries/timeseries.r` — R script using ggplot2 + dplyr.

## Setup

```r
install.packages(c("ggplot2", "dplyr", "tidyr", "scales", "vegan"))
source("analysis/04_timeseries/timeseries.r")
```

Run from the **repository root**.

## Analyses & Plots

The script produces six ggplot2 plots and a console numeric summary.

| Plot | Description |
|---|---|
| **Plot 1** — Genre share over time | Proportional stacked area chart; separates real shifts from catalogue growth |
| **Plot 2** — Track count per genre | Absolute counts; makes the post-2018 streaming surge visible |
| **Plot 3** — Shannon diversity index | H′ = −Σ pᵢ ln(pᵢ) per year; rising = more even genre mix |
| **Plot 4** — Audio features over time | Yearly means for energy, danceability, valence, acousticness, speechiness, instrumentalness (all genres combined); LOESS smoothed |
| **Plot 5** — Features per genre | Energy, valence, danceability faceted by top-6 genres; reveals genre-specific vs. universal trends |
| **Plot 6** — Genre convergence | Mean pairwise Euclidean distance between genre centroids in normalised 6-dimensional feature space over time; ±1 SD ribbon + linear trend |

## Console Summary

| Output | Description |
|---|---|
| Top-3 genres at key epochs | Dominant genres in 1995, 2000, 2005, 2010, 2015, 2020, 2024 |
| Feature slopes per decade | Linear rate of change per audio feature 1990–2024 |
| Shannon diversity slope | Linear trend in genre evenness (p-value reported) |
| Convergence direction | Whether genres are sonically converging or diverging (slope + p-value) |

## Key Design Decisions

- **Year range:** 1990–2024 (`YEAR_START = 1990`); pre-1990 data is too sparse for reliable yearly genre averages
- **Min genre sample:** ≥ 30 tracks total; ≥ 5 tracks per genre-year for feature plots; ≥ 10 for convergence centroids
- **Global normalisation for distances:** features scaled to [0, 1] globally so loudness (in dB) does not dominate Euclidean distances
- **Shannon entropy vs. genre count:** entropy weights by proportion, penalising years where one genre dominates
- **LOESS span:** 0.4–0.6 depending on plot; noted in code and adjustable
