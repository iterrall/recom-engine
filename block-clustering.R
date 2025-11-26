#library(tidyverse)
library(pheatmap)

ratings <- read.csv("data/ml-20m/ratings.csv")

library(data.table)

# Convert to data.table
setDT(ratings)

# Set thresholds
min_user_ratings <- 1000
min_movie_ratings <- 6000

# Count ratings per user and movie
user_counts <- ratings[, .N, by = userId]
movie_counts <- ratings[, .N, by = movieId]

# Filter users and movies
users_to_keep <- user_counts[N >= min_user_ratings, userId]
movies_to_keep <- movie_counts[N >= min_movie_ratings, movieId]

# Create the pivot table with zeros for missing combinations
pivot_matrix <- dcast(
  ratings[userId %in% users_to_keep & movieId %in% movies_to_keep],
  userId ~ movieId,
  value.var = "rating",
  fill = 0,
  drop = FALSE  # This ensures all users_to_keep and movies_to_keep are included
)

# Convert to matrix with userId as rownames
user_ids <- pivot_matrix$userId
pivot_matrix <- as.matrix(pivot_matrix[, -1])
rownames(pivot_matrix) <- user_ids

cat("Matrix dimensions:", dim(pivot_matrix), "\n")
cat("Number of zeros:", sum(pivot_matrix == 0), "\n")
cat("Number of non-zeros:", sum(pivot_matrix != 0), "\n")



# Generate clustered heatmap (similar to seaborn.clustermap)
pheatmap(
  log1p(pivot_matrix),
  color = colorRampPalette(c("blue", "white", "red"))(50),
  clustering_distance_rows = "euclidean",  # same as metric="euclidean"
  clustering_distance_cols = "euclidean",
  clustering_method = "average",
  show_rownames = FALSE,
  show_colnames = FALSE,
  cutree_rows = 2, 
  cutree_cols = 2,
  treeheight_row = 0,
  treeheight_col = 0,
  labels_row = rep(" ", nrow(pivot_matrix)),
  labels_col = rep(" ", ncol(pivot_matrix)),
  angle_col = 0
  #main = "Aggregated Order Values for Customer/Part Family pairs",
  #legend = TRUE,
  #legend_title = "Log Transformed Order Values")
)

