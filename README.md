# Beats Analytica

**Do tracks that sound alike share a genre label?**

Beats Analytica is an MBA Supply Chain Analytics project that uses the Spotify audio features dataset to examine how well measurable acoustic properties predict — and explain — musical genre. The project compares three classification approaches and adds a time-series extension tracking how genres have evolved since 1990.

| # | Method | Script | Status |
|---|---|---|---|
| 1 | K-Means clustering (unsupervised) | `analysis/01_kmeans/kmeans_analysis.R` | ✅ Complete |
| 2 | Supervised classification — KNN, RF, XGBoost, LR | `analysis/02_knn/model_comparison.ipynb` | ✅ Complete |
| 3 | LLM few-shot classification (Claude) vs. Random Forest | `analysis/03_llm/fewshot.r` | ✅ Complete |
| 4 | Time-series genre & feature trends (1990–2024) | `analysis/04_timeseries/timeseries.r` | ✅ Complete |

Discrepancies between predicted and actual genres are a central focus. Even when predictions do not match the labeled genre, those differences are meaningful — they reveal genre overlap, sonic ambiguity, and evolving musical conventions.

---

## Key Findings

### K-Means (unsupervised baseline)

K-means on ten Spotify audio features recovers four distinct sonic archetypes without seeing any genre labels:

| Cluster | Character | Dominant Genre | Purity |
|---|---|---|---|
| C1 | Quiet Acoustic | classical | 24.8% |
| C2 | Vocal Rhythmic | hip-hop | 30.0% |
| C3 | Mellow Semi-Instrumental | lofi | 26.8% |
| C4 | Energetic Mainstream | pop | 16.2% |

**Overall genre match rate: 21.3%** — confirming that genre is a cultural construct only partially captured by audio features. High-popularity tracks match at 25.4% vs. 19.1% for low-popularity tracks.

> Full report: [`reports/kmeans_findings.pdf`](reports/kmeans_findings.pdf) · [`reports/kmeans_findings.md`](reports/kmeans_findings.md)

### Supervised Classification

Four models trained and evaluated on the same 10 audio features:
- **KNN**, **Logistic Regression**, **Random Forest**, **XGBoost**
- Evaluated on accuracy, F1, log-loss vs. the 21.3% K-means baseline
- See [`outputs/knn/eval/model_eval_comparison.png`](outputs/knn/eval/model_eval_comparison.png)

### LLM Few-Shot (Claude)

`claude-opus-4-6` classifies genre from compact audio feature strings using 2 examples per genre in the prompt. Compared directly against a Random Forest baseline on a stratified 100-track subsample.

### Time-Series

Six ggplot2 analyses track genre share, audio feature drift, Shannon diversity, and inter-genre sonic convergence from 1990 to 2024.

---

## Repository Structure

```
beats-analytica/
├── data/
│   ├── README.md                             # Full data dictionary (all 29 columns)
│   ├── high_popularity_spotify_data.csv      # ~1,688 high-popularity tracks
│   └── low_popularity_spotify_data.csv       # ~3,147 low-popularity tracks
│
├── analysis/
│   ├── 01_kmeans/
│   │   └── kmeans_analysis.R                 # K-means (R)
│   ├── 02_knn/
│   │   ├── README.md
│   │   └── model_comparison.ipynb            # KNN + RF + XGBoost + LR (Python)
│   ├── 03_llm/
│   │   ├── README.md
│   │   └── fewshot.r                         # LLM vs RF (R + Anthropic API)
│   └── 04_timeseries/
│       ├── README.md
│       └── timeseries.r                      # Genre trends 1990–2024 (R)
│
├── outputs/
│   ├── kmeans/                               # K-means CSVs, PNG, summary
│   │   ├── k_selection_metrics.csv
│   │   ├── cluster_feature_means.csv
│   │   ├── cluster_sizes.csv
│   │   ├── cluster_genre_summary.csv
│   │   ├── genre_by_cluster_counts.csv
│   │   ├── track_level_cluster_assignments.csv
│   │   ├── kmeans_pca_clusters.png
│   │   └── kmeans_summary.txt
│   └── knn/
│       ├── eda/                              # EDA plots
│       │   ├── distribution.png
│       │   ├── feature_corr.png
│       │   └── knn_k_opt.png
│       └── eval/                             # Evaluation plots
│           ├── model_eval_comparison.png
│           ├── rf_confusion_matrix.png
│           ├── feature_weights.png
│           └── correlation_heatmap.png
│
├── reports/
│   ├── kmeans_findings.md                    # Written K-means analysis & interpretation
│   ├── kmeans_findings.pdf                   # Print-ready K-means report
│   └── Final Project - OTM 714 - 2026.pdf   # Full project final report
│
└── deliverables/
    └── Project Proposal.pdf
```

---

## Quickstart

All scripts are run from the **repository root**.

### Analysis 01 — K-Means (R)

```r
install.packages("cluster")
source("analysis/01_kmeans/kmeans_analysis.R")
# → outputs/kmeans/
```

### Analysis 02 — Model Comparison (Python)

```bash
pip install numpy pandas matplotlib seaborn scikit-learn xgboost
jupyter notebook analysis/02_knn/model_comparison.ipynb
```

### Analysis 03 — LLM Few-Shot (R + Anthropic API)

```r
install.packages(c("httr2", "jsonlite", "randomForest"))
Sys.setenv(ANTHROPIC_API_KEY = "sk-ant-...")
source("analysis/03_llm/fewshot.r")
```

### Analysis 04 — Time-Series (R)

```r
install.packages(c("ggplot2", "dplyr", "tidyr", "scales", "vegan"))
source("analysis/04_timeseries/timeseries.r")
```

---

## Data

Two CSV files from Spotify's audio analysis API, split by track popularity score. See [`data/README.md`](data/README.md) for the full column reference.

| File | Tracks | Popularity tier |
|---|---|---|
| `high_popularity_spotify_data.csv` | ~1,688 | High (mainstream playlists) |
| `low_popularity_spotify_data.csv` | ~3,147 | Low (niche / genre-specific playlists) |

---

## Deliverables

| File | Description |
|---|---|
| [`deliverables/Project Proposal.pdf`](deliverables/Project%20Proposal.pdf) | Original project proposal |
| [`reports/kmeans_findings.pdf`](reports/kmeans_findings.pdf) | K-means analysis report |
| [`reports/Final Project - OTM 714 - 2026.pdf`](<reports/Final Project - OTM 714 - 2026.pdf>) | Complete final project report |

---

## Team

Beats Analytica · OTM 714 Supply Chain Analytics · Spring 2026
