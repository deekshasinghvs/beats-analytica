# Analysis 02 · K-Nearest Neighbors Classification

> **Status: In progress**

## Objective

Use K-Nearest Neighbors (KNN) to predict a track's `playlist_genre` from its ten Spotify audio features, then compare classification accuracy against the K-means unsupervised baseline (21.3% majority-label match rate).

## Planned Approach

### Features

Same ten audio features used in the K-means analysis, z-score scaled:

```
danceability, energy, tempo, valence, acousticness,
instrumentalness, speechiness, liveness, loudness, duration_ms
```

### Methodology

1. **Train/test split** — stratified 80/20 split by `playlist_genre` to preserve class proportions across both popularity tiers.
2. **k selection** — cross-validated accuracy over k = 1, 3, 5, 7, 10, 15, 20 using 5-fold CV on the training set.
3. **Evaluation metrics**
   - Overall accuracy
   - Per-genre precision, recall, F1
   - Confusion matrix
   - Comparison to K-means 21.3% baseline
4. **Popularity tier split** — accuracy reported separately for high-popularity and low-popularity tracks, mirroring the K-means popularity analysis.

### Expected output files (`outputs/knn/`)

| File | Contents |
|---|---|
| `knn_cv_accuracy.csv` | Cross-validated accuracy by k |
| `knn_confusion_matrix.csv` | Full genre × predicted-genre confusion matrix |
| `knn_per_genre_metrics.csv` | Precision, recall, F1 per genre |
| `knn_track_predictions.csv` | Per-track predicted genre and match flag |
| `knn_summary.txt` | Console summary of all key metrics |

## Research Questions

- Does supervised learning substantially outperform the 21.3% unsupervised baseline?
- Which genres benefit most from labeled training examples?
- Do genres that cluster cleanly in K-means also classify cleanly in KNN?
- Is the popularity-tier gap (25.4% vs. 19.1%) preserved or reduced under supervised learning?

## Script

`analysis/02_knn/knn_analysis.R` — to be created.
