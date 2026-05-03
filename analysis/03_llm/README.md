# Analysis 03 · LLM Few-Shot Genre Classification

> **Status: Complete** — `fewshot.r`

## Objective

Pass each track's audio feature values to a large language model using few-shot prompting, obtain a genre prediction, and compare the LLM's accuracy against both the K-means baseline (21.3%) and the KNN classifier.

The core question is whether a model with world knowledge about musical genres can classify tracks more effectively than methods that see only raw numbers.

## Planned Approach

### Prompt Design

Each track is formatted as a structured text block and passed to the LLM with a few labeled examples in the prompt. Example format:

```
You are a music genre classifier. Given a track's Spotify audio features,
predict its genre. Choose from: pop, rock, hip-hop, jazz, classical,
electronic, latin, lofi, ambient, r&b, or other.

Examples:
Track: danceability=0.85, energy=0.72, tempo=128, valence=0.65,
       acousticness=0.05, instrumentalness=0.01, speechiness=0.08
Genre: pop

Track: danceability=0.42, energy=0.09, tempo=98, valence=0.11,
       acousticness=0.94, instrumentalness=0.87, speechiness=0.04
Genre: classical

---
Track: danceability={x}, energy={x}, tempo={x}, valence={x},
       acousticness={x}, instrumentalness={x}, speechiness={x}
Genre:
```

### Few-Shot Configuration

- **Number of examples:** 3–5 per prompt (one per broad genre archetype)
- **Example selection strategy:** Select examples that span the four K-means cluster archetypes to anchor the LLM's genre space in audio terms
- **Model:** TBD (OpenAI GPT-4o or equivalent)
- **Sampling:** Run on a stratified random sample of 500–1,000 tracks (API cost management)

### Evaluation

1. **Raw accuracy** vs. Spotify `playlist_genre` label
2. **Comparison matrix** — three-way comparison: K-means prediction / KNN prediction / LLM prediction / actual label
3. **Disagreement analysis** — cases where K-means and KNN agree but LLM differs, and vice versa
4. **Confidence / uncertainty** — if the model returns log-probabilities or a confidence score, analyze uncertainty by genre

### Expected output files (`outputs/llm/`)

| File | Contents |
|---|---|
| `llm_predictions.csv` | Per-track LLM prediction and match flag |
| `llm_per_genre_accuracy.csv` | Accuracy by genre |
| `llm_vs_kmeans_vs_knn.csv` | Three-way prediction comparison |
| `llm_disagreement_cases.csv` | Tracks where LLM and KNN disagree |
| `llm_summary.txt` | Console summary |

## Research Questions

- Does world knowledge about genre improve classification beyond audio features alone?
- On which genres does the LLM outperform KNN? On which does it underperform?
- Do LLM errors match K-means errors (shared audio confusion) or are they different (cultural/contextual errors)?
- Can few-shot examples drawn from the K-means cluster centroids improve LLM calibration?

## Script

`analysis/03_llm/fewshot.r` — R script using the Anthropic Claude API.

## Setup

```r
install.packages(c("httr2", "jsonlite", "randomForest"))
Sys.setenv(ANTHROPIC_API_KEY = "sk-ant-...")
source("analysis/03_llm/fewshot.r")
```

Run from the **repository root**.

## Implementation Details

- **Model:** `claude-opus-4-6` via the Anthropic Messages API
- **Few-shot count:** 2 examples per genre (N_SHOT = 2), compact single-line format
- **Batch size:** 5 tracks per API call to amortise the fixed few-shot prefix cost (~95% of each prompt is the shared few-shot block)
- **Test set cap:** 100 stratified samples by default (`MAX_TEST_N = 100`) for cost control
- **Rate limiting:** rolling 60-second token-budget window (`TOKEN_BUDGET = 20,000`) + 429 retry with server-specified backoff
- **Random Forest baseline:** 300-tree RF trained on all 13 features evaluated on the same subsample for direct comparison
- **Cost estimate:** < $1 USD per full run at May 2026 pricing

## Prompt Format

Each track is formatted as a compact feature string:
```
[energy=0.83 tempo=128 dance=0.71 loud=-5.2dB live=0.12 valence=0.65
 speech=0.042 instr=0.001 acoustic=0.05 key=7 mode=1 tsig=4 dur=214s] → rock
```

## Output

Results printed to console:
- Overall accuracy: LLM vs. Random Forest on the same 100-track subsample
- Lift: percentage-point difference (LLM − RF)
- Per-genre accuracy table
- LLM confusion matrix
- Top-7 RF feature importances (Mean Decrease Gini)
