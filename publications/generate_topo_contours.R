#!/usr/bin/env Rscript
#Generate randomized topographic contour SVG backgrounds using R.
#Uses either noise generation or random peaks to create unique contour patterns.
#

require(argparse)
require(ggplot2)
require(dplyr)
require(tidyr)

# Try to load ambient for Perlin noise; if not available, use fallback
tryCatch({
  library(ambient)
  HAS_AMBIENT <- TRUE
}, error = function(e) {
  HAS_AMBIENT <<- FALSE
  cat("Warning: 'ambient' package not found. Using fallback random method.\n")
  cat("Install with: install.packages('ambient')\n")
})

#' Generate elevation data using Perlin noise
#'
#' @param seed Random seed for reproducibility
#' @param width SVG width in pixels
#' @param height SVG height in pixels
#' @param octaves Number of noise octaves (more = more detail)
#' @param scale Scale of noise features
#' @param num_contours Number of contour levels
#'
#' @return Matrix of elevation values
generate_perlin_contours <- function(seed = NULL, width = 1200, height = 800, 
                                    octaves = 4, scale = 200, num_contours = 15) {
  if (!is.null(seed)) {
    set.seed(seed)
  }
  
  if (!HAS_AMBIENT) {
    return(generate_random_contours(seed, width, height, num_contours))
  }
  
  # Create coordinate grid
  x <- seq(0, 4, length.out = width)
  y <- seq(0, 4, length.out = height)
  grid <- expand.grid(x = x, y = y)
  
  # Generate Perlin noise using ambient package
  grid$elevation <- noise_perlin(
    x = grid$x,
    y = grid$y,
    frequency = 1 / scale,
    octaves = octaves,
    seed = seed
  )
  
  # Reshape to matrix
  elevations <- matrix(grid$elevation, nrow = height, ncol = width, byrow = FALSE)
  
  # Normalize to 0-1
  elevations <- (elevations - min(elevations)) / (max(elevations) - min(elevations))
  
  return(elevations)
}

#' Generate elevation data using random Gaussian peaks
#'
#' @param seed Random seed for reproducibility
#' @param width SVG width
#' @param height SVG height
#' @param num_contours Number of random peaks to create
#'
#' @return Matrix of elevation values
generate_random_contours <- function(seed = NULL, width = 1200, height = 800, num_contours = 15) {
  if (!is.null(seed)) {
    set.seed(seed)
  }
  
  # Create blank elevation matrix
  elevations <- matrix(0, nrow = height, ncol = width)
  
  # Generate random peaks with Gaussian falloff
  num_peaks <- num_contours * 2
  for (i in 1:num_peaks) {
    cx <- sample(1:width, 1)
    cy <- sample(1:height, 1)
    strength <- runif(1, 0.3, 1.0)
    radius <- sample(100:400, 1)
    
    # Create meshgrid for this peak
    xx <- col(elevations) - cx
    yy <- row(elevations) - cy
    dist <- sqrt(xx^2 + yy^2)
    
    # Gaussian peak
    peak <- strength * exp(-(dist^2) / (2 * radius^2))
    elevations <- elevations + peak
  }
  
  # Normalize
  elevations <- (elevations - min(elevations)) / (max(elevations) - min(elevations) + 1e-6)
  
  return(elevations)
}

