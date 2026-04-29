# Beats Analytica

**Do tracks that sound alike share a genre label?**

Beats Analytica is an MBA Supply Chain Analytics project that uses the Spotify audio features dataset to examine how well measurable acoustic properties predict — and explain — musical genre. The project compares three approaches:

| # | Method | Status |
|---|---|---|
| 1 | K-Means clustering (unsupervised) | ✅ Complete |
| 2 | K-Nearest Neighbors classification (supervised) | 🔲 In progress |
| 3 | LLM few-shot classification | 🔲 In progress |

Discrepancies between predicted and actual genres are a central focus. Even when predictions do not match the labeled genre, those differences are meaningful — they reveal genre overlap, sonic ambiguity, and evolving musical conventions.

---

## Key Finding (K-Means)

K-means on ten Spotify audio features recovers four distinct sonic archetypes:

| Cluster | Character | Dominant Genre | Match Rate |
|---|---|---|---|
| C1 | Quiet Acoustic | classical | 24.8% |
| C2 | Vocal Rhythmic | hip-hop | 30.0% |
| C3 | Mellow Semi-Instrumental | lofi | 26.8% |
| C4 | Energetic Mainstream | pop | 16.2% |

**Overall genre match rate: 21.3%** — confirming that genre is a cultural construct only partially captured by audio features. High-popularity tracks match 25.4% vs. 19.1% for low-popularity tracks, reflecting that mainstream genres have stronger audio-cultural alignment than niche or culturally specific genres.

> Full findings: [`reports/kmeans_findings.md`](reports/kmeans_findings.md) · [`reports/kmeans_findings.pdf`](reports/kmeans_findings.pdf)

---

## Repository Structure

```
beats-analytica/
├── data/
│   ├── README.md                        # Data dictionary & variable descriptions
│   ├── high_popularity_spotify_data.csv # 1,688 high-popularity tracks
│   └── low_popularity_spotify_data.csv  # 3,147 low-popularity tracks
│
├── analysis/
│   ├── 01_kmeans/
│   │   └── kmeans_analysis.R            # K-means clustering (complete)
│   ├── 02_knn/
│   │   └── README.md                    # KNN analysis (in progress)
│   └── 03_llm/
│       └── README.md                    # LLM few-shot analysis (in progress)
│
├── outputs/
│   └── kmeans/                          # All K-means model outputs
│       ├── k_selection_metrics.csv
│       ├── cluster_feature_means.csv
│       ├── cluster_sizes.csv
│       ├── cluster_genre_summary.csv
│       ├── genre_by_cluster_counts.csv
│       ├── track_level_cluster_assignments.csv
│       ├── kmeans_pca_clusters.png
│       └── kmeans_summary.txt
│
├── reports/
│   ├── kmeans_findings.md               # Full written analysis & interpretation
│   ├── kmeans_findings.html             # Styled HTML version
│   └── kmeans_findings.pdf             # Print-ready PDF
│
└── deliverables/
    └── Project Proposal.pdf
```

---

## Quickstart

All analysis scripts are designed to be run from the **repository root**.

### Prerequisites

```r
install.packages("cluster")   # only dependency — base R handles everything else
```

### Run K-Means Analysis

```r
source("analysis/01_kmeans/kmeans_analysis.R")
```

Outputs are written to `outputs/kmeans/`. The script is fully reproducible — `set.seed(123)` is set at the top.

---

## Data

Two CSV files sourced from Spotify's audio analysis API, split by track popularity score:

| File | Tracks | Popularity range |
|---|---|---|
| `high_popularity_spotify_data.csv` | ~1,688 | High (mainstream playlists) |
| `low_popularity_spotify_data.csv` | ~3,147 | Low (niche / genre-specific playlists) |

Both files share 29 common columns including `playlist_genre`, `playlist_subgenre`, and ten audio feature columns. See [`data/README.md`](data/README.md) for the full data dictionary.

---

## Methods Overview

### 1 · K-Means Clustering (`analysis/01_kmeans/`)

- **Features:** 10 Spotify audio features, z-score scaled
- **k selection:** WSS elbow + average silhouette (k = 2–8 evaluated)
- **Selected k:** 4
- **Evaluation:** Cluster-to-genre majority label match rate + silhouette scores
- **Key result:** 21.3% overall genre match; high-popularity tracks match at 25.4% vs. 19.1% for low-popularity

### 2 · K-Nearest Neighbors (`analysis/02_knn/`)

Supervised genre classification using the same ten audio features. Will use cross-validated tuning of k and will be benchmarked directly against the 21.3% K-means baseline.

### 3 · LLM Few-Shot Classification (`analysis/03_llm/`)

Audio features for each track (formatted as structured text) will be passed to a large language model with genre examples in the prompt. The LLM's genre prediction will be compared to both the Spotify label and the K-means/KNN predictions to test whether world knowledge about genre conventions improves classification.

---

## Deliverables

| File | Description |
|---|---|
| [`deliverables/Project Proposal.pdf`](deliverables/Project%20Proposal.pdf) | Original project proposal |
| [`reports/kmeans_findings.pdf`](reports/kmeans_findings.pdf) | K-means analysis report |

---

## Team

Beats Analytica · MBA Supply Chain Analytics · Spring 2026
