# Data Dictionary

Two CSV files of Spotify track data drawn from playlist-based audio analysis. Both files expose the same columns but cover different popularity tiers.

| File | Rows | Notes |
|---|---|---|
| `high_popularity_spotify_data.csv` | ~1,688 | Tracks from mainstream, high-visibility playlists |
| `low_popularity_spotify_data.csv` | ~3,147 | Tracks from niche, genre-specific, or lower-visibility playlists |

---

## Column Reference

### Track identifiers

| Column | Type | Description |
|---|---|---|
| `track_id` | string | Spotify track URI (unique per track) |
| `track_name` | string | Track title |
| `track_artist` | string | Primary artist name(s) |
| `track_href` | string | Spotify API URL for the track |
| `uri` | string | Full Spotify URI (`spotify:track:<id>`) |

### Album metadata

| Column | Type | Description |
|---|---|---|
| `track_album_id` | string | Spotify album URI |
| `track_album_name` | string | Album title |
| `track_album_release_date` | string | Release date (YYYY-MM-DD or YYYY) |

### Playlist context

| Column | Type | Description |
|---|---|---|
| `playlist_id` | string | Spotify playlist URI |
| `playlist_name` | string | Human-readable playlist name |
| `playlist_genre` | string | Broad genre label assigned to the playlist (e.g. `pop`, `rock`, `jazz`) |
| `playlist_subgenre` | string | Finer subgenre label (e.g. `mainstream`, `classic`, `lofi beats`) |

### Popularity

| Column | Type | Range | Description |
|---|---|---|---|
| `track_popularity` | integer | 0–100 | Spotify popularity score at time of collection |

### Audio features (0–1 scale)

These are the primary modelling features. All are computed by Spotify's audio analysis engine.

| Column | Type | Range | Description |
|---|---|---|---|
| `danceability` | float | 0–1 | How suitable a track is for dancing based on tempo, rhythm stability, beat strength, and regularity. Higher = more danceable. |
| `energy` | float | 0–1 | Perceptual intensity and activity. Energetic tracks feel fast, loud, and noisy. Based on dynamic range, loudness, timbre, onset rate, and entropy. |
| `valence` | float | 0–1 | Musical positiveness. High valence = happy, cheerful, euphoric. Low valence = sad, depressed, angry. |
| `acousticness` | float | 0–1 | Confidence that the track is acoustic (not electronically amplified or processed). 1.0 = high confidence acoustic. |
| `instrumentalness` | float | 0–1 | Probability that the track contains no vocals. Values above 0.5 are intended to represent instrumental tracks; values above 0.8 have high confidence. |
| `speechiness` | float | 0–1 | Presence of spoken words. Values above 0.66 are likely entirely spoken word (podcast, audiobook). 0.33–0.66 may contain both music and speech. Below 0.33 is music. |
| `liveness` | float | 0–1 | Probability that the track was performed live. Values above 0.8 indicate a strong likelihood of a live recording. |

### Audio features (other scales)

| Column | Type | Unit | Description |
|---|---|---|---|
| `loudness` | float | dB | Overall loudness, averaged across the track. Typical range: −60 to 0 dB. |
| `tempo` | float | BPM | Estimated tempo (beats per minute). |
| `duration_ms` | integer | milliseconds | Track duration. |
| `key` | integer | 0–11 | Estimated musical key using standard Pitch Class notation (0 = C, 1 = C♯/D♭, …, 11 = B). −1 if no key was detected. |
| `mode` | integer | 0 or 1 | Modality: 1 = major, 0 = minor. |
| `time_signature` | integer | 3–7 | Estimated number of beats per bar. Most tracks are 4/4 (value = 4). |

### Spotify API metadata

| Column | Type | Description |
|---|---|---|
| `type` | string | Always `audio_features` |
| `id` | string | Duplicate of `track_id` |
| `analysis_url` | string | Spotify API URL for the full audio analysis object |

---

## Notes on Usage

- **Common columns:** Both files share all 29 columns. The analysis combines them with `rbind()` after selecting the intersection of column names.
- **Missing values:** A small number of rows have `NA` in audio feature columns. The analysis applies `complete.cases()` filtering, resulting in 4,830 usable rows from a combined 4,835.
- **Genre label granularity:** `playlist_genre` contains ~35 unique values. `playlist_subgenre` further subdivides each genre. Only `playlist_genre` is used as the ground-truth label in the K-means analysis.
- **Popularity bias:** The high-popularity file skews toward pop, rock, hip-hop, and latin. The low-popularity file contains substantially more electronic, ambient, lofi, world, and other niche genres. This asymmetry is a structural feature of the dataset that materially affects genre match rates (see `reports/kmeans_findings.md` §5.2).

---

## Source

Spotify Web API — audio features endpoint (`/v1/audio-features`). Data was collected via playlist enumeration across genre-tagged Spotify playlists.
