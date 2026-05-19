# Topographic Contour Generator (R Version)

Generate custom, randomized topographic contour map backgrounds for your publications page using R.

## Installation

First, install the required R packages:

```R
install.packages(c("argparse", "ggplot2", "dplyr", "tidyr"))
install.packages("ambient")  # Optional, for Perlin noise; script will fall back to random if not available
```

Or from the command line:

```bash
Rscript -e 'install.packages(c("argparse", "ggplot2", "dplyr", "tidyr", "ambient"))'
```

## Usage

### Basic Usage

Generate a random topographic contour SVG with default settings:

```bash
Rscript generate_topo_contours.R
```

This creates a file like `topo_contours_20240519_143022.svg` in your current directory.

### With a Specific Seed (for Reproducibility)

If you find a contour map you like, use the seed to regenerate it later:

```bash
Rscript generate_topo_contours.R --seed 42
```

This uses seed `42`, so you'll always get the same contour pattern.

### Adjusting Parameters

**Number of contours (default: 20):**
```bash
Rscript generate_topo_contours.R --contours 30  # More contours = denser
Rscript generate_topo_contours.R --contours 10  # Fewer = sparser
```

**Line width (default: 0.8):**
```bash
Rscript generate_topo_contours.R --line-width 1.2  # Thicker lines
Rscript generate_topo_contours.R --line-width 0.5  # Thinner lines
```

**Line color (default: e0e0e0, light gray):**
```bash
Rscript generate_topo_contours.R --line-color "a0a0a0"  # Darker gray
Rscript generate_topo_contours.R --line-color "00d4d4"  # Teal (LCARS!)
Rscript generate_topo_contours.R --line-color "ff9d42"  # Orange (LCARS!)
```

**Background color (default: 1a1a1a, dark):**
```bash
Rscript generate_topo_contours.R --bg-color "0a0a0a"  # Even darker
```

**Noise detail (Perlin method only, default octaves: 4):**
```bash
Rscript generate_topo_contours.R --octaves 6  # More fractal detail
Rscript generate_topo_contours.R --octaves 2  # Smoother, larger features
```

**Generation method (default: perlin):**
```bash
Rscript generate_topo_contours.R --method random   # Use random peaks instead
```

### Full Example with All Options

```bash
Rscript generate_topo_contours.R \
  --seed 123 \
  --contours 25 \
  --line-width 0.9 \
  --line-color "a8a8a8" \
  --octaves 5 \
  --method perlin
```

## Iteration Workflow

Here's how to find a contour pattern you like:

1. **Generate several random variations:**
   ```bash
   Rscript generate_topo_contours.R --seed 1
   Rscript generate_topo_contours.R --seed 2
   Rscript generate_topo_contours.R --seed 3
   ```

2. **View the SVGs** — Open them in your browser or image viewer to see the patterns

3. **Once you find one you like, note the seed:**
   - If you like the SVG generated with `--seed 42`, save that seed

4. **Fine-tune parameters** with that seed:
   ```bash
   Rscript generate_topo_contours.R --seed 42 --contours 22 --line-width 1.0
   ```

5. **Try different colors:**
   ```bash
   Rscript generate_topo_contours.R --seed 42 --line-color "00d4d4"  # Teal
   ```

6. **Test with different octaves** (for Perlin):
   ```bash
   Rscript generate_topo_contours.R --seed 42 --octaves 3  # Smoother
   Rscript generate_topo_contours.R --seed 42 --octaves 6  # More detail
   ```

## Using the SVG in Your HTML

Once you've found a contour map you like:

1. **Copy the SVG file** to your publications folder:
   ```bash
   cp topo_contours_XXXXXX.svg /path/to/publications/images/topo-bg.svg
   ```

2. **Your HTML is already set up** to use it at `/publications/images/topo-bg.svg`

## Parameter Recommendations

### For a Subtle, Professional Look:
```bash
Rscript generate_topo_contours.R --seed YOURNUM --contours 15 --line-width 0.6 --line-color "c0c0c0"
```

### For a Bold, Dramatic Look:
```bash
Rscript generate_topo_contours.R --seed YOURNUM --contours 30 --line-width 1.2 --line-color "a0a0a0"
```

### For LCARS Color Palette:
```bash
Rscript generate_topo_contours.R --seed YOURNUM --line-color "00d4d4"  # Teal
# or
Rscript generate_topo_contours.R --seed YOURNUM --line-color "ff9d42"  # Orange
```

### For High Detail (Perlin):
```bash
Rscript generate_topo_contours.R --seed YOURNUM --octaves 6 --contours 25
```

### For Smooth, Large Features (Perlin):
```bash
Rscript generate_topo_contours.R --seed YOURNUM --octaves 2 --contours 15
```

## Troubleshooting

**"Error: could not find function"**
- Make sure all packages are installed: `install.packages(c("argparse", "ggplot2", "dplyr", "tidyr"))`

**"Warning: ambient package not found"**
- Install it: `install.packages("ambient")`
- Or use the fallback: `--method random`

**Lines are too thick/thin**
- Adjust `--line-width` (range 0.5-2.0 is usually good)

**Too many or too few contours**
- Adjust `--contours` (try 10-40)

**Pattern looks too uniform/random**
- For Perlin: adjust `--octaves` (2-6 range)
- For random: that's the nature of it; try a different seed

**Colors not showing up**
- Make sure you're using hex colors *without* the `#` symbol
- Example: `--line-color "ff0000"` (not `#ff0000`)

## Advantages of R Version

- **ggplot2's contour algorithm** produces cleaner results with fewer artifacts
- **No post-processing needed** — R's `stat_contour` handles path cleaning automatically
- **Ambient package** provides excellent Perlin noise with fine control
- **Familiar to statisticians** — if you use R already, it fits your workflow

## Examples

**Quick random:**
```bash
Rscript generate_topo_contours.R
```

**Refined teal LCARS look:**
```bash
Rscript generate_topo_contours.R --seed 777 --contours 18 --line-width 0.7 --line-color "00a8a8"
```

**Dramatic high-detail:**
```bash
Rscript generate_topo_contours.R --seed 555 --octaves 6 --contours 28 --line-width 1.0
```

**Smooth, subtle:**
```bash
Rscript generate_topo_contours.R --seed 333 --octaves 2 --contours 12 --line-width 0.5 --line-color "d0d0d0"
```
