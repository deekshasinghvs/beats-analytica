# Analysis 03 · LLM Few-Shot Genre Classification

> **Status: In progress**

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

`analysis/03_llm/llm_classification.py` — to be created. Requires an OpenAI API key set as the `OPENAI_API_KEY` environment variable.
