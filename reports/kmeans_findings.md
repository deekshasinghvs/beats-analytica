# K-Means Clustering of Spotify Audio Features
### Beats Analytica · Spring 2026

---

## 1. Overview

This analysis applies unsupervised K-means clustering to 4,830 Spotify tracks using ten measurable audio features. The goal is not to build a genre classifier but to ask a more fundamental question: **do tracks that sound alike also share a genre label?** Discrepancies between the audio-derived clusters and Spotify's playlist genre labels reveal where genre is a sonic construct and where it is a cultural or marketing one.

| Item | Value |
|---|---|
| Tracks analyzed | 4,830 (after complete-case filtering) |
| Source datasets | `high_popularity_spotify_data.csv` + `low_popularity_spotify_data.csv` |
| Audio features used | danceability, energy, tempo, valence, acousticness, instrumentalness, speechiness, liveness, loudness, duration\_ms |
| Algorithm | K-means (`kmeans()`, nstart = 50, iter.max = 100, set.seed(123)) |
| Cluster selection | k = 4 (elbow + silhouette plateau) |
| Evaluation metric | Cluster-to-genre majority label match rate |
| **Overall genre match rate** | **21.3%** |
| Script | `deliverables/kmeans_analysis.R` |

---

## 2. Model Selection — Choosing k

Candidate values k = 2 through 8 were evaluated on two metrics: average silhouette score (measures how well each track fits its assigned cluster vs. its nearest neighbor cluster) and total within-cluster sum of squares (WSS, measures cluster compactness).

| k | Total WSS | Between SS | Avg Silhouette |
|---|---:|---:|---:|
| 2 | 35,086 | 13,204 | 0.341 |
| 3 | 31,580 | 16,710 | 0.204 |
| **4** | **28,437** | **19,853** | **0.199** |
| 5 | 26,023 | 22,267 | 0.193 |
| 6 | 24,052 | 24,238 | 0.168 |
| 7 | 22,560 | 25,730 | 0.169 |
| 8 | 21,097 | 27,193 | 0.175 |

**Critical reading of the metrics.** The silhouette score peaks sharply at k = 2 (0.341) and drops substantially at k = 3 (0.204), after which it plateaus. Taken at face value, this would favor k = 2 — but two clusters would collapse the entire dataset into "acoustic/quiet" vs. "energetic/produced," which is too coarse to be analytically interesting. The plateau from k = 4 onward means additional clusters do not impose meaningfully greater separation costs. The elbow in WSS is visible between k = 3 and k = 5. **k = 4 was selected** as the point where the WSS reduction slows and four interpretable, distinct sonic archetypes emerge.

The moderate overall silhouette scores (0.17–0.34) are themselves informative: audio features do not partition the musical landscape into sharply separated groups. Genre overlap in audio space is real and measurable.

---

## 3. The Four Cluster Profiles

All ten features were z-score scaled before clustering. The feature means below are back-transformed to original units.

### Cluster 1 — Quiet Acoustic (n = 355, 7.3% of tracks)

| Feature | Mean |
|---|---|
| Acousticness | 0.93 |
| Instrumentalness | 0.84 |
| Energy | 0.07 |
| Valence | 0.09 |
| Loudness | −29.7 dB |
| Speechiness | 0.04 |
| Danceability | 0.21 |

**Dominant genre:** classical (24.8%) · **Top 3:** classical, wellness, ambient

These tracks occupy the most extreme sonic position in the dataset: near-zero energy, almost entirely instrumental, and exceptionally quiet. A loudness of −29.7 dB is roughly four times quieter than the mainstream cluster. The absence of speech (0.04) and near-total instrumentalness (0.84) define this as the dataset's "pure music" corner. Classical, wellness, and ambient converge here because all three genres share the same audio signature despite being culturally distinct.

**Critical note:** Even within this cluster, the dominant genre captures only 24.8% of tracks. The remainder consists of wellness (80), ambient (73), gaming (13), and others — none of which are acoustically wrong, but each carries a genre label driven by context (yoga playlist, video game soundtrack) rather than sound.

---

### Cluster 2 — Vocal Rhythmic (n = 789, 16.3% of tracks)

| Feature | Mean |
|---|---|
| Speechiness | 0.30 |
| Danceability | 0.72 |
| Energy | 0.66 |
| Valence | 0.57 |
| Acousticness | 0.26 |
| Instrumentalness | 0.03 |

**Dominant genre:** hip-hop (30.0%) · **Top 3:** hip-hop, latin, ambient

Speechiness at 0.30 is the single most distinctive feature of this cluster — nearly five times higher than any other cluster. This is the voice-forward, rhythm-driven space. Hip-hop and latin share this cluster because both genres rely heavily on vocal delivery and percussive rhythm, despite being culturally and linguistically distinct. The presence of ambient (103 tracks) in this cluster is counterintuitive and worth examining: ambient tracks with spoken-word elements or binaural beats with vocal layers are pulled into this cluster by their speechiness scores.

