set.seed(123)

suppressPackageStartupMessages({
  library(cluster)
})

data_dir <- "data"
output_dir <- file.path("outputs", "kmeans")
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

high_path <- file.path(data_dir, "high_popularity_spotify_data.csv")
low_path <- file.path(data_dir, "low_popularity_spotify_data.csv")

high_data <- read.csv(high_path, stringsAsFactors = FALSE)
low_data <- read.csv(low_path, stringsAsFactors = FALSE)

common_cols <- intersect(names(high_data), names(low_data))
spotify <- rbind(high_data[, common_cols], low_data[, common_cols])

feature_cols <- c(
  "danceability",
  "energy",
  "tempo",
  "valence",
  "acousticness",
  "instrumentalness",
  "speechiness",
  "liveness",
  "loudness",
  "duration_ms"
)

analysis_cols <- c("track_name", "track_artist", "playlist_genre", feature_cols)
spotify_model <- spotify[, analysis_cols]
spotify_model <- spotify_model[complete.cases(spotify_model), ]
spotify_model$playlist_genre <- trimws(tolower(spotify_model$playlist_genre))

scaled_features <- scale(spotify_model[, feature_cols])

k_grid <- 2:8
k_diagnostics <- lapply(k_grid, function(k) {
  km <- kmeans(scaled_features, centers = k, nstart = 25, iter.max = 100)
  silhouette_avg <- mean(silhouette(km$cluster, dist(scaled_features))[, 3])

  data.frame(
    k = k,
    tot_withinss = km$tot.withinss,
    betweenss = km$betweenss,
    avg_silhouette = silhouette_avg
  )
})

k_diagnostics <- do.call(rbind, k_diagnostics)
write.csv(k_diagnostics, file.path(output_dir, "k_selection_metrics.csv"), row.names = FALSE)

# Silhouette favors smaller k in this dataset, but k = 4 preserves more
# meaningful separation across broad genre families than k = 2.
final_k <- 4
final_kmeans <- kmeans(scaled_features, centers = final_k, nstart = 50, iter.max = 100)
spotify_model$cluster <- factor(final_kmeans$cluster)

cluster_sizes <- as.data.frame(table(spotify_model$cluster), stringsAsFactors = FALSE)
names(cluster_sizes) <- c("cluster", "n_tracks")
write.csv(cluster_sizes, file.path(output_dir, "cluster_sizes.csv"), row.names = FALSE)

cluster_feature_means <- aggregate(
  spotify_model[, feature_cols],
  by = list(cluster = spotify_model$cluster),
  FUN = mean
)
write.csv(cluster_feature_means, file.path(output_dir, "cluster_feature_means.csv"), row.names = FALSE)

genre_cluster_table <- as.data.frame.matrix(table(spotify_model$cluster, spotify_model$playlist_genre))
genre_cluster_table <- cbind(cluster = rownames(genre_cluster_table), genre_cluster_table)
rownames(genre_cluster_table) <- NULL
write.csv(genre_cluster_table, file.path(output_dir, "genre_by_cluster_counts.csv"), row.names = FALSE)

cluster_purity <- do.call(
  rbind,
  lapply(split(spotify_model, spotify_model$cluster), function(cluster_df) {
    genre_counts <- sort(table(cluster_df$playlist_genre), decreasing = TRUE)
    dominant_genre <- names(genre_counts)[1]
    dominant_share <- as.numeric(genre_counts[1]) / nrow(cluster_df)

    data.frame(
      cluster = unique(cluster_df$cluster),
      size = nrow(cluster_df),
      dominant_genre = dominant_genre,
      dominant_share = round(dominant_share, 3),
      top_3_genres = paste(
        paste(names(genre_counts)[1:min(3, length(genre_counts))],
              as.integer(genre_counts[1:min(3, length(genre_counts))]),
              sep = ": "),
        collapse = " | "
      )
    )
  })
)
write.csv(cluster_purity, file.path(output_dir, "cluster_genre_summary.csv"), row.names = FALSE)

majority_map <- aggregate(
  playlist_genre ~ cluster,
  data = spotify_model,
  FUN = function(x) names(sort(table(x), decreasing = TRUE))[1]
)
names(majority_map)[2] <- "predicted_genre"
spotify_model <- merge(spotify_model, majority_map, by = "cluster", all.x = TRUE, sort = FALSE)
spotify_model$genre_match <- spotify_model$playlist_genre == spotify_model$predicted_genre

overall_match_rate <- mean(spotify_model$genre_match)

pca_fit <- prcomp(scaled_features, center = FALSE, scale. = FALSE)
pca_scores <- as.data.frame(pca_fit$x[, 1:2])
pca_scores$cluster <- spotify_model$cluster

png(
  filename = file.path(output_dir, "kmeans_pca_clusters.png"),
  width = 1000,
  height = 700
)
plot(
  pca_scores$PC1,
  pca_scores$PC2,
  col = as.integer(pca_scores$cluster),
  pch = 19,
  cex = 0.55,
  xlab = "PC1",
  ylab = "PC2",
  main = "K-means Clusters on Spotify Audio Features"
)
legend(
  "topright",
  legend = levels(pca_scores$cluster),
  col = seq_along(levels(pca_scores$cluster)),
  pch = 19,
  title = "Cluster"
)
dev.off()

sink(file.path(output_dir, "kmeans_summary.txt"))
cat("Spotify K-means analysis\n")
cat("========================\n\n")
cat("Observations used:", nrow(spotify_model), "\n")
cat("Features used:", paste(feature_cols, collapse = ", "), "\n")
cat("Candidate k values:", paste(k_grid, collapse = ", "), "\n")
cat("Selected k:", final_k, "\n")
cat("Overall majority-genre match rate:", round(overall_match_rate, 3), "\n\n")

cat("K selection diagnostics\n")
print(k_diagnostics, row.names = FALSE)
cat("\nCluster genre summary\n")
print(cluster_purity, row.names = FALSE)
cat("\nInterpretation\n")
cat(
  paste(
    "Clusters reflect broad audio profiles rather than a one-to-one genre mapping.",
    "Any mismatch between a cluster's dominant genre and the labeled genre is evidence",
    "of genre overlap, mixed playlist curation, or ambiguous sonic boundaries."
  ),
  "\n"
)
sink()

write.csv(
  spotify_model[, c("track_name", "track_artist", "playlist_genre", "cluster", "predicted_genre", "genre_match")],
  file.path(output_dir, "track_level_cluster_assignments.csv"),
  row.names = FALSE
)

message("K-means analysis complete. Outputs saved to: ", output_dir)
