# Analysis 02 · Supervised Classification (KNN + Model Comparison)

> **Status: Complete** — `model_comparison.ipynb`

## Objective

Predict a track's `playlist_genre` from its Spotify audio features using supervised classifiers and compare accuracy against the K-means unsupervised baseline (21.3% majority-label match rate).

## Script

`analysis/02_knn/model_comparison.ipynb` — Python notebook (scikit-learn + XGBoost).

## Models Compared

| Model | Notes |
|---|---|
| K-Nearest Neighbors | Distance-weighted; k tuned via 5-fold stratified CV |
| Logistic Regression | Linear baseline |
| Random Forest | 300 trees; feature importances extracted |
| XGBoost | Gradient-boosted trees |

## Methodology

1. **Data** — same high + low popularity CSVs, merged and deduplicated on `track_id`. Genres bucketed into 4 acoustic families for one experiment; full multi-class labels used for the main evaluation.
2. **Features** — 10 audio features, z-score scaled via `StandardScaler`.
3. **Train/test split** — stratified 80/20; `StratifiedKFold(n_splits=5)` for CV.
4. **k selection** — evaluated k ∈ {1, 3, 5, 7, 11, 15, 21, 31, 51, 75, 101} with distance weighting; best k chosen by CV accuracy.
5. **Evaluation** — accuracy, F1, log-loss, confusion matrix, permutation importance.

## Output Plots (`outputs/knn/`)

### EDA (`eda/`)

| File | Description |
|---|---|
| `distribution.png` | Track count by genre (class balance check) |
| `feature_corr.png` | Audio feature correlation matrix |
| `knn_k_opt.png` | CV accuracy vs. k — optimal k selection curve |

### Evaluation (`eval/`)

| File | Description |
|---|---|
| `model_eval_comparison.png` | Accuracy / F1 / log-loss across all four models |
| `rf_confusion_matrix.png` | Random Forest confusion matrix (best performer) |
| `feature_weights.png` | Permutation importance — top features for genre prediction |
| `correlation_heatmap.png` | Feature-to-feature correlation heatmap |

## Dependencies

```bash
pip install numpy pandas matplotlib seaborn scikit-learn xgboost
```

## Key Research Questions Answered

- Does supervised learning outperform the 21.3% K-means baseline? (**Yes — see `model_eval_comparison.png`**)
- Which audio features are most predictive? (**See `feature_weights.png`**)
- Which genres are hardest to classify? (**See `rf_confusion_matrix.png`**)