**Critical note:** A 30.0% dominant share means 70% of tracks in this cluster are not hip-hop. The cluster captures a sonic archetype — rhythmic vocal music — that multiple genre labels occupy simultaneously.

---

### Cluster 3 — Mellow Semi-Instrumental (n = 991, 20.5% of tracks)

| Feature | Mean |
|---|---|
| Acousticness | 0.66 |
| Instrumentalness | 0.51 |
| Energy | 0.37 |
| Valence | 0.34 |
| Loudness | −12.0 dB |
| Speechiness | 0.06 |

**Dominant genre:** lofi (26.8%) · **Top 3:** lofi, jazz, electronic

This cluster occupies the middle acoustic space: quieter and more organic-sounding than the mainstream clusters, but more present and textured than Cluster 1. Instrumentalness at 0.51 places it at the boundary between vocal and instrumental music. Low valence (0.34) signals that this sonic space tends toward moody, introspective tones. Lofi, jazz, and certain strands of electronic music converge here because they all share a mellow, partly instrumental, low-energy profile. The presence of 99 electronic tracks is notable — these are not high-BPM electronic tracks; they are ambient electronic, IDM, or downtempo productions.

---

### Cluster 4 — Energetic Mainstream (n = 2,695, 55.8% of tracks)

| Feature | Mean |
|---|---|
| Energy | 0.72 |
| Danceability | 0.66 |
| Valence | 0.56 |
| Acousticness | 0.17 |
| Instrumentalness | 0.05 |
| Loudness | −6.4 dB |

**Dominant genre:** pop (16.2%) · **Top 3:** pop, electronic, rock

This cluster holds more than half of all tracks. It is defined by high energy, strong production, and low acousticness — characteristics shared by commercial pop, rock, electronic, and large portions of latin, hip-hop, and world music. The dominant share is only 16.2%, the lowest of any cluster, meaning the majority label (pop) represents a small minority of the cluster's contents. This is by design: the cluster does not represent one genre — it represents a production aesthetic.

**Critical note:** The size and heterogeneity of Cluster 4 is the strongest evidence in the dataset that the energetic, produced commercial sound has become a cross-genre default. Genre labels within this cluster (pop, rock, electronic, latin) function as cultural markers, not acoustic descriptions.

---

## 4. Genre Distribution across Clusters

The table below shows track counts for the ten most analytically interesting genres, broken by cluster.

| Genre | C1 Quiet Acoustic | C2 Vocal Rhythmic | C3 Mellow Semi-Instr. | C4 Energetic Mainstream | Total | Concentration |
|---|---:|---:|---:|---:|---:|---|
| ambient | 73 | 103 | 58 | 125 | 359 | Low |
| classical | 88 | 0 | 30 | 3 | 121 | **High** |
| electronic | 67 | 54 | 99 | 369 | 589 | Low |
| hip-hop | 0 | 237 | 7 | 151 | 395 | Medium |
| jazz | 2 | 6 | 116 | 22 | 146 | **High** |
| latin | 0 | 111 | 47 | 267 | 425 | Low |
| lofi | 19 | 11 | 266 | 2 | 298 | **High** |
| pop | 0 | 23 | 56 | 436 | 515 | Medium |
| rock | 0 | 5 | 18 | 322 | 345 | Medium |
| wellness | 80 | 0 | 0 | 0 | 80 | **High** |

**Genres with high concentration (strong sonic identity):** classical, lofi, wellness, jazz. These genres cluster because their audio profile is consistent and measurable.

**Genres with low concentration (weak sonic identity):** ambient, electronic, latin. These genres scatter because their label describes mood, geography, or cultural context — not a stable set of audio properties.

**Genres with medium concentration:** hip-hop, pop, rock. These genres have a recognizable sound but their commercial mainstream success means they bleed into the large Cluster 4 alongside other produced genres.

---

## 5. Genre Match Rate Analysis

### 5.1 Overall: 21.3%

When each cluster is assigned its majority genre label and that label is applied to every track in the cluster, 21.3% of tracks receive a label matching their actual Spotify playlist genre. The critical interpretation is that this number is the finding itself, not a measure of model quality.

A 21.3% match rate means:
- **78.7% of tracks are assigned to a cluster whose sonic archetype differs from their genre label.** These are not mislabeled tracks — they are evidence of genre definitions that operate on non-audio dimensions.
- Genres whose match rate would be high (classical, lofi) are genres where the label *is* an audio description.
- Genres whose match rate would be low (ambient, electronic, latin, pop) are genres where the label is a cultural or commercial category.

### 5.2 By Popularity Tier

| Popularity Tier | Tracks | Genre Match Rate |
|---|---:|---:|
| High popularity | 1,686 | **25.4%** |
| Low popularity | 3,144 | **19.1%** |
| Overall | 4,830 | 21.3% |

High-popularity tracks align with their genre labels approximately 33% more often than low-popularity tracks. This gap is explained by the composition of each dataset, not by any inherent property of popularity itself.

**High popularity genre mix (top 5):** pop (357), rock (235), hip-hop (227), latin (184), electronic (148)