#' Create SVG from elevation data using contours
#'
#' @param elevations Matrix of elevation values
#' @param width SVG width
#' @param height SVG height
#' @param num_contours Number of contour levels
#' @param line_color Line color in hex without #
#' @param bg_color Background color in hex without #
#' @param line_width Width of contour lines
#' @param output Output filename (auto-generated if NULL)
#'
#' @return Path to generated SVG file
create_svg_from_contours <- function(elevations, width = 1200, height = 800, 
                                     num_contours = 20, line_color = "e0e0e0",
                                     bg_color = "1a1a1a", line_width = 0.8,
                                     output = NULL) {
  
  # Create data frame for ggplot
  df <- expand.grid(x = 1:ncol(elevations), y = 1:nrow(elevations))
  df$z <- as.vector(elevations)
  
  # Create contour plot
  p <- ggplot(df, aes(x = x, y = y, z = z)) +
    stat_contour(aes(color = after_stat(level)), 
                 bins = num_contours,
                 size = line_width,
                 alpha = 0.7,
                 show.legend = FALSE) +
    scale_color_continuous(low = paste0("#", line_color), high = paste0("#", line_color)) +
    theme_void() +
    theme(
      plot.background = element_rect(fill = paste0("#", bg_color), color = NA),
      panel.background = element_rect(fill = paste0("#", bg_color), color = NA)
    ) +
    coord_equal() +
    xlim(0, width) +
    ylim(0, height)
  
  # Generate output filename if not provided
  if (is.null(output)) {
    timestamp <- format(Sys.time(), "%Y%m%d_%H%M%S")
    output <- paste0("topo_contours_", timestamp, ".svg")
  }
  
  # Save as SVG
  ggsave(output, plot = p, width = width / 100, height = height / 100, dpi = 100,
         device = "svg", bg = paste0("#", bg_color))
  
  cat(sprintf("\n✓ Generated: %s\n", output))
  cat(sprintf("\nTo use this in your HTML, embed it as:\n"))
  cat(sprintf('  <object class="topo-svg" data="%s" type="image/svg+xml"></object>\n', output))
  
  return(output)
}

#' Clean up contour paths to remove artifacts
#'
#' This is handled more gracefully in R's ggplot2, so we don't need
#' the aggressive filtering that was needed in Python.
#' The contour algorithm in R is cleaner by default.

main <- function() {
  parser <- ArgumentParser(description = "Generate randomized topographic contour SVG backgrounds")
  
  parser$add_argument('--seed', type = 'integer', default = NULL,
                      help = 'Random seed for reproducibility (default: random)')
  parser$add_argument('--width', type = 'integer', default = 1200,
                      help = 'SVG width in pixels (default: 1200)')
  parser$add_argument('--height', type = 'integer', default = 800,
                      help = 'SVG height in pixels (default: 800)')
  parser$add_argument('--contours', type = 'integer', default = 20,
                      help = 'Number of contour lines (default: 20)')
  parser$add_argument('--octaves', type = 'integer', default = 4,
                      help = 'Perlin noise octaves, more = more detail (default: 4)')
  parser$add_argument('--scale', type = 'integer', default = 200,
                      help = 'Noise scale, smaller = more features (default: 200)')
  parser$add_argument('--line-color', default = 'e0e0e0',
                      help = 'Line color in hex without # (default: e0e0e0 - light gray)')
  parser$add_argument('--bg-color', default = '1a1a1a',
                      help = 'Background color in hex without # (default: 1a1a1a - dark)')
  parser$add_argument('--line-width', type = 'double', default = 0.8,
                      help = 'Contour line width (default: 0.8)')
  parser$add_argument('--method', default = 'perlin', choices = c('perlin', 'random'),
                      help = 'Generation method: perlin or random (default: perlin)')
  parser$add_argument('--output', default = NULL,
                      help = 'Output filename (default: auto-generated with timestamp)')
  
  args <- parser$parse_args()
  
  cat("Generating topographic contours...\n")
  cat(sprintf("  Seed: %s\n", if (is.null(args$seed)) "random" else args$seed))
  cat(sprintf("  Size: %dx%d\n", args$width, args$height))
  cat(sprintf("  Contours: %d\n", args$contours))
  cat(sprintf("  Method: %s\n", args$method))
  
  # Generate elevation data
  if (args$method == 'perlin') {
    if (HAS_AMBIENT) {
      elevations <- generate_perlin_contours(
        seed = args$seed,
        width = args$width,
        height = args$height,
        octaves = args$octaves,
        scale = args$scale,
        num_contours = args$contours
      )
    } else {
      cat("  (Falling back to random method - ambient package not installed)\n")
      elevations <- generate_random_contours(
        seed = args$seed,
        width = args$width,
        height = args$height,
        num_contours = args$contours
      )
    }
  } else {
    elevations <- generate_random_contours(
      seed = args$seed,
      width = args$width,
      height = args$height,
      num_contours = args$contours
    )
  }
  
  # Create SVG
  svg_path <- create_svg_from_contours(
    elevations,
    width = args$width,
    height = args$height,
    num_contours = args$contours,
    line_color = args$line_color,
    bg_color = args$bg_color,
    line_width = args$line_width,
    output = args$output
  )
  
  invisible(svg_path)
}

# Run if executed as script
if (identical(environment(), globalenv())) {
  main()
}