**Low popularity genre mix (top 5):** electronic (441), ambient (298), lofi (296), latin (241), world (224)

The high popularity dataset is dominated by genres that have a well-established, commercially reinforced sonic identity — pop sounds like pop, rock sounds like rock. The low popularity dataset includes far more niche and culturally defined genres (ambient, world, lofi, brazilian, arabic) whose labels carry less audio information.

### 5.3 Match Rate by Cluster and Popularity Tier

| Cluster (majority label) | High popularity match | Low popularity match | Gap |
|---|---:|---:|---:|
| C1 — hip-hop | 42.9% | 23.2% | 19.7 pp |
| C2 — classical | **64.3%** | 23.2% | 41.1 pp |
| C3 — lofi | 1.2% | **32.2%** | −31.0 pp |
| C4 — pop | 24.4% | 9.3% | 15.1 pp |

Three specific findings deserve attention:

**Classical cluster, high popularity (64.3%):** Only 14 high-popularity tracks land in the classical cluster, and almost all are genuinely classical recordings. High-popularity classical music is acoustically unmistakable. Low-popularity tracks from wellness, ambient, and gaming genres migrate into this cluster because they share the audio profile but not the cultural label.

**Lofi cluster, high popularity (1.2%):** 172 high-popularity tracks land in the lofi cluster, meaning they sound like lofi music — mellow, partly instrumental, acoustically textured — but almost none (just 2 tracks) carry the lofi genre label. High-popularity music is almost never labeled lofi regardless of its audio properties. This is one of the clearest demonstrations in the dataset of the gap between sonic and cultural genre assignment.

**Lofi cluster, low popularity (32.2%):** By contrast, low-popularity tracks in this cluster are the genre's natural home: 266 of 991 Cluster 3 tracks are genuinely labeled lofi, giving the cluster its highest single-genre match rate among all low-popularity cluster pairings.

---

## 6. Critical Assessment

### What the model does well

- Recovers four meaningful sonic archetypes from unlabeled audio data, with clear feature-level interpretability.
- Identifies which genres have a stable, measurable audio identity (classical, lofi, wellness) vs. which are culturally constructed categories (ambient, electronic, latin).
- The popularity-tier split reveals a structural asymmetry in how genre labels relate to audio properties across different segments of the streaming market.

### What the model cannot do

- **K-means assumes spherical clusters** in feature space. Real genre distributions are likely non-convex and non-spherical — genres like "ambient" or "electronic" may form multiple disconnected regions in audio space that K-means collapses into one assignment or spreads across clusters.
- **The majority-label match rate is a blunt metric.** A track labeled "latin" that lands in the hip-hop cluster may be a reggaeton track that is acoustically indistinguishable from hip-hop — the "mismatch" is informative, not erroneous.
- **No temporal or artist-level features are used.** Genre is partly a function of who makes the music and when — two tracks with identical audio features may be categorized differently based on the artist's established genre identity.
- **Cluster labeling is arbitrary.** The label assigned to each cluster (its majority genre) changes if the dataset composition changes — as seen in the popularity-split re-run, where cluster numbering shifted. The underlying audio archetypes are stable; their majority-genre labels are artifacts of dataset balance.
- **k = 4 is an analytical choice, not a ground truth.** The dataset contains 35+ genre labels. Four clusters can only approximate the true structure. Increasing k captures more variation but reduces interpretability.

### Implications for the broader project

The K-means results establish a baseline for the research question: **audio features alone explain roughly 21% of genre label assignment.** The remaining 79% is driven by factors outside the audio signal. This creates a principled benchmark against which the supervised KNN classifier and the LLM few-shot classifier can be compared. If KNN outperforms 21.3% substantially, the additional signal comes from learning decision boundaries from labeled examples. If the LLM outperforms both, it is drawing on world knowledge about genre conventions that neither audio features nor labels alone can capture.

The popularity-tier finding also motivates a potential segmentation strategy: genre prediction may be more tractable for high-popularity mainstream tracks and inherently less reliable for the long-tail of niche or culturally specific genres.

---

## 7. Output Files

All outputs are in `deliverables/kmeans_outputs/`.

| File | Contents |
|---|---|
| `k_selection_metrics.csv` | WSS, between-SS, and silhouette for k = 2–8 |
| `cluster_feature_means.csv` | Mean value of each audio feature per cluster |
| `cluster_sizes.csv` | Track count per cluster |
| `cluster_genre_summary.csv` | Dominant genre, share, and top-3 genres per cluster |
| `genre_by_cluster_counts.csv` | Full genre × cluster cross-tabulation |
| `track_level_cluster_assignments.csv` | Per-track cluster, predicted genre, and match flag |
| `kmeans_pca_clusters.png` | PCA scatter plot of clusters (PC1 vs PC2) |
| `kmeans_summary.txt` | Console-formatted summary of all key results |

---

*Analysis performed in R · `deliverables/kmeans_analysis.R` · Beats Analytica, April 2026*
